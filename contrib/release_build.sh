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
#   ./contrib/release_build.sh --release|--debug --dist-clean=none|selected|all [--dry-run] [--no-cache] [--allow-dirty] [--android-password=PASSWORD]
#                              [--skip-sdist] [--skip-appimage] [--skip-windows] [--skip-android]
#   ./contrib/release_build.sh --help
#
# env vars respected by the individual build scripts:
#   ELECBUILD_NOCACHE  – force rebuild of docker images
#   ELECBUILD_COMMIT   – do a fresh clone + checkout (reproducible build)

set -e

PROJECT_ROOT="$(dirname "$(readlink -e "$0")")/.."
cd "$PROJECT_ROOT"

. "$PROJECT_ROOT/contrib/build_tools_util.sh"

print_help() {
        cat <<'EOF'
Electrin release build helper

Usage:
    ./contrib/release_build.sh --release --dist-clean=none|selected|all [options]
    ./contrib/release_build.sh --debug --dist-clean=none|selected|all [options]
    ./contrib/release_build.sh --help

Modes (mandatory: choose exactly one):
    --release                Run release build flow (current implementation)
    --debug                  Placeholder only (TODO, currently fails intentionally)

General options:
    --help, -h               Show this help and exit
    --dry-run                Print selected mode/targets/options and exit (no build)
    --dist-clean=MODE        Mandatory. Dist cleanup strategy before build:
                             - none: keep all existing dist/ artifacts
                             - selected: remove only artifacts for enabled targets
                             - all: remove whole dist/ directory
    --no-cache               Rebuild docker images from scratch (ELECBUILD_NOCACHE=1)
    --allow-dirty            Allow builds with uncommitted git changes
    --android-password=PASS  Android keystore password (release mode)

Platform selection options:
    --skip-sdist             Skip Linux source tarball build
    --skip-appimage          Skip Linux AppImage build
    --skip-windows           Skip Windows build
    --skip-android           Skip Android build

Examples:
    # Build everything in release mode
    ./contrib/release_build.sh --release --dist-clean=selected --android-password=YOUR_PASSWORD

    # Build only Linux AppImage + Android
    ./contrib/release_build.sh --release --dist-clean=selected --skip-sdist --skip-windows --android-password=YOUR_PASSWORD

    # Build only AppImage
    ./contrib/release_build.sh --release --dist-clean=selected --skip-sdist --skip-windows --skip-android

    # Show what would run without starting builds
    ./contrib/release_build.sh --release --dist-clean=none --dry-run --skip-sdist --skip-windows

    # Keep all existing artifacts explicitly
    ./contrib/release_build.sh --release --dist-clean=none --skip-sdist --skip-windows

    # Show help
    ./contrib/release_build.sh --help
EOF
}

# ── parse flags ──────────────────────────────────────────────────
SKIP_SDIST=0
SKIP_APPIMAGE=0
SKIP_WINDOWS=0
SKIP_ANDROID=0
ALLOW_DIRTY=0
DRY_RUN=0
DIST_CLEAN=""
BUILD_MODE_RELEASE=0
BUILD_MODE_DEBUG=0
ANDROID_KEYSTORE_PASSWD=""
for arg in "$@"; do
    case "$arg" in
                --help|-h)
                        print_help
                        exit 0
                        ;;
                --release)
                        BUILD_MODE_RELEASE=1
                        ;;
                --debug)
                        BUILD_MODE_DEBUG=1
                        ;;
        --dry-run)
            DRY_RUN=1
            ;;
        --dist-clean=*)
            DIST_CLEAN="${arg#*=}"
            ;;
        --no-cache)
            export ELECBUILD_NOCACHE=1
            info "ELECBUILD_NOCACHE enabled — docker images will be rebuilt from scratch."
            ;;
        --skip-sdist)
            SKIP_SDIST=1
            info "Skipping Linux source distribution (sdist) build."
            ;;
        --skip-appimage)
            SKIP_APPIMAGE=1
            info "Skipping Linux AppImage build."
            ;;
        --skip-windows)
            SKIP_WINDOWS=1
            info "Skipping Windows build."
            ;;
        --skip-android)
            SKIP_ANDROID=1
            info "Skipping Android build."
            ;;
        --allow-dirty)
            ALLOW_DIRTY=1
            warn "ALLOW_DIRTY enabled — build will proceed with uncommitted changes."
            ;;
        --android-password=*)
            ANDROID_KEYSTORE_PASSWD="${arg#*=}"
            ;;
        *)
            print_help
            fail "Unknown flag: $arg"
            ;;
    esac
