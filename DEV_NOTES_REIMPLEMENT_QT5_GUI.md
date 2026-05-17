# Qt5-era UX tweaks lost during Qt6 upstream merge

During the upstream merge of `cdc2ae34..b9be9749` (Electrum master, May 2026),
we accepted upstream Qt6 / Qt6.10 commits as-is in cases where they replaced
Qt code that contained our custom UX improvements. The goal of this file is
to record what we lost, so we can re-implement these UX improvements on top
of the Qt6 baseline as a separate workstream.

For each item: what we lost, why upstream change took priority, and a hint
on where to re-port the fix.

---

## Conventions

- **File**: path of the upstream/Electrin file where the original tweak lived.
- **Lost in commit**: upstream SHA that overwrote our change.
- **Original rincoin commit**: SHA in `rincoin-bootstrap` history that introduced our tweak.
- **Re-port hint**: how to add it back on the new Qt6 code.

---

## (entries appended as the merge progresses)

### Constants.qml — `notificationBackground` light-theme lightness
- **File**: `electrum/gui/qml/components/Constants.qml`
- **Lost in commit**: upstream `9772a6d5` and `cdb5c0b8` (Qt6.10 styling refactors)
- **Original rincoin commit**: pre-merge baseline used `Qt.lighter(Material.background, isDark ? 1.5 : 0.92)` to make notifications readable on light theme.
- **Status**: RE-APPLIED during conflict resolution. Kept the `isDark ? 1.5 : 0.92` conditional on top of upstream's `dialogColor`/`seedTextAreaBackground` additions. No re-port needed unless future Qt upstream replaces this line again.
