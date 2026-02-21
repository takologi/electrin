import os
import shutil

from pythonforandroid.recipe import PythonRecipe


class Argon2CffiRecipe(PythonRecipe):
    # Pure Python wrapper around argon2-cffi-bindings.
    # argon2_cffi 25.1.0 uses pyproject.toml only (hatchling backend) so
    # PythonRecipe's default build_arch (which calls setup.py) fails.
    # We simply copy the src/argon2 tree into site-packages ourselves.
    version = "25.1.0"
    sha512sum = "746f4469cd9be79f4639f814bee99ddca71200a7bfb31c8f34ca88cc760ee73665fc0d4e46d50ca003911fcfab0dd153fd555ec6cb9127066c1e1e0fd63755b5"
    url = "https://files.pythonhosted.org/packages/0e/89/ce5af8a7d472a67cc819d5d998aa8c82c5d860608c4db9f46f1162d7dab9/argon2_cffi-{version}.tar.gz"
    depends = ["argon2_cffi_bindings"]

    def build_arch(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        install_dir = self.ctx.get_python_install_dir(arch.arch)
        src = os.path.join(build_dir, 'src', 'argon2')
        dst = os.path.join(install_dir, 'argon2')
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)


recipe = Argon2CffiRecipe()

