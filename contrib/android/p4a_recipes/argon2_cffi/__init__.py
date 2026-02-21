from pythonforandroid.recipe import PythonRecipe


assert PythonRecipe.depends == ['python3']
assert PythonRecipe.python_depends == []


class Argon2CffiRecipe(PythonRecipe):
    # Pure Python wrapper around argon2-cffi-bindings.
    # Wheel is py3-none-any; no C compilation required.
    version = "25.1.0"
    sha512sum = "746f4469cd9be79f4639f814bee99ddca71200a7bfb31c8f34ca88cc760ee73665fc0d4e46d50ca003911fcfab0dd153fd555ec6cb9127066c1e1e0fd63755b5"
    url = "https://files.pythonhosted.org/packages/0e/89/ce5af8a7d472a67cc819d5d998aa8c82c5d860608c4db9f46f1162d7dab9/argon2_cffi-{version}.tar.gz"
    depends = ["argon2_cffi_bindings"]
    # No setuptools: build backend is hatchling (bundled by pip in >= 23.x)


recipe = Argon2CffiRecipe()
