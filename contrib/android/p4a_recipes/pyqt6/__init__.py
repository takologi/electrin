import os
import shutil

from pythonforandroid.recipes.pyqt6 import PyQt6Recipe
from pythonforandroid.logger import info
from pythonforandroid.util import load_source

util = load_source('util', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'util.py'))


assert PyQt6Recipe._version == "6.10.1"
assert PyQt6Recipe.depends == ['qt6', 'pyjnius', 'setuptools', 'pyqt6sip', 'hostpython3', 'python3'], PyQt6Recipe.depends
assert PyQt6Recipe.python_depends == []


class PyQt6RecipePinned(util.InheritedRecipeMixin, PyQt6Recipe):
    sha512sum = "af9bb54b20fd177cf1dac5fe8fb0ff289e1e7e42716d09093d49dd99a7d8065c6b6f34784ed19e21e7e07ba0d550b270cb6be7273f7180e2bf886160fc773d01"

    def postbuild_arch(self, arch):
        """Fix sip-install creating an uppercase-named install directory.

        sip-install ignores the case of target-dir and installs PyQt6
        bindings (QtCore.abi3.so, QtQml.abi3.so, etc.) into a directory
        named after the project title (e.g. 'Electrin') instead of the
        dist name (e.g. 'electrin'). The packaging step reads from the
        lowercase directory, so the .abi3.so files are missing from the APK.

        This copies any files from the uppercase dir that are missing
        in the lowercase dir.
        """
        super().postbuild_arch(arch)

        install_dir = self.ctx.get_python_install_dir(arch.arch)  # .../electrin/arm64-v8a
        parent_dir = os.path.dirname(install_dir)  # .../python-installs/<dist_name>
        grandparent_dir = os.path.dirname(parent_dir)  # .../python-installs

        dist_name = os.path.basename(parent_dir)
        # Look for a case-mismatched sibling directory (e.g. 'Electrin' vs 'electrin')
        if os.path.isdir(grandparent_dir):
            for entry in os.listdir(grandparent_dir):
                entry_path = os.path.join(grandparent_dir, entry)
                if (entry.lower() == dist_name.lower()
                        and entry != dist_name
                        and os.path.isdir(entry_path)):
                    mismatched_dir = os.path.join(entry_path, arch.arch)
                    if not os.path.isdir(mismatched_dir):
                        continue
                    info(f"pyqt6: fixing case mismatch, copying from '{entry}' to '{dist_name}'")
                    # Walk the mismatched dir and copy missing files
                    for dirpath, dirnames, filenames in os.walk(mismatched_dir):
                        relpath = os.path.relpath(dirpath, mismatched_dir)
                        target_dirpath = os.path.join(install_dir, relpath)
                        os.makedirs(target_dirpath, exist_ok=True)
                        for filename in filenames:
                            src = os.path.join(dirpath, filename)
                            dst = os.path.join(target_dirpath, filename)
                            if not os.path.exists(dst):
                                info(f"  copying {os.path.join(relpath, filename)}")
                                shutil.copy2(src, dst)
                    break


recipe = PyQt6RecipePinned()
