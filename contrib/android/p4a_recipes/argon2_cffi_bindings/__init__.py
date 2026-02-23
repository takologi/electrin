import glob
import os
import shutil

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

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)

        # 1) p4a sets PYTHONHOME to the target Python during builds, which
        #    hides hostpython3's own Lib/site-packages (including setuptools).
        #    Prepend hostpython3's site-packages to PYTHONPATH explicitly.
        hp_sp = os.path.join(os.path.dirname(str(self.ctx.hostpython)),
                             'Lib', 'site-packages')
        if not os.path.isdir(hp_sp):
            # Fallback: glob search in the build tree
            matches = glob.glob(os.path.join(
                self.ctx.build_dir, 'other_builds', 'hostpython3',
                '*', 'hostpython3', 'native-build', 'Lib', 'site-packages'))
            if matches:
                hp_sp = matches[0]
        if os.path.isdir(hp_sp):
            existing = env.get('PYTHONPATH', '')
            env['PYTHONPATH'] = hp_sp + (os.pathsep + existing
                                         if existing else '')

        # 2) argon2-cffi-bindings' _ffi_build.py detects the HOST arch
        #    (x86_64) and selects the SSE2-optimised libargon2/src/opt.c,
        #    which fails to compile for the ARM64 target. Setting
        #    ARGON2_CFFI_USE_SSE2=0 forces the portable ref.c path and
        #    also drops the -msse2 compile flag.
        env['ARGON2_CFFI_USE_SSE2'] = '0'

        # 3) On Android the linker does not resolve Python C-API symbols
        #    unless the extension is explicitly linked against libpython.
        #    PythonRecipe only adds -lpython when
        #    call_hostpython_via_targetpython is False; CFFI API-mode
        #    extensions (_ffi.so) still call into the Python C-API, so
        #    we must add the flag here.
        python_recipe = self.ctx.python_recipe
        env['LDFLAGS'] += ' -L{} -lpython{}'.format(
            python_recipe.link_root(arch.arch),
            python_recipe.link_version,
        )

        return env

    def build_arch(self, arch):
        # Delete any _ffi.c cached from a prior failed run that still
        # references opt.c (wrong arch) so cffi regenerates it cleanly.
        build_dir = self.get_build_dir(arch.arch)
        for cached in glob.glob(
                os.path.join(build_dir, '**', '_ffi.c'), recursive=True):
            try:
                with open(cached, 'rb') as fh:
                    if b'opt.c' in fh.read():
                        os.remove(cached)
            except OSError:
                pass

        super().build_arch(arch)

        # setup.py install only installs the CFFI extension (_ffi.abi3.so)
        # but not the package's __init__.py, because setup.py relies on
        # pyproject.toml's [tool.setuptools.packages.find] which is not
        # processed during legacy 'setup.py install'.  Copy it manually.
        build_dir = self.get_build_dir(arch.arch)
        install_dir = self.ctx.get_python_install_dir(arch.arch)
        src_init = os.path.join(build_dir, 'src',
                                '_argon2_cffi_bindings', '__init__.py')
        dst_init = os.path.join(install_dir,
                                '_argon2_cffi_bindings', '__init__.py')
        if os.path.isfile(src_init) and not os.path.isfile(dst_init):
            os.makedirs(os.path.dirname(dst_init), exist_ok=True)
            shutil.copy2(src_init, dst_init)


recipe = Argon2CffiBindingsRecipe()