done

if [ "$BUILD_MODE_RELEASE" -eq 1 ] && [ "$BUILD_MODE_DEBUG" -eq 1 ]; then
    print_help
    fail "Choose exactly one mode: --release or --debug (not both)."
fi

if [ "$BUILD_MODE_RELEASE" -eq 0 ] && [ "$BUILD_MODE_DEBUG" -eq 0 ]; then
    print_help
    fail "Missing mandatory mode flag: use --release or --debug."
fi

if [ -z "$DIST_CLEAN" ]; then
    print_help
    fail "Missing mandatory --dist-clean flag. Recommended: --dist-clean=none"
fi

if [ "$DIST_CLEAN" != "none" ] && [ "$DIST_CLEAN" != "selected" ] && [ "$DIST_CLEAN" != "all" ]; then
    print_help
    fail "Invalid --dist-clean value '$DIST_CLEAN'. Allowed: none, selected, all."
fi

if [ "$BUILD_MODE_DEBUG" -eq 1 ]; then
    fail "TODO: --debug mode is not implemented yet."
fi

if [ "$SKIP_SDIST" -eq 1 ] && [ "$SKIP_APPIMAGE" -eq 1 ] && [ "$SKIP_WINDOWS" -eq 1 ] && [ "$SKIP_ANDROID" -eq 1 ]; then
    fail "All build targets are skipped. Enable at least one target."
fi

if [ "$DRY_RUN" -eq 1 ]; then
    info "Dry-run mode enabled. No builds will be started."
    info "Mode: release"
    info "Targets:"
    info "  - Linux sdist: $([ "$SKIP_SDIST" -eq 0 ] && echo ENABLED || echo SKIPPED)"
    info "  - Linux AppImage: $([ "$SKIP_APPIMAGE" -eq 0 ] && echo ENABLED || echo SKIPPED)"
    info "  - Windows: $([ "$SKIP_WINDOWS" -eq 0 ] && echo ENABLED || echo SKIPPED)"
    info "  - Android: $([ "$SKIP_ANDROID" -eq 0 ] && echo ENABLED || echo SKIPPED)"
    info "Options:"
    info "  - dist-clean: $DIST_CLEAN"
    info "  - allow-dirty: $([ "$ALLOW_DIRTY" -eq 1 ] && echo YES || echo NO)"
    info "  - no-cache: $([ -n "$ELECBUILD_NOCACHE" ] && echo YES || echo NO)"
    if [ -n "$ANDROID_KEYSTORE_PASSWD" ]; then
        info "  - android-password: PROVIDED"
    else
        info "  - android-password: NOT PROVIDED"
    fi
    exit 0
fi

restore_git_tree() {
    info "Restoring git/submodule working tree…"
    git checkout . 2>/dev/null || true
    git submodule foreach --recursive git checkout . 2>/dev/null || true
    git submodule update --init --recursive 2>/dev/null || true
}

# ── pre-flight checks ───────────────────────────────────────────
info "=== Electrin release build ==="

VERSION=$(python3 -c "exec(open('electrum/version.py').read()); print(ELECTRIN_VERSION)")
info "Building version: $VERSION"

if ! command -v docker &>/dev/null; then
    fail "docker is not installed or not in PATH."
fi

