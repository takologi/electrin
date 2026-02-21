import os

from pythonforandroid.recipe import PythonRecipe


assert PythonRecipe.depends == ['python3']
assert PythonRecipe.python_depends == []


class Argon2CffiBindingsRecipe(PythonRecipe):
    # Low-level C bindings for Argon2, bundled with the argon2 C source.
    # Compiled via CFFI; requires the cffi recipe for cross-compilation.
    version = "25.1.0"
    sha512sum = "64e387a4997b5a905e177b62d1bfb5fafb3b466c10c759d5305fa3e4ec35b7f386eabd34562157266405114c0c71a8c616e25efd9fd8638de03bcc16cc3df6df"
    url = "https://files.pythonhosted.org/packages/5c/2d/db8af0df73c1cf454f71b2bbe5e356b8c1f8041c979f505b3d3186e520a9/argon2_cffi_bindings-{version}.tar.gz"
    depends = ["setuptools", "cffi"]

    def build_arch(self, arch):
        import glob
        import os
        build_dir = self.get_build_dir(arch.arch)

        # The CFFI builder chooses between libargon2/src/opt.c (SSE2,
        # x86-only) and ref.c (portable) based on the HOST machine arch.
        # When cross-compiling for ARM64 from an x86 host, opt.c is
        # selected, which fails with clang for aarch64.  Force ref.c.
        for path in glob.glob(
                os.path.join(build_dir, '**', '*.py'), recursive=True) + \
                glob.glob(
                os.path.join(build_dir, '**', '*.c'), recursive=True):
            try:
                with open(path, 'rb') as fh:
                    data = fh.read()
                if b'libargon2/src/opt.c' in data:
                    with open(path, 'wb') as fh:
                        fh.write(data.replace(
                            b'libargon2/src/opt.c',
                            b'libargon2/src/ref.c'))
            except (OSError, PermissionError):
                pass

        # Remove cached _ffi.c so cffi regenerates it using ref.c
        for cached in glob.glob(
                os.path.join(build_dir, '**', '_ffi.c'), recursive=True):
            try:
                with open(cached, 'rb') as fh:
                    if b'opt.c' in fh.read():
                        os.remove(cached)
            except OSError:
                pass

        super().build_arch(arch)


        env = super().get_recipe_env(arch, with_flags_in_cc)
        # p4a sets PYTHONHOME during builds to point at the target Python,
        # which hides hostpython3's own Lib/site-packages (including
        # setuptools).  Prepend hostpython3's site-packages to PYTHONPATH
        # so that setup.py can 'import setuptools' regardless.
        hp_sp = os.path.join(os.path.dirname(self.ctx.hostpython),
                             'Lib', 'site-packages')
        if os.path.isdir(hp_sp):
            existing = env.get('PYTHONPATH', '')
            env['PYTHONPATH'] = hp_sp + (os.pathsep + existing
                                         if existing else '')
        return env


recipe = Argon2CffiBindingsRecipe()
