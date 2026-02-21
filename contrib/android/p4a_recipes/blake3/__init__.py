import os

from pythonforandroid.recipe import PythonRecipe


assert PythonRecipe.depends == ['python3']
assert PythonRecipe.python_depends == []


class Blake3Recipe(PythonRecipe):
    # 0.4.1 is the last CFFI-based release (no Rust toolchain required).
    # Later releases (≥ 1.0.0) require Rust and cannot currently be
    # cross-compiled for Android in the p4a environment.
    version = "0.4.1"
    sha512sum = "3c08e6bec2d69d6e7ce57dde3f8428f0d1b40f596b38a979f4a2f930061f14067f5675b4f74207d4bcccc4dda6b49f79cf48093d50a6b625e9bbebacecdf77ce"
    url = "https://files.pythonhosted.org/packages/b0/8d/43eafa8a785547c33b611068ffd6d914f5c5f96637d5b453abc556f095a0/blake3-{version}.tar.gz"
    depends = ["setuptools", "cffi"]

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
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


recipe = Blake3Recipe()