GIT_STATUS="$(git status --porcelain)"
if [ -n "$GIT_STATUS" ]; then
    warn "Working tree is not clean before build."
    warn "First dirty entries:"
    echo "$GIT_STATUS" | sed -n '1,20p'

    # Friendly hint: this can be caused by submodule modified content (e.g. locale *.po deleted by prior build).
    if echo "$GIT_STATUS" | grep -qE '^.[[:space:]]+electrum/locale$|electrum/locale'; then
        warn "Detected locale submodule dirtiness. This often happens after Android/AppImage build removes *.po files."
        warn "Fix now with: git submodule update --init --recursive && git -C electrum/locale reset --hard && git -C electrum/locale clean -ffxd"
    fi

    if [ "$ALLOW_DIRTY" -ne 1 ]; then
        fail "Refusing to start release build on dirty tree. Commit/stash/clean first, or rerun with --allow-dirty."
    fi
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
mkdir -p dist

case "$DIST_CLEAN" in
    all)
        info "Cleaning dist/ artifacts: mode=all"
        rm -rf dist/
        mkdir -p dist
        ;;
    selected)
        info "Cleaning dist/ artifacts: mode=selected"
        if [ "$SKIP_SDIST" -eq 0 ]; then
            rm -f dist/*.tar.gz
        fi
        if [ "$SKIP_APPIMAGE" -eq 0 ]; then
            rm -f dist/*.AppImage
        fi
        if [ "$SKIP_WINDOWS" -eq 0 ]; then
            rm -f dist/*.exe
        fi
        if [ "$SKIP_ANDROID" -eq 0 ]; then
            rm -f dist/*android*.apk dist/*-arm64-v8a*.apk
        fi
        ;;
    none)
        info "Cleaning dist/ artifacts: mode=none (keeping existing dist/ files)"
        ;;
esac

# ── 1. sdist ─────────────────────────────────────────────────────
if [ "$SKIP_SDIST" -eq 0 ]; then
    info ""
    info "═══════════════════════════════════════════"
    info "  [1/4]  Linux source distribution (sdist)"
    info "═══════════════════════════════════════════"
    contrib/build-linux/sdist/build.sh

    # The sdist build touches all file timestamps (find -exec touch), which makes
    # git report the tree as dirty. Restore before subsequent builds.
    info "Restoring file timestamps after sdist build…"
    restore_git_tree
else
    info ""
    info "═══════════════════════════════════════════"
    info "  [1/4]  Linux source distribution (sdist) — SKIPPED"
    info "═══════════════════════════════════════════"
fi

# ── 2. AppImage ──────────────────────────────────────────────────
if [ "$SKIP_APPIMAGE" -eq 0 ]; then
    info ""
    info "═══════════════════════════════════════════"
    info "  [2/4]  Linux AppImage"
    info "═══════════════════════════════════════════"
    contrib/build-linux/appimage/build.sh

    # AppImage build also touches timestamps inside the mounted volume. Restore.
    info "Restoring file timestamps after AppImage build…"
    restore_git_tree
else
    info ""
    info "═══════════════════════════════════════════"
    info "  [2/4]  Linux AppImage — SKIPPED"
    info "═══════════════════════════════════════════"
fi

# ── 3. Windows ───────────────────────────────────────────────────
if [ "$SKIP_WINDOWS" -eq 0 ]; then
    info ""
    info "═══════════════════════════════════════════"
    info "  [3/4]  Windows .exe (Wine)"
    info "═══════════════════════════════════════════"
    contrib/build-wine/build.sh
else
    info ""
    info "═══════════════════════════════════════════"
    info "  [3/4]  Windows .exe (Wine) — SKIPPED"
    info "═══════════════════════════════════════════"
fi

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

    # Android build writes to .buildozer_* paths by default; collect final APK into dist/.
    APK_PATH="$(find "$PROJECT_ROOT/.buildozer_qml" -type f \( -name 'electrin-release.apk' -o -name 'electrin-release-unsigned.apk' \) | sort | tail -n1)"
    if [ -z "$APK_PATH" ] || [ ! -f "$APK_PATH" ]; then
        fail "Android build completed but no APK was found under .buildozer_qml."
    fi
    cp -v "$APK_PATH" "dist/electrin-${VERSION}-android-arm64-v8a.apk"

    # Android build removes tracked locale .po files; restore for subsequent runs.
    info "Restoring working tree after Android build…"
    restore_git_tree
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
