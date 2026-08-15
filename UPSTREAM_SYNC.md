# Upstream sync ledger

Electrin intentionally does not merge everything from upstream `spesmilo/electrum`. Lightning Network,
the NWC plugin, and LN-adjacent work (submarine swaps, anchor outputs, trampoline routing) are permanently
skipped — Rincoin has no Lightning support (`HAS_LIGHTNING = False`, see `CLAUDE.md`) and that whole
surface is dead code here. Because of that, **GitHub's "N commits behind" counter on this fork will never
trend to zero** — it counts raw commit reachability, not relevance, and upstream keeps adding Lightning
work we'll never take. That's expected, not a sign of neglect. What this file tracks instead is whether the
things that *do* matter are actually landing on a regular cadence.

## Policy

- **Security fixes: land immediately, ad hoc**, whenever noticed upstream — not batched into a sync pass.
  Small, standalone cherry-picks straight onto `master`, patch-released promptly.
- **Everything else relevant (bug fixes, wallet/core, tests, build): batched on a regular cadence.** No
  fixed interval is mandated here — match it to how often you're already touching the repo (monthly or
  quarterly is reasonable). Each pass re-runs the triage below against the *new* commits since the last
  pass, not the whole upstream history again.
- **Lightning core, NWC plugin, and LN-adjacent items are skipped without re-litigating each pass** — the
  policy is decided once (this file), not re-justified per commit.
- Each sync pass gets a dated entry below, appended, never overwritten — this file is the actual record of
  "we checked and here's what we decided," which is worth more than the raw diff-count badge.

### How to run a sync pass

```bash
git fetch upstream
git log --oneline <last-pass-anchor>..upstream/master   # new commits since last pass
```

Triage each new commit into:

