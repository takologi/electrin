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


recipe = Argon2CffiBindingsRecipe()
