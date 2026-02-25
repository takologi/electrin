#!/bin/bash
#
# Build release binaries for all platforms (sequential).
#
# Platforms built:
#   1. Linux sdist (source tarball)
#   2. Linux AppImage
#   3. Windows .exe (via Wine in Docker)
#   4. Android APK (arm64-v8a, release-unsigned)
#
# Usage:
#   ./contrib/release_build.sh [--no-cache] [--skip-android] [--android-password=PASSWORD]
#
# env vars respected by the individual build scripts:
#   ELECBUILD_NOCACHE  – force rebuild of docker images
#   ELECBUILD_COMMIT   – do a fresh clone + checkout (reproducible build)

set -e

PROJECT_ROOT="$(dirname "$(readlink -e "$0")")/.."
cd "$PROJECT_ROOT"

. "$PROJECT_ROOT/contrib/build_tools_util.sh"

# ── parse flags ──────────────────────────────────────────────────
SKIP_ANDROID=0
ANDROID_KEYSTORE_PASSWD=""
for arg in "$@"; do
    case "$arg" in
        --no-cache)
            export ELECBUILD_NOCACHE=1
            info "ELECBUILD_NOCACHE enabled — docker images will be rebuilt from scratch."
            ;;
        --skip-android)
            SKIP_ANDROID=1
            info "Skipping Android build."
            ;;
        --android-password=*)
            ANDROID_KEYSTORE_PASSWD="${arg#*=}"
            ;;
        *)
            fail "Unknown flag: $arg\nUsage: $0 [--no-cache] [--skip-android] [--android-password=PASSWORD]"
            ;;
    esac
done

# ── pre-flight checks ───────────────────────────────────────────
info "=== Electrin release build ==="

VERSION=$(python3 -c "exec(open('electrum/version.py').read()); print(ELECTRUM_VERSION)")
info "Building version: $VERSION"

if ! command -v docker &>/dev/null; then
    fail "docker is not installed or not in PATH."
fi

if [ -n "$(git status --porcelain)" ]; then
    warn "Working tree is not clean. Builds will use the current (dirty) tree."
fi

# ── clean caches ─────────────────────────────────────────────────
info "Cleaning build caches…"
rm -rf contrib/build-wine/tmp/
rm -rf contrib/build-wine/build/
rm -rf contrib/build-wine/.cache/
rm -rf contrib/build-wine/dist/
rm -rf contrib/build-linux/appimage/build/
rm -rf contrib/build-linux/appimage/.cache/
rm -rf contrib/build-linux/sdist/build/
rm -rf contrib/android/.cache/
rm -rf Electrin.egg-info/ Electrum.egg-info/ *.egg-info/
find . -type d -name __pycache__ -not -path './.venv*' -exec rm -rf {} + 2>/dev/null || true
rm -rf dist/
mkdir -p dist

# ── 1. sdist ─────────────────────────────────────────────────────
info ""
info "═══════════════════════════════════════════"
info "  [1/4]  Linux source distribution (sdist)"
info "═══════════════════════════════════════════"
contrib/build-linux/sdist/build.sh

# The sdist build touches all file timestamps (find -exec touch), which makes
# git report the tree as dirty. Restore before subsequent builds.
info "Restoring file timestamps after sdist build…"
git checkout . 2>/dev/null || true
git submodule foreach --recursive git checkout . 2>/dev/null || true

# ── 2. AppImage ──────────────────────────────────────────────────
info ""
info "═══════════════════════════════════════════"
info "  [2/4]  Linux AppImage"
info "═══════════════════════════════════════════"
contrib/build-linux/appimage/build.sh

# AppImage build also touches timestamps inside the mounted volume. Restore.
info "Restoring file timestamps after AppImage build…"
git checkout . 2>/dev/null || true
git submodule foreach --recursive git checkout . 2>/dev/null || true

# ── 3. Windows ───────────────────────────────────────────────────
info ""
info "═══════════════════════════════════════════"
info "  [3/4]  Windows .exe (Wine)"
info "═══════════════════════════════════════════"
contrib/build-wine/build.sh

# ── 4. Android ───────────────────────────────────────────────────
if [ "$SKIP_ANDROID" -eq 0 ]; then
    info ""
    info "═══════════════════════════════════════════"
    info "  [4/4]  Android APK (arm64-v8a)"
    info "═══════════════════════════════════════════"
    if [ -f "$HOME/.keystore" ]; then
        if [ -n "$ANDROID_KEYSTORE_PASSWD" ]; then
            contrib/android/build.sh qml arm64-v8a release "$ANDROID_KEYSTORE_PASSWD"
        else
            warn "~/.keystore found but no password provided. Use --android-password=PASSWORD"
            warn "Building release-unsigned APK instead."
            contrib/android/build.sh qml arm64-v8a release-unsigned
        fi
    else
        warn "~/.keystore not found — building release-unsigned APK."
        warn "To create a keystore:  keytool -genkey -v -keystore ~/.keystore -alias electrin -keyalg RSA -keysize 2048 -validity 10000"
        contrib/android/build.sh qml arm64-v8a release-unsigned
    fi
else
    info ""
    info "═══════════════════════════════════════════"
    info "  [4/4]  Android — SKIPPED"
    info "═══════════════════════════════════════════"
fi

# ── collect outputs ──────────────────────────────────────────────
info ""
info "═══════════════════════════════════════════"
info "  Build complete!  Artifacts in dist/:"
info "═══════════════════════════════════════════"

# Windows .exe ends up under contrib/build-wine/dist/, copy to dist/
if ls contrib/build-wine/dist/*.exe 1>/dev/null 2>&1; then
    cp -v contrib/build-wine/dist/*.exe dist/
fi

ls -lh dist/
info "Done."