1. **Immediately** — security/RPC hardening, or anything touching a file currently mid-refactor on a topic
   branch (land before that branch's work, to avoid rebasing around it later).
2. **Next batch, before the next release** — low-risk, non-urgent wallet/core/test fixes.
3. **Soon, can wait another release** — build/CI/packaging churn, isolated feature additions, no urgency.
4. **Needs its own decision** — Qt/QML styling churn (risks drifting from Electrin's branding, batch-review
   don't cherry-pick one at a time), Android/Qt-toolchain version bumps (conflict-prone against Electrin's
   custom RinHash/argon2/blake3 recipes — evaluate whether the bump is actually needed before touching it).
5. **Skip, not relevant** — Lightning/NWC/LN-adjacent (permanent policy), Bitcoin-specific chain
   data/checkpoints/server lists, upstream's own release-notes/docs.

Land buckets 1–3 as cherry-picks (`git cherry-pick -x <sha>` to keep the upstream SHA traceable in the
message). **Inspect the conflict before resolving one, even for "simple" commits** — `rincoin-bootstrap`
has skipped long runs of intervening upstream commits to the same files, so a 3-way merge can conflict even
when Electrin's side is just an older, otherwise-unmodified version of the file (see the `d34129ef` note in
Sync pass #1 below for a concrete example). Don't force a resolution you can't verify by reading the
result.

---

## Sync pass #1 — 2026-08-15

**Scope**: `rincoin-bootstrap..upstream/master` at the time of this audit — 351 commits (upstream base
`4.7.0` + 69 commits at fork point; upstream head at `b9be9749`). This pass is a first full audit of that
entire backlog, not an incremental one — future passes should be incremental against this date.

**Already landed**: ~85 of the 351 were already cherry-picked onto `rincoin-bootstrap` prior to this audit
(matched by commit-subject heuristic against `git log upstream/master..rincoin-bootstrap`, not a content
diff — treat as a strong starting point, not a guarantee; a future pass could re-verify with an actual diff
if it matters). This includes **every non-Lightning "mandatory" security item** found in the backlog: BIP70
removal, RPC-server lockdown (GUI-mode minimal RPC, `setconfig` rpcserver lock, restrictive unix-socket
permissions and umask), the CVE-2012-2459 verifier fix, and encrypting the keystore before adding it to the
wallet DB.

### Bucket 1 — land immediately (before the KDF seed-interop work)

Hand-picked, not mechanical — each one touches a file the in-flight KDF seed-interop effort is about to
modify:

- Stale SLIP-44 TODO in `constants.py` — resolved this pass (commit `84a135600`).
- **`d34129ef` "qml: deduplicate wallet name validation"** — **attempted and reverted this pass.** Touches
  `gui/qml/qewizard.py` and `gui/qml/components/wizard/WCWalletName.qml`, exactly the QML wizard files the
  KDF work will extend. The cherry-pick conflicts because it depends on a wallet-rename UI section in
  `WalletDetails.qml` that Electrin's copy doesn't have at all (never received the upstream commit that
  added it) — forcing the merge would have silently duplicated/corrupted that file. Needs a real look at
  why that upstream feature was never ported, not a blind conflict resolution. Left as bucket 4 until
  someone investigates the gap.
- Version-identity work (`ELECTRIN_VERSION`/`ELECTRUM_VERSION` split) — done this pass, not itself an
  upstream commit, but sequenced here because Stage 5 of the KDF plan bumps the wallet-file format version
  and should land on the real scheme, not the old placeholder string.

### Bucket 2 — after KDF, before the next release

Nothing here blocks KDF; land it once that work is merged, to harden the same files while still fresh:

- Re-verify the ~85 "already landed" matches above with an actual diff, not just subject-line matching.
- `a5f1a299` (regex literal-pipe fix), `b3808b79` (`GET_MASTER_FINGERPRINT` for hardware-wallet clients —
  relevant if a hardware wallet ever pairs with a KDF-HD-recovered Electrin wallet).
- Tests supporting the KDF test-oracle work (`toyserver` infra, `wallet_db` upgrader tests) — see the
  KDF plan's Stage 7.

### Bucket 3 — soon, can wait for another release

No interaction with KDF's files, no urgency:

| SHA | Subject | Category | Importance | Action |
|---|---|---|---|---|
| `0e7f7b30` | locale: rm llm_proofreader directory during build | Build / CI / packaging | optional | manual-port |
| `88f9c49a` | ci: add claude code code review | Build / CI / packaging | optional | manual-port |
| `85ea6af5` | ci: llm sec review: tweak trigger types | Build / CI / packaging | optional | manual-port |
| `1ba31448` | ci: bump code review ci claude version 4.6 -> 4.7 | Build / CI / packaging | optional | manual-port |
| `8e49eb80` | appimage: update Dockerfile dependencies | Build / CI / packaging | optional | manual-port |
| `44570bfa` | Bump minimum required version of ledger_bitcoin (build-time and runtime) | Build / CI / packaging | optional | manual-port |
| `1096ebcd` | build: update pinned ledger-bitcoin (partial rerun freeze_packages) | Build / CI / packaging | optional | manual-port |
| `0c52a01a` | ci: code review: pass commit messages into prompt context | Build / CI / packaging | optional | manual-port |
| `8c5af52c` | test_checksum_non_ascii | Tests only | optional | cherry-pick |
| `907ceb9f` | tests: timelock_recovery plugin: add test vector for checksum from bip | Tests only | optional | cherry-pick |
| `37159e47` | qml: 2fa: make it possible to copy 2fa secret | Wallet/core non-LN | optional | manual-port |
| `e71616e6` | update release notes for version 4.7.2 | Wallet/core non-LN | optional | cherry-pick |
| `a5f1a299` | pi: don't match literal \| char in regexes | Wallet/core non-LN | optional | cherry-pick |
| `b3808b79` | Using GET_MASTER_FINGERPRINT for Legacy Client to get the root public key fingerprint | Wallet/core non-LN | optional | cherry-pick |

Also two more from the `timelock_recovery` BIP-128 checksum cluster (`2f3f397a`, `c2f37294`) — real
correctness fix for a real (non-LN) plugin, low urgency; confirm the plugin is actually enabled for Rincoin
before scheduling.

### Bucket 4 — needs its own decision

- **`d34129ef`** (see Bucket 1 note above) — investigate the missing `WalletDetails.qml` rename-UI feature
  before deciding whether to port it.
- **The Android/Qt6.10/NDK28/p4a rebase wave** (`dba6b751`, `4d55b049`, `42472a1e`, `cdb5c0b8`, `32318987`,
  `74f3c042`, `854f95b7`, `c8f5798d`, `9d5b4a7c`, `7b7d7028`, `29b5e167`, `83b67700`, `96a3345a`, and
  related) — conflict-prone against Electrin's custom `blake3`/`argon2-cffi` p4a recipes. Decide whether
  Electrin actually needs Qt6.10 (e.g. Android-8-minimum-API compliance) before touching this; don't adopt
  it reflexively.
- **General Qt/QML styling and UX churn** — button-container refactors, dialog restyling, icon touch-ups,
  roughly 40 commits (see the full 351-commit source triage referenced below for the complete list — not
  reproduced here to keep this section scannable). Batch-review on its own schedule rather than
  cherry-picking individually; risks drifting from Electrin's Rincoin-branded theme one commit at a time.

### Bucket 5 — skip, not relevant

By category, with a few representative examples (not the full list — the point of this bucket is that it
doesn't need re-reading each pass):

- **Lightning core** (64) — e.g. `ddb01f53` lnpeer, `0b2c7a8a` lnsweep, and the rest of `electrum/lnworker.py`
  / `lnpeer.py` / `lnchannel.py` churn. Dead code path, `HAS_LIGHTNING = False`.
- **NWC plugin** (13) — e.g. `4c703ea2`, `0dc08fdf`. Requires Lightning; same reason.
- **LN-adjacent, miscategorized elsewhere** (~10) — submarine swaps (`88c7a731`, `022a1bf0`, `c4dcd85a`),
  LN RPC commands (`46803695` list_channels, `5a5c1e1f` list_channel_htlcs, `3399c20a`
  export_lightning_preimage), LN test suites (`db003257`, `e309f89a`, and the rest of `test_lnpeer.py`/
  `test_onion_message.py`/`test_lnrouter.py`). Same reason, despite upstream's own category labels.
- **Chain data / servers** (3) — Bitcoin checkpoint updates, personal `servers.json` entries. Not
  applicable; Rincoin's server list is Fulcrum-rin-based.
- **Docs / release notes** (7) — Electrum-branded release notes, not Electrin's.
- **All merge commits** (94) — no content of their own.

---

## Reference

The complete commit-by-commit triage this pass was built from (all 351 rows, with the original
category/effort/confidence columns) is preserved in git history at
`UPSTREAM_MERGE_TRIAGE_RINCOIN_BOOTSTRAP.md` — recovered from a stray `origin/master` state during this
pass; see `git log --all -- UPSTREAM_MERGE_TRIAGE_RINCOIN_BOOTSTRAP.md` if the original per-commit detail
is needed for a specific SHA not called out above.
