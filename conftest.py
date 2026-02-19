"""
Root pytest configuration for Electrum-RIN.

Allows the non-GUI core test suite to run on headless CI environments
where PyQt6 is not installed. QML tests are silently excluded at
collection time rather than aborting the run with import errors.
"""

# collect_ignore_glob is evaluated before pytest collects any files,
# so it prevents ImportError during collection rather than at run time.
collect_ignore_glob = []

try:
    import PyQt6  # noqa: F401
except ImportError:
    collect_ignore_glob.append("tests/test_qml*.py")
