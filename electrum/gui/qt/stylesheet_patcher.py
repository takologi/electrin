"""This is used to patch the QApplication style sheet.
It reads the current stylesheet, appends our modifications and sets the new stylesheet.

Note: since we switched from qdarkstyle CSS to Fusion + dark QPalette,
the dark-theme patch is no longer needed (native widget geometry is
preserved).  Only the macOS StatusBarButton patch remains.
"""

import sys

from PyQt6 import QtWidgets

CUSTOM_PATCH_FOR_DEFAULT_THEME_MACOS = '''
/* On macOS, main window status bar icons have ugly frame (see #6300) */
StatusBarButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    margin: 0px;
    padding: 2px;
}
StatusBarButton:checked {
  background-color: transparent;
  border: 1px solid #1464A0;
}
StatusBarButton:checked:disabled {
  border: 1px solid #14506E;
}
StatusBarButton:pressed {
  margin: 1px;
  background-color: transparent;
  border: 1px solid #1464A0;
}
StatusBarButton:disabled {
  border: none;
}
StatusBarButton:hover {
  border: 1px solid #148CD2;
}
'''


def patch_qt_stylesheet(use_dark_theme: bool) -> None:
    custom_patch = ""
    if not use_dark_theme and sys.platform == 'darwin':
        custom_patch = CUSTOM_PATCH_FOR_DEFAULT_THEME_MACOS
    if custom_patch:
        app = QtWidgets.QApplication.instance()
        style_sheet = app.styleSheet() + custom_patch
        app.setStyleSheet(style_sheet)
