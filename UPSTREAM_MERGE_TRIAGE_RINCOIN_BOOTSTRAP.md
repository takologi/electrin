# Upstream merge triage: `rincoin-bootstrap` vs `spesmilo/electrum:master`

Scope: commit-by-commit triage for `origin/rincoin-bootstrap..upstream/master` using policy: **aggressive merge overall**, **conservative for Qt GUI/QML**, with Qt6 reassessment.

- Provided comparison anchors: base `cdc2ae34eeaa767c3e862378f8a4de9f78aa6199` / head `b9be9749f61224d51c6c96ab6b693385b9904172`
- Commits triaged: **351**
- Qt6 migration signals detected: **yes** (8 commit(s) mention Qt6/PyQt6)

## Flag definitions
- Importance: `mandatory` / `optional` / `not relevant`
- Effort: `easy` / `moderate` / `difficult`
- Confidence: `high` / `medium` / `low`
- Recommended action: `cherry-pick` / `manual-port` / `skip`

## Category rationale and recommended posture
- **Security / RPC hardening**: prioritize as `mandatory`; port quickly, test daemon/RPC/auth paths.
- **NWC plugin**: treat auth/budget/encryption fixes as `mandatory` if plugin is shipped; otherwise optional.
- **Wallet/core non-LN**: aggressive merge default; cherry-pick low-risk fixes and manually port broader refactors.
- **Lightning core**: still high value, but conflict-prone; stage as manual ports unless isolated fixes are obvious.
- **Qt GUI / QML**: conservative by default. Qt6 migration is active upstream, so Qt6-compatibility items are retained in backlog but still not bulk-merged.
- **Build / CI / packaging**: merge selectively based on Electrin release pipeline needs.
- **Chain data / servers**: generally not relevant for Rincoin fork; skip unless structural tooling is needed.

## Summary counts
- Merge commits: 94
- Lightning core: 64
- Qt GUI / QML: 49
- Wallet/core non-LN: 38
- Build / CI / packaging: 33
- Tests only: 32
- Security / RPC hardening: 17
- NWC plugin: 13
- Docs / release notes: 8
- Chain data / servers: 3

Importance/Effort matrix:
- mandatory + difficult: 4
- mandatory + easy: 1
- mandatory + moderate: 19
- not relevant + easy: 10
- not relevant + moderate: 1
- optional + difficult: 85
- optional + easy: 139
- optional + moderate: 92

## Actionable merge plan (ordered waves)
1. **Wave 1 (mandatory, low/medium effort)**: cherry-pick security/RPC hardening and mandatory NWC fixes.
2. **Wave 2 (optional but high-leverage core)**: cherry-pick wallet/core non-LN fixes with easy conflict profile.
3. **Wave 3 (difficult mandatory/optional)**: manual-port complex Lightning and RPC/security-adjacent changes.
4. **Wave 4 (Qt GUI/QML)**: keep conservative; port only Qt6-readiness and clear bug/security fixes.
5. **Wave 5 (infra/build)**: apply only pipeline-relevant changes; skip unrelated platform packaging churn.
6. **Wave 6 (skip bucket)**: chain data/server lists and upstream-only housekeeping not applicable to Rincoin.

## Commit-by-commit triage

| SHA | Subject | Category | Importance | Effort | Confidence | Action |
|---|---|---|---|---|---|---|
| `319b73ec` | util: use FileNotFoundError for dangling symlink | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `f0fc8a96` | qt: add changelog action to help menu in toolbar | Qt GUI / QML | optional | difficult | high | skip |
| `99b0df0f` | contrib: android: Dockerfile: fix build user env | Build / CI / packaging | optional | difficult | high | manual-port |
| `202ea287` | contrib: android: Dockerfile: fix ownership of COPY | Build / CI / packaging | optional | difficult | high | manual-port |
| `73a03249` | wallet_db: handle non-existing parent_set_key in v65 | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `71a1e96d` | Merge pull request #10489 from f321x/fix_10487 | Merge commits | optional | easy | high | skip |
| `a1f1b393` | wallet_db: assert WalletDBUpgrader.storage is dict | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `53166cc0` | git: ignore changes to locale submodule | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `0e7f7b30` | locale: rm llm_proofreader directory during build | Build / CI / packaging | optional | easy | high | manual-port |
| `49f1eff1` | Merge pull request #10490 from f321x/locale_llm_proofreader_cleanup | Merge commits | optional | easy | high | skip |
| `6de3fef7` | (trivial) consistent whitespaces in .gitmodules | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `3afa2fcd` | locale: gui: show translation completion percentage in language names | Qt GUI / QML | optional | difficult | high | skip |
| `4d2ea4f2` | update locale | Chain data / servers | not relevant | easy | high | skip |
| `9a71382c` | Merge pull request #10479 from SomberNight/202602_locale_fancy_names | Merge commits | optional | easy | high | skip |
| `ddb01f53` | lnpeer: don't save our own channel update as remote upd | Lightning core | optional | moderate | high | manual-port |
| `2df68d92` | qt: console: allow changing font size | Qt GUI / QML | optional | difficult | high | skip |
| `cb972009` | Merge pull request #10494 from f321x/console_font_size | Merge commits | optional | easy | high | skip |
| `8427a11a` | Merge pull request #10493 from f321x/gossip_fix_save_remote_update | Merge commits | optional | easy | high | skip |
| `a9f20e4d` | wallet: rbf: estimate base tx size before stripping | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `6e1bf7c4` | test_wallet_vertical: add test for batch tx fee increase | Tests only | optional | easy | high | cherry-pick |
| `6c143fa9` | test_wallet_vertical: add test for dscancel fee estimate | Tests only | optional | easy | high | cherry-pick |
| `f1e792cc` | test_wallet_vertical: test bump_fee raises for too low fee | Tests only | optional | easy | high | cherry-pick |
| `e9ac3e93` | transaction: use dummy DER ECDSA sig from descriptor.py | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `3133148a` | transaction: extend estimated_size() docstring | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `6feb9927` | Merge pull request #10453 from f321x/debug_rbf_fee_calculation | Merge commits | optional | easy | high | skip |
| `0b2c7a8a` | lnsweep: safer maybe_reveal_preimage_for_htlc, add "is_preimage_public" | Lightning core | optional | difficult | high | manual-port |
| `10274c1c` | simplify prev | Lightning core | optional | moderate | high | manual-port |
| `9a41a547` | Merge pull request #10442 from SomberNight/202601_lnworker_is_preimage_public | Merge commits | optional | easy | high | skip |
| `9dc725fa` | deps: bump libsecp256k1 version (0.7.0->0.7.1) and electrum-ecc | Build / CI / packaging | optional | easy | high | manual-port |
| `2c9f4fdb` | Merge pull request #10433 from f321x/qt_changelog | Merge commits | optional | easy | high | skip |
| `d733350a` | lnwatcher: ~document behaviour re subbing to historical chans and swaps | Lightning core | optional | moderate | high | manual-port |
| `ff6f3738` | Merge pull request #10495 from SomberNight/202602_bump_secp | Merge commits | optional | easy | high | skip |
| `8d95135a` | add version 4.7.1 release notes | Docs / release notes | not relevant | easy | high | skip |
| `eee2e858` | bump version to 4.7.1 | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `67b4ebd8` | Merge pull request #10497 from f321x/version_4_7_1 | Merge commits | optional | easy | high | skip |
| `57bf8c89` | follow-up RELEASE-NOTES | Docs / release notes | not relevant | easy | high | skip |
| `d72b7411` | update block header checkpoints | Chain data / servers | not relevant | moderate | high | skip |
| `a36c9a24` | build: appimage: fix build missing a system-wide python | Build / CI / packaging | optional | easy | high | manual-port |
| `c4dcd85a` | txbatcher: don't spend anchors if ctx fee is sufficient | Wallet/core non-LN | optional | difficult | high | manual-port |
| `04a034e6` | tests: add unittest for TxBatch._to_sweep_after() | Tests only | optional | easy | high | cherry-pick |
| `b939e877` | build: win: update debian base (12->13) | Build / CI / packaging | optional | easy | high | manual-port |
| `3674232d` | build: win: bump wine (10->11) | Build / CI / packaging | optional | easy | high | manual-port |
| `ff44d4b4` | Merge pull request #10093 from f321x/anchor_output_sweeping_lower_fee | Merge commits | optional | easy | high | skip |
| `31ed05c0` | build: win: change from win-iconv to GNU libiconv | Build / CI / packaging | optional | moderate | high | manual-port |
| `f3ba25df` | qt: utxo_list: only enable 'fully spend...' menu if there are unfrozen coins in the selection. | Qt GUI / QML | optional | difficult | high | skip |
| `fe5cb09e` | wallet_db: convert PaymentInfo amounts from 0 to None | Lightning core | optional | moderate | high | manual-port |
| `161142dd` | Merge pull request #10502 from SomberNight/202603_lnworker_payment_infos_convert_amount | Merge commits | optional | easy | high | skip |
| `4c703ea2` | plugin: nwc: remove multi_pay_invoice rpc | NWC plugin | mandatory | difficult | high | manual-port |
| `0dc08fdf` | plugin: nwc: handle encryption scheme signaling | NWC plugin | mandatory | moderate | high | cherry-pick |
| `91efb3e1` | common_qt: move QtEventListener and qt_event_listener decorator to common_qt | Qt GUI / QML | optional | difficult | high | skip |
| `423cc678` | qt: MyTreeView: close menu if its context changes | Qt GUI / QML | optional | difficult | high | skip |
| `cbaa3a8b` | Merge pull request #10467 from f321x/fix_10464 | Merge commits | optional | easy | high | skip |
| `3956bff0` | plugin: nwc: do budget accounting in msat | NWC plugin | mandatory | moderate | high | cherry-pick |
| `52223740` | plugin: nwc: improved budget accounting | NWC plugin | mandatory | moderate | high | cherry-pick |
| `ea1e2c82` | plugin: nwc: add 'state' field to responses | NWC plugin | optional | moderate | high | cherry-pick |
| `835ab39d` | plugin: nwc: bump version to 0.0.2 | NWC plugin | optional | moderate | high | cherry-pick |
| `4c27b8de` | qt: utxo_list: add asserts to helper methods that coins are selected | Qt GUI / QML | optional | difficult | high | skip |
| `0cb4e89a` | Merge pull request #10503 from accumulator/qt_coins_fully_spend_menu | Merge commits | optional | easy | high | skip |
| `48916f56` | qt: perform 'fully spend' action with coin selection, keep separate from coin control when doing action. | Qt GUI / QML | optional | difficult | high | skip |
| `cb696ed6` | Merge pull request #10504 from accumulator/move_qt_event_listener | Merge commits | optional | easy | high | skip |
| `fd52b970` | Merge pull request #10505 from f321x/nwc_improvement | Merge commits | optional | easy | high | skip |
| `db003257` | tests: lnpeer: make mpp_cleanup_after_expiry more robust | Tests only | optional | easy | high | cherry-pick |
| `851781fb` | Merge pull request #10508 from SomberNight/202603_lnpeer_test_mpp_cleanup_more_robust | Merge commits | optional | easy | high | skip |
| `e309f89a` | test_lnpeer: factorize test_reestablish_replay_messages | Tests only | optional | easy | high | cherry-pick |
| `8dddb5d5` | plugin: nwc: unify budget_allows_spend and add_to_budget | NWC plugin | mandatory | moderate | high | cherry-pick |
| `8ccdc3f7` | plugin: nwc: consider routing fees for payment budget | NWC plugin | mandatory | moderate | high | cherry-pick |
| `9b4d4d61` | plugin: nwc: add update timer to connection list | NWC plugin | optional | moderate | high | cherry-pick |
| `f53203d1` | plugin: nwc: consider inflight htlcs in get_payment_info | NWC plugin | optional | moderate | high | cherry-pick |
| `f64923b4` | plugin: nwc: lookup_invoice: fix exc, include b11 | NWC plugin | optional | moderate | high | cherry-pick |
| `3695e00f` | Merge pull request #10511 from f321x/nwc_followup | Merge commits | optional | easy | high | skip |
| `e8eee065` | transaction: re-raise NetworkException in add_info_from_network | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `3d13d478` | qml: rbf/cancel: abort update if adding tx info fails | Qt GUI / QML | optional | difficult | high | skip |
| `d85985cd` | qml: rbf/cancel: fix type error | Qt GUI / QML | optional | difficult | high | skip |
| `601dda78` | Merge pull request #10514 from f321x/fix_bump_fee_exc | Merge commits | optional | easy | high | skip |
| `e31ce7dc` | Update my Electrum server details in servers.json | Chain data / servers | not relevant | easy | high | skip |
| `d112653e` | Merge pull request #10515 from jhoenicke/patch-1 | Merge commits | optional | easy | high | skip |
| `93f04524` | lnpeer: simplify where maybe_send_commitment() is called | Lightning core | optional | moderate | high | manual-port |
| `7e3af72a` | lnpeer: maybe_send_commitment: impl batching updates | Lightning core | optional | moderate | high | manual-port |
| `169227e1` | Merge pull request #10509 from SomberNight/202603_lnpeer_send_commitment | Merge commits | optional | easy | high | skip |
| `1c24c613` | tests: lnpeer: uncomment testcase: test_modern_shutdown_no_overlap | Tests only | optional | easy | high | cherry-pick |
| `27a94ff5` | Merge pull request #10517 from SomberNight/202603_test_lnpeer_modern_shutdown | Merge commits | optional | easy | high | skip |
| `2f3f397a` | Fix checksum following BIP-128 standard | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `8c5af52c` | test_checksum_non_ascii | Tests only | optional | easy | high | cherry-pick |
| `907ceb9f` | tests: timelock_recovery plugin: add test vector for checksum from bip | Tests only | optional | easy | high | cherry-pick |
| `c2f37294` | plugins: timelock_recovery: move checksum func to base class | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `e4ad44c0` | Merge branch '202603_timelock_recovery_plugin_checksum': fix checksum calc | Docs / release notes | not relevant | easy | high | skip |
| `b397ddb0` | tests: move revealer and timelock_recovery stuff to tests/plugins/ | Tests only | optional | moderate | high | cherry-pick |
| `d6ec34a8` | Merge pull request #10527 from SomberNight/202603_tests_plugins | Merge commits | optional | easy | high | skip |
| `ffd25928` | qt: SwapServerDialog: resize server list with dialog | Qt GUI / QML | optional | difficult | high | skip |
| `88c7a731` | swaps: rm until filter when fetching server pairs | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `44e99bc1` | tests: move qml stuff to tests/qml/ | Tests only | optional | difficult | high | manual-port |
| `66ee2185` | Merge pull request #10529 from SomberNight/202603_tests_qml | Merge commits | optional | easy | high | skip |
| `022a1bf0` | swapserver: cli: skip pending swaps in history commands | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `efca1cc5` | qt: PluginsDialog: add link to website | Qt GUI / QML | optional | difficult | high | skip |
| `edc70867` | Merge pull request #10530 from f321x/plugins_website | Merge commits | optional | easy | high | skip |
| `558f8529` | trampoline: allow trampoline onion packets of arbitrary size | Lightning core | optional | difficult | high | manual-port |
| `f56e6318` | swaps: make SwapManager.percentage Decimal | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `7ee2477b` | Merge pull request #10528 from f321x/qt_swapserver_list_resize | Merge commits | optional | easy | high | skip |
| `46803695` | add more options to list_channels | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `01d017cd` | follow-up #10442 | Lightning core | optional | moderate | high | manual-port |
| `b19820dc` | adb.get_spender: subscribe to outputs explicitly, instead of as a side effect | Lightning core | optional | moderate | high | manual-port |
| `dea8d3e1` | Merge pull request #10500 from SomberNight/202602_win_build | Merge commits | optional | easy | high | skip |
| `03e95acc` | qt, qml: for new transaction notifications, instead of using sign, explicitly say sent/received. For multiple transactions, split summary in total sent/received and a balance change. | Qt GUI / QML | optional | difficult | high | skip |
| `2ea8d115` | fixup prev | Qt GUI / QML | optional | moderate | high | skip |
| `8f21f1d7` | Merge pull request #10507 from accumulator/new_txs_notify_summary | Merge commits | optional | easy | high | skip |
| `dceece1c` | mv os.urandom sanity check to main __init__.py | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `fa6deb8d` | interface.py: rm dead code | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `baf9a1d9` | interface.py: rm broken dead code | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `42ad18b2` | rm bip70 support | Security / RPC hardening | mandatory | difficult | high | manual-port |
| `3e3f595e` | pem.py, x509.py: rm unused code | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `64dab5ef` | Merge pull request #10535 from SomberNight/202603_rm_bip70 | Merge commits | optional | easy | high | skip |
| `89da2a3b` | Merge pull request #10533 from spesmilo/adb_subscribe_to_outputs | Merge commits | optional | easy | high | skip |
| `543b73be` | wizard: catch NotLegacySinglesigScriptType | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `2c541d26` | qt: ElectrumGui: repr(UserFacingException) -> str() | Qt GUI / QML | optional | difficult | high | skip |
| `3c62bf73` | Merge pull request #10538 from f321x/fix_10536 | Merge commits | optional | easy | high | skip |
| `31c2ffbf` | Merge pull request #10532 from spesmilo/variable_trampoline_onions | Merge commits | optional | easy | high | skip |
| `3cf2c325` | Merge pull request #10506 from accumulator/spend_from_coin_selection_refactor | Merge commits | optional | easy | high | skip |
| `37159e47` | qml: 2fa: make it possible to copy 2fa secret | Wallet/core non-LN | optional | difficult | high | manual-port |
| `cb023e22` | qml: 2fa: make 2fa setup qr code clickable | Qt GUI / QML | optional | difficult | high | skip |
| `0dcef978` | daemon: forbid "setconfig" command to change rpcserver settings in-flight | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `06e9f2b5` | Merge pull request #10534 from SomberNight/202603_rpc_password_not_empty | Merge commits | optional | easy | high | skip |
| `efb3e344` | Merge pull request #10543 from f321x/qml_trustedcoin | Merge commits | optional | easy | high | skip |
| `3012c367` | Qt: move LN fee slider to payment dialog. fixes #10516 | Qt GUI / QML | optional | difficult | high | skip |
| `06490657` | fix: remove negative fee assert from get_tx_fee_warning | Wallet/core non-LN | optional | difficult | high | manual-port |
| `a76603ce` | Merge pull request #10073 from f321x/fix_issue_10065 | Merge commits | optional | easy | high | skip |
| `e08390a0` | daemon: (trivial) CommandsServer.run: move tcp-specific line | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `bd443994` | Merge pull request #10545 from SomberNight/202603_commands_getsockname | Merge commits | optional | easy | high | skip |
| `d951a3d2` | in GUI mode, only start a limited minimal RPC server | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `726d3995` | qt gui: more defensive 'gui' RPC (i.e. URI) handling | Security / RPC hardening | mandatory | difficult | high | manual-port |
| `0265c707` | LNWallet: only include tramp r_tags if tramp feature | Lightning core | optional | moderate | high | manual-port |
| `609a2746` | LNWallet: set trampoline invoice feature independently | Lightning core | optional | difficult | high | manual-port |
| `ac87eea0` | test_lnwallet: unittest trampoline invoice_feature and r_tag | Tests only | optional | easy | high | cherry-pick |
| `9d50d78e` | Merge pull request #10541 from f321x/trampoline_feature_invoice | Merge commits | optional | easy | high | skip |
| `297aed99` | lnpeer: check just-in-time channel opening fee | Lightning core | optional | moderate | high | manual-port |
| `1f17574d` | lnchannel: fix update_unfunded_state, add unittest | Lightning core | optional | moderate | high | manual-port |
| `2da9fbbf` | lnworker/config: check if zeroconf is enabled when forwarding | Lightning core | optional | difficult | high | manual-port |
| `f56e1caf` | lnworker: stop setting static jit alias for jit channel | Lightning core | optional | moderate | high | manual-port |
| `2eac67b4` | open_channel_just_in_time: add cleanup and broadcast retry | Lightning core | optional | difficult | high | manual-port |
| `a3f12506` | tests: add unittests for LNWallet just in time opening | Tests only | optional | easy | high | cherry-pick |
| `85356e55` | lnwallet: make jit fees configurable, add mining fees | Lightning core | optional | moderate | high | manual-port |
| `a06c8bac` | lnpeer: don't signal OPTION_ZEROCONF_OPT to untrusted peer | Lightning core | optional | difficult | high | manual-port |
| `a4af5cf4` | qt: ReceiveTab: fix flickering zeroconf message | Qt GUI / QML | optional | difficult | high | skip |
| `032dfcf1` | plugins: use decorator to early return if plugin not authorized | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `35b44a1e` | Merge pull request #10552 from spesmilo/authorized_decorator | Merge commits | optional | easy | high | skip |
| `a5085190` | plugin.py: fix some type hints | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `316e2b8c` | Merge pull request #10554 from SomberNight/202603_plugin_fix_type_hints | Merge commits | optional | easy | high | skip |
| `7afec538` | follow-up prev | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `b9a24ae1` | plugin: nwc: handle missing params dict in request | NWC plugin | optional | moderate | high | cherry-pick |
| `1aad09a6` | qt: SettingsDialog: guard self.network access | Qt GUI / QML | optional | difficult | high | skip |
| `efbe1907` | Merge pull request #10556 from f321x/settings_dialog_guard_network | Merge commits | optional | easy | high | skip |
| `eb6a796d` | Merge pull request #10555 from f321x/nwc_handle_missing_params | Merge commits | optional | easy | high | skip |
| `d3321265` | crypto.py: replace sys.exit with ImportError | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `11f0a68c` | trampoline: prevent adding ourself on the route | Lightning core | optional | difficult | high | manual-port |
| `88f9c49a` | ci: add claude code code review | Build / CI / packaging | optional | easy | high | manual-port |
| `a8cd2715` | Merge pull request #10553 from f321x/code_review | Merge commits | optional | easy | high | skip |
| `85ea6af5` | ci: llm sec review: tweak trigger types | Build / CI / packaging | optional | easy | high | manual-port |
| `9d204abf` | daemon: set restrictive permission on RPC-server unix domain socket | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `7755d97a` | set restrictive unix umask application-wide by default | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `efcf1f05` | Merge pull request #10547 from SomberNight/202603_umask | Merge commits | optional | easy | high | skip |
| `8942ceac` | Merge pull request #10558 from f321x/followup_10541 | Merge commits | optional | easy | high | skip |
| `09a09057` | Merge pull request #10548 from SomberNight/202603_lockdown_rpcserver | Merge commits | optional | easy | high | skip |
| `65fb7395` | segwit_addr: bech32 decode without checksum option | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `b7a51284` | onion_message: factor out get_blinded_paths_to_me from get_blinded_reply_paths. the former also calculates payinfo information for payment scenarios. include payment_relay struct for payment blinded_paths. | Lightning core | optional | moderate | high | manual-port |
| `8d4affa2` | test_onion_message: test get_blinded_paths_to_me | Tests only | optional | easy | high | cherry-pick |
| `5c4fc2d7` | onion_message: verify LNPeerAddr returned as hint in NoRouteFound | Tests only | optional | easy | high | cherry-pick |
| `2b6ad681` | tests: test_onion_message: mock LNWallet._add_peer | Tests only | optional | easy | high | cherry-pick |
| `3e3bffa4` | onion_message: let caller specify considered channels for blinded paths. This allows restricting blinded paths to channels that have sufficient receive capacity for payment. | Lightning core | optional | moderate | high | manual-port |
| `9bcbbdd3` | move blinding_privkey from onion_message to lnonion | Lightning core | optional | moderate | high | manual-port |
| `2e0f2632` | onion_message: iterate blinded paths for onion message requests | Lightning core | optional | moderate | high | manual-port |
| `4134dc7b` | onion_message: split send_onion_message_to | Lightning core | optional | moderate | high | manual-port |
| `4254c9a0` | onion_message: fix route construction to ip | Lightning core | optional | moderate | high | manual-port |
| `e71616e6` | update release notes for version 4.7.2 | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `7adc833f` | contrib: check for unsigned apk in release.sh | Build / CI / packaging | optional | easy | high | manual-port |
| `2ea48746` | Merge pull request #10566 from f321x/release_script_apk | Merge commits | optional | easy | high | skip |
| `7a6a39d1` | add comments about xpub encryption | Lightning core | optional | moderate | high | manual-port |
| `3d390742` | verifier.py: fix CVE-2012-2459: reject left-sibling duplicates | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `fd230cf9` | plugin: nwc: handle 'null' params in request | NWC plugin | optional | moderate | high | cherry-pick |
| `3304d769` | Merge pull request #10571 from f321x/nwc_handle_null_params | Merge commits | optional | easy | high | skip |
| `9827734a` | exchange rate: fix coingecko api | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `8a12874c` | qml: allow renaming wallets | Security / RPC hardening | mandatory | difficult | high | manual-port |
| `1235b4a6` | Merge pull request #10572 from f321x/fix_coingecko | Merge commits | optional | easy | high | skip |
| `016c8b5f` | bip21: add comment listing URI scheme handler registrations | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `ef702d74` | pi: handle lud-17 URI payment identifier | Qt GUI / QML | optional | difficult | high | skip |
| `a5f1a299` | pi: don't match literal \| char in regexes | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `78135ac8` | windows: delete lightning URI hooks on uninstall | Build / CI / packaging | optional | easy | high | manual-port |
| `24d93420` | qml: add top padding to nostr relay url list | Qt GUI / QML | optional | difficult | high | skip |
| `4a14feff` | lnpeer: chan_reest: clarify my_current_per_commitment_point is ignored | Lightning core | optional | moderate | high | manual-port |
| `3fbf5974` | Merge pull request #10579 from f321x/qml_relay_list_padding | Merge commits | optional | easy | high | skip |
| `b3808b79` | Using GET_MASTER_FINGERPRINT for Legacy Client to get the root public key fingerprint | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `16c8cb50` | lnchannel: (trivial) fix type hint of receive_fail_reasons | Lightning core | optional | moderate | high | manual-port |
| `21946e1e` | lnpeer: channel_reestablish: split "they_are_ahead" into ctn vs revnum | Lightning core | optional | moderate | high | manual-port |
| `ca8bdba0` | tests: lnpeer: fix flaky test "hold_invoice_set_doesnt_get_expired" | Tests only | optional | easy | high | cherry-pick |
| `febe95e6` | wallet: make_unsigned_tx: fix base_tx for GUI simple-send batching | Qt GUI / QML | optional | moderate | high | skip |
| `45458c2f` | wallet_db: put 'genesis_blockhash' in DB, detect mainnet/testnet mixup | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `68e6995a` | bitcoin.py: add helper func: neuter_bitcoin_address | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `b45d89e1` | Merge pull request #10546 from f321x/bolt12_preparation_1 | Merge commits | optional | easy | high | skip |
| `1ba31448` | ci: bump code review ci claude version 4.6 -> 4.7 | Build / CI / packaging | optional | easy | high | manual-port |
| `1bea2392` | Merge pull request #10595 from f321x/update_ci_review_model | Merge commits | optional | easy | high | skip |
| `c1893601` | Merge pull request #10590 from SomberNight/202604_test_lnpeer_flaky_hold_invoice_set | Merge commits | optional | easy | high | skip |
| `294d2140` | Merge pull request #10568 from SomberNight/202604_verifier_left_sibling_duplicates | Merge commits | optional | easy | high | skip |
| `bca41d94` | Merge pull request #10573 from f321x/qml_wallet_rename | Merge commits | optional | easy | high | skip |
| `dba6b751` | android: update for rebase p4a, update qt to 6.10, ndk to 28 | Build / CI / packaging | optional | difficult | medium | manual-port |
| `9772a6d5` | qml: add workarounds for issue assigning custom types to QObject properties | Qt GUI / QML | optional | difficult | high | skip |
| `fd5b8676` | qml: don't import QtMultimedia when running on android (android 8 compat) | Qt GUI / QML | optional | difficult | high | skip |
| `4d55b049` | android: upgrade to androidx.core:core:1.16.0 from com.android.support:support-compat:28.0.0 | Build / CI / packaging | optional | difficult | high | manual-port |
| `42472a1e` | android: minimum API 26 required for Qt6.10 (Android 8.0) | Build / CI / packaging | optional | difficult | high | manual-port |
| `cdb5c0b8` | qml: styling updates qt6.10 | Qt GUI / QML | optional | difficult | high | manual-port |
| `e99b3023` | qml: wizard styling, password dialog styling | Qt GUI / QML | optional | difficult | high | skip |
| `28f744f7` | qml: additional styling updates | Qt GUI / QML | optional | difficult | high | skip |
| `738992ac` | qml: don't add navigationbar padding when on-screen keyboard is visible, also allow stackview pages to override navigationbar background color to allow correct color runoff below buttons | Qt GUI / QML | optional | difficult | high | skip |
| `1c0851c6` | styling OpenChannelDialog | Qt GUI / QML | optional | moderate | high | skip |
| `3a740256` | qml: add missing button containers | Qt GUI / QML | optional | difficult | high | skip |
| `87bb63e4` | qml: use standard Button for buttons outside of buttoncontainer | Qt GUI / QML | optional | difficult | high | skip |
| `895679a6` | qml: styling History, ProxyConfig and NostrConfigDialog | Qt GUI / QML | optional | difficult | high | skip |
| `7c83e749` | icons: square closebutton.png and copy_bw.png so they don't resize on highlight (qml) and upscale qrcode-[_white].png for the same reason and so we don't need to apply scaling | Qt GUI / QML | optional | difficult | high | skip |
| `3c5dc660` | qml: various styling updates | Qt GUI / QML | optional | difficult | high | skip |
| `8e78d747` | qml: remove unused components | Qt GUI / QML | optional | difficult | high | skip |
| `31b19740` | qml: FlatButton: show indicator for press-and-hold functionality | Qt GUI / QML | optional | difficult | high | skip |
| `3f34e6be` | qml: additional styling InfoTextArea in dialogs | Qt GUI / QML | optional | difficult | high | skip |
| `32318987` | android: update Qt6 to 6.10.2, PyQt6 to 6.10.2 | Build / CI / packaging | optional | difficult | high | manual-port |
| `f2e8b466` | qml: add type hints for QVariant pyqtProperty workarounds | Qt GUI / QML | optional | difficult | high | skip |
| `74f3c042` | android: pin hostpython3 PyProjectRecipe versions, pin android and pyjnius recipes Cython version | Build / CI / packaging | optional | difficult | high | manual-port |
| `854f95b7` | android: openssl 3.0.18 | Build / CI / packaging | optional | difficult | high | manual-port |
| `c8f5798d` | android: build pyqt_builder and sip ourselves, hash pin all hostpython_prerequisites | Build / CI / packaging | optional | difficult | high | manual-port |
| `9d5b4a7c` | android: use plain 'build' dependency (using 'venv') instead of 'build[virtualenv]', remove setuptools as its use is now pinned via hostpython_prerequisites where applicable, update depends asserts in pyqt6sip, sip, pyqt_builder | Build / CI / packaging | optional | difficult | high | manual-port |
| `7b7d7028` | android: hash-pin hostpython prerequisites for pyqt6sip and sip | Build / CI / packaging | optional | difficult | high | manual-port |
| `29b5e167` | p4a ref 1098be6964cfc2156959e435e81c2c50f8398586 | Build / CI / packaging | optional | easy | high | manual-port |
| `83b67700` | android: remove unneeded dl-ndk-ci.sh | Build / CI / packaging | optional | difficult | high | manual-port |
| `8e49eb80` | appimage: update Dockerfile dependencies | Build / CI / packaging | optional | easy | high | manual-port |
| `36e9f185` | regtest: make fw_fail_htlc less flaky | Tests only | optional | easy | high | cherry-pick |
| `46eadbf4` | lnpeer: channel_reestablish: further restrict states for msg handler | Lightning core | optional | moderate | high | manual-port |
| `14f20294` | regtest: increase timeouts 30s -> 120s | Tests only | optional | easy | high | cherry-pick |
| `230e6275` | Merge pull request #10600 from SomberNight/202604_lnpeer_chan_reest | Merge commits | optional | easy | high | skip |
| `d13c6a6a` | Merge pull request #10596 from romanz/update-patch | Merge commits | optional | easy | high | skip |
| `4b412de9` | Merge pull request #10599 from f321x/fix_fw_fail_htlc | Merge commits | optional | easy | high | skip |
| `7c433c56` | rm 'received orphan channnel' log line (too verbose) | Lightning core | optional | moderate | high | manual-port |
| `d34129ef` | qml: deduplicate wallet name validation | Qt GUI / QML | optional | difficult | high | skip |
| `294fdd12` | Merge pull request #10604 from f321x/dedup_valid_wallet_name | Merge commits | optional | easy | high | skip |
| `44570bfa` | Bump minimum required version of ledger_bitcoin (build-time and runtime) | Build / CI / packaging | optional | easy | high | manual-port |
| `d31d1cf7` | onion_message: simplify send_onion_message_to | Lightning core | optional | moderate | high | manual-port |
| `3ff3205b` | onion_message: use util.random_shuffled_copy instead rand sort | Lightning core | optional | moderate | high | manual-port |
| `5a0c0523` | onion_message: move round-robin logic in Request method | Lightning core | optional | moderate | high | manual-port |
| `c66458e5` | Merge pull request #10598 from f321x/onion_message_followup | Merge commits | optional | easy | high | skip |
| `e96b833f` | Merge pull request #10592 from SomberNight/202604_testnet_mainnet_mixup2 | Merge commits | optional | easy | high | skip |
| `b9dc6aa3` | Merge pull request #10591 from SomberNight/202604_fix_wallet_mktx_base_tx | Merge commits | optional | easy | high | skip |
| `1096ebcd` | build: update pinned ledger-bitcoin (partial rerun freeze_packages) | Build / CI / packaging | optional | easy | high | manual-port |
| `c8c44e35` | qt: send start_new_window exc to reporter | Qt GUI / QML | optional | difficult | high | skip |
| `5af40f43` | Merge branch '202604_pr10603_ledger' | Docs / release notes | not relevant | easy | high | skip |
| `ca212da7` | Merge pull request #10605 from f321x/crash_reporter_start_new_window | Merge commits | optional | easy | high | skip |
| `6933faee` | trampoline: handle edges with known fees in allocation | Lightning core | optional | difficult | high | manual-port |
| `06fd0889` | test_lnrouter: add unittests for tramp fee allocation | Tests only | optional | easy | high | cherry-pick |
| `b483e0d1` | trampoline: _allocate_fee_budget_among_route: followup comment | Lightning core | optional | difficult | high | manual-port |
| `8be4f8c8` | Merge pull request #10606 from f321x/trampoline_route_fees | Merge commits | optional | easy | high | skip |
| `cc1874c9` | Merge pull request #10575 from f321x/lnurlw_prefix | Merge commits | optional | easy | high | skip |
| `96a3345a` | setup.py: "qml_gui" extra: update pyqt version | Build / CI / packaging | optional | difficult | high | manual-port |
| `9b26c181` | Merge pull request #10485 from accumulator/ndk28_qt610_rebase_p4a | Merge commits | optional | easy | high | skip |
| `9079badf` | qml: add default topPadding to ElTextArea | Qt GUI / QML | optional | difficult | high | skip |
| `68726370` | qml: ElTextArea: hide placeholder text on user input | Qt GUI / QML | optional | difficult | high | skip |
| `3534f62b` | crash_reporter: detect more altcoin-forks, don't send reports | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `306cac19` | lnaddr: rename LnAddr -> bolt11 | Qt GUI / QML | optional | difficult | high | skip |
| `560d90e8` | qt, watchtower: cleanup imports | Qt GUI / QML | optional | difficult | high | skip |
| `d2700dfb` | qml: BalanceDetails: fix typo | Qt GUI / QML | optional | difficult | high | skip |
| `b0a5e201` | bolt11: follow-up renames | Lightning core | optional | difficult | high | manual-port |
| `f60cdb0f` | Merge pull request #10614 from f321x/lnaddr_rename | Merge commits | optional | easy | high | skip |
| `044c00a4` | Merge pull request #10585 from f321x/qml_eltextarea_padding | Merge commits | optional | easy | high | skip |
| `5a31bf6a` | Merge pull request #10463 from f321x/jit_2 | Merge commits | optional | easy | high | skip |
| `df5c8c4c` | create_routes_for_payment: allow trampoline forwarding without channel_db if there is a direct path | Lightning core | optional | difficult | high | manual-port |
| `f3a8dd61` | lazy trampoline: | Lightning core | optional | difficult | high | manual-port |
| `187ea806` | lazy_trampoline: adapt unit test | Lightning core | optional | difficult | high | manual-port |
| `b776daca` | Merge pull request #10613 from SomberNight/202604_crash_report_altcoin | Merge commits | optional | easy | high | skip |
| `c964fdef` | Merge pull request #10544 from spesmilo/lazy_trampoline | Merge commits | optional | easy | high | skip |
| `3399c20a` | commands: export_lightning_preimage: add comment about wallet password | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `bd5ac019` | release notes: 4.7.2: add links to security disclosures | Docs / release notes | not relevant | easy | high | skip |
| `a271e2f1` | SECURITY.md: enable "private vuln reports" on GitHub | Docs / release notes | not relevant | easy | high | skip |
| `5122ad10` | Merge pull request #10616 from SomberNight/202604_security_md | Merge commits | optional | easy | high | skip |
| `e1153265` | qml: QERequestDetails: handle _wallet = None in callback | Qt GUI / QML | optional | difficult | high | skip |
| `52d00688` | Merge pull request #10618 from f321x/fix_10617 | Merge commits | optional | easy | high | skip |
| `5a5c1e1f` | commands: add list_channel_htlcs command to list failed, inflight and settled HTLCs for a channel | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `4357ef2f` | LnFeatures: rename OPTION_ANCHORS_ZERO_FEE_HTLC to OPTION_ANCHORS | Lightning core | optional | difficult | high | manual-port |
| `be2096f8` | lnpeer: add property for "config" | Lightning core | optional | moderate | high | manual-port |
| `efa4d06e` | lnpeer: simplify channel_type, as it is now "assumed" | Lightning core | optional | moderate | high | manual-port |
| `7ccf349f` | lnworker: add docstring to pay_invoice | Lightning core | optional | moderate | high | manual-port |
| `ed0e6e90` | Merge pull request #10624 from SomberNight/202605_lnworker_payinvoice_docstring | Merge commits | optional | easy | high | skip |
| `323bf7b1` | lnonion/onion_wire: encrypted_data -> encrypted_recipient_data | Lightning core | optional | moderate | high | manual-port |
| `63e0258b` | lnonion: rm is_onion_message param from process_onion_packet | Lightning core | optional | moderate | high | manual-port |
| `3ca17838` | Merge pull request #10626 from f321x/rm_is_onionmessage_param | Merge commits | optional | easy | high | skip |
| `d0936cc8` | Merge pull request #10621 from f321x/rm_encrypted_data | Merge commits | optional | easy | high | skip |
| `193ea6da` | LNWallet: set OPT_ANCHOR_REQ for peer, rm config.ENABLE_ANCHOR_CHANNELS | Lightning core | optional | difficult | high | manual-port |
| `02847771` | tests: lnpeer: simplify anchors | Lightning core | optional | difficult | high | manual-port |
| `e2ec6b3c` | tests: lnpeer: simplify anchors more | Tests only | optional | difficult | high | manual-port |
| `6bd6dc1f` | lnpeer: refuse new incoming SRK channels | Lightning core | optional | moderate | high | manual-port |
| `621eac23` | lnutil.ChannelType: rm "discard unknown" part from discard_unknown_and_check | Lightning core | optional | moderate | high | manual-port |
| `36e6e435` | Merge pull request #10622 from SomberNight/202604_lnpeer_channel_type | Merge commits | optional | easy | high | skip |
| `c99879a7` | interface: explain how to make aiorpcx log json traffic | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `d8159dfc` | tests: interface: split ToyServer from ToyServerSession | Tests only | optional | easy | high | cherry-pick |
| `4043d84f` | tests: split out toy_server from test_interface.py | Tests only | optional | easy | high | cherry-pick |
| `2cb11800` | tests: toy_server: move start/stop logic | Tests only | optional | easy | high | cherry-pick |
| `86ca70d9` | tests/toyserver: track UTXOs, and forbid conflicts | Tests only | mandatory | easy | high | cherry-pick |
| `0811f3d7` | tests: toyserver: add faucet | Tests only | optional | easy | high | cherry-pick |
| `62a03ff5` | tests: toyserver: add basic remove_tx/reorg functionality | Wallet/core non-LN | optional | difficult | high | manual-port |
| `be9b4cbb` | tests: toyserver: extend remove_tx to subgraph of transitive children | Tests only | optional | easy | high | cherry-pick |
| `755672d0` | tests: toyserver: move to subdirectory | Tests only | optional | easy | high | cherry-pick |
| `b9cb44db` | wallet: make_unsigned_transaction: nicer error msg for bad outputs | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `2ccca903` | tests: toyserver: add tests, implement mempool replacement | Tests only | optional | easy | high | cherry-pick |
| `b89898ee` | tests: toyserver: calc_sh_history: impl sort order, unconf parent (-1) | Tests only | optional | easy | high | cherry-pick |
| `8c47499b` | swaps: server_update_pairs: add named constant for MAX_SWAP_AMT | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `de613196` | Merge pull request #10629 from SomberNight/202605_toy_server2 | Merge commits | optional | easy | high | skip |
| `ddc4d2fd` | build: appimage: fix build: bump alpine apk deps | Build / CI / packaging | optional | easy | high | manual-port |
| `12dfa15e` | contrib: android: make_apk.sh: add/update testnet comments | Build / CI / packaging | optional | difficult | high | manual-port |
| `4800573f` | contrib: build-{linux,wine}: continue fixing build user env | Build / CI / packaging | optional | easy | high | manual-port |
| `b3be2a01` | build: fix regression: support local dev builds also using UID!=1000 | Build / CI / packaging | optional | moderate | high | manual-port |
| `66f53f52` | Merge pull request #10486 from SomberNight/202602_afiore_android_build | Merge commits | optional | easy | high | skip |
| `c3e900ef` | create_channel_backup: handle case where peer_addresses list is empty | Lightning core | optional | moderate | high | manual-port |
| `ef2f9e33` | lnpeer: send channel update also for private channels, if we are forwarding | Lightning core | optional | moderate | high | manual-port |
| `abc5e25a` | Merge pull request #10630 from spesmilo/send_channel_update | Merge commits | optional | easy | high | skip |
| `da53b4eb` | qml: fix userinfo race in Invoice view | Qt GUI / QML | optional | difficult | high | skip |
| `0505ef59` | qewallet: replace some threads with coroutines | Qt GUI / QML | optional | moderate | high | skip |
| `37b6fe3d` | lnonion: factor out next_blinding_from_shared_secret | Lightning core | optional | moderate | high | manual-port |
| `9aef60e3` | contrib/android/Readme.md: mention build cache | Docs / release notes | not relevant | easy | high | skip |
| `cbe97a8c` | lnworker: fix _get_next_peers_to_try regression | Lightning core | optional | moderate | high | manual-port |
| `b15be1fa` | wallet: encrypt the keystore before adding it to db | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `2de7f4aa` | Merge pull request #10632 from f321x/next_blinding_func | Merge commits | optional | easy | high | skip |
| `e1099925` | Merge pull request #10631 from f321x/qml_fix_status_race | Merge commits | optional | easy | high | skip |
| `91d558eb` | Merge pull request #10634 from spesmilo/encrypt_keystore_first | Merge commits | optional | easy | high | skip |
| `ce4e9f55` | Merge pull request #10633 from f321x/fix_gossip_regression | Merge commits | optional | easy | high | skip |
| `844f68d2` | Merge pull request #10619 from accumulator/cli_list_channel_htlcs | Merge commits | optional | easy | high | skip |
| `a1d8483d` | lnpeer: send channel_update on channel_reestablish | Lightning core | optional | moderate | high | manual-port |
| `913e635b` | Merge pull request #10635 from f321x/send_channel_update | Merge commits | optional | easy | high | skip |
| `eca128a8` | util: ESocksProxy: add fixme for is_proxy_tor race | Wallet/core non-LN | optional | moderate | high | cherry-pick |
| `aed6ec14` | regtests: swaps: add test for forward-swap success case | Security / RPC hardening | mandatory | moderate | high | cherry-pick |
| `9a569f3e` | regtests: make wait_until_spent more robust | Tests only | optional | easy | high | cherry-pick |
| `bed768e5` | qml: InvoiceDialog: rename "Remote Pubkey" -> "Recipient Pubkey" | Qt GUI / QML | optional | difficult | high | skip |
| `5003939e` | Merge pull request #10642 from f321x/remote_pubkey | Merge commits | optional | easy | high | skip |
| `0c52a01a` | ci: code review: pass commit messages into prompt context | Build / CI / packaging | optional | easy | high | manual-port |
| `6eba49b6` | ci: code review: extend prompt to verify commit message intent | Docs / release notes | not relevant | easy | high | skip |
| `828766db` | Merge pull request #10643 from f321x/ci_code_review_move | Merge commits | optional | easy | high | skip |
| `d0860ed7` | Move StoredDict class into new 'stored_dict' module | Lightning core | optional | difficult | high | manual-port |
| `e0fd4d83` | Merge pull request #10644 from spesmilo/move_stored_dict | Merge commits | optional | easy | high | skip |
| `a7e595ef` | lnutil: rename LNFC.INVOICE -> BOLT11_INVOICE, add b12 LNFC | Lightning core | optional | difficult | high | manual-port |
| `7ed84375` | lnutil: add blinded path feature flag | Lightning core | optional | moderate | high | manual-port |
| `9150de11` | lnutil: make dependencies context dependent | Lightning core | optional | difficult | high | manual-port |
| `a7d552ad` | lnutil: add to_tlv_bytes() to LnFeatures | Lightning core | optional | moderate | high | manual-port |
| `b2e519fe` | lnutil: update LN_FEATURES_IMPLEMENTED | Lightning core | optional | moderate | high | manual-port |
| `16f73521` | LNWallet: make get_invoice_features base feature independent | Lightning core | optional | moderate | high | manual-port |
| `8b70f215` | Merge pull request #10612 from f321x/bolt12_lnutil_additions | Merge commits | optional | easy | high | skip |
| `12547f94` | tests: regtest: make test_just_in_time less flaky | Tests only | optional | easy | high | cherry-pick |
| `10efb3e9` | Merge pull request #10648 from f321x/fix_jit_regtest | Merge commits | optional | easy | high | skip |
| `b27ab844` | Merge pull request #10637 from SomberNight/202605_swap_regtest_forward | Merge commits | optional | easy | high | skip |
| `5f6a491f` | new 'stored_at' syntax | Lightning core | optional | difficult | high | manual-port |
| `0eda368a` | Merge pull request #10424 from vishwas-droid/util-filenotfounderror | Merge commits | optional | easy | high | skip |
| `b9be9749` | Merge pull request #10647 from spesmilo/stored_at_syntax | Merge commits | optional | easy | high | skip |
