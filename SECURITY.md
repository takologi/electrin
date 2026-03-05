# Security Policy

> **⚠ TESTING PHASE** — Electrin is currently in a testing phase.
> We **strongly recommend NOT using this wallet** for anything other than
> testing with **small amounts** of Rincoin.  There may be undiscovered
> bugs that could lead to loss of funds.

## Reporting a Vulnerability

To report security issues, send an email to the address listed below.
(Not for support. Support requests will be *ignored*.)

<!-- TODO [SECURITY] — Before leaving the testing phase:
     1. Generate a dedicated GPG key pair for the Electrin project
        (see "How to generate project GPG keys" below).
     2. Add additional maintainer keys as the team grows.
     3. Publish the public keys in the `pubkeys/` directory of this repo
        and on public keyservers.
-->

| Name      | Email                          | GPG fingerprint                                   |
|-----------|--------------------------------|---------------------------------------------------|
| Takologi  | takologi [AT] proton [DOT] me  | 588F 056A 90C0 D941 274F 6662 24DC 647F 06EE F1D9 |

### Upstream Electrum contacts (original project)

Electrin is forked from [Electrum](https://github.com/spesmilo/electrum).
If you believe a vulnerability also affects upstream Electrum, please
**also** report it to the original maintainers:

| Name        | Email                                  | GPG fingerprint                                   |
|-------------|----------------------------------------|---------------------------------------------------|
| ThomasV     | thomasv [AT] electrum [DOT] org        | 6694 D8DE 7BE8 EE56 31BE D950 2BD5 824B 7F94 70E6 |
| SomberNight | somber.night [AT] protonmail [DOT] com | 4AD6 4339 DFA0 5E20 B3F6 AD51 E7B7 48CD AF5E 5ED9 |

#### Where to find GPG keys

You can import a key by running the following command with that
individual's fingerprint: `gpg --recv-keys "<fingerprint>"`

Upstream Electrum public keys can also be found in the
[Electrum git repository](https://github.com/spesmilo/electrum),
in the top-level `pubkeys` folder.


-------------------
| DEVELOPER MEMOS |
-------------------

## How to generate project GPG keys

This section documents the procedure for creating the Electrin project
signing keys. These keys are used for:

- Signing release tarballs / binaries
- Signing version-announcement messages (for the update checker)
- Encrypted communication for security reports

### Step 1 — Generate a new GPG key pair

```bash
gpg --full-generate-key
```

Recommended settings:
- **Key type**: RSA and RSA (option 1)
- **Key size**: 4096 bits
- **Expiry**: 2 years (can be extended later)
- **Real name**: `Electrin Release Signing Key` (or your maintainer name)
- **Email**: the project email listed above

### Step 2 — Export the public key

```bash
# ASCII-armored export
gpg --armor --export "takologi@proton.me" > pubkeys/takologi.asc
```

### Step 3 — Publish the key

1. Commit `pubkeys/takologi.asc` to this repository.
2. Upload to public keyservers:
   ```bash
   gpg --keyserver hkps://keys.openpgp.org --send-keys "<YOUR_FINGERPRINT>"
   gpg --keyserver hkps://keyserver.ubuntu.com --send-keys "<YOUR_FINGERPRINT>"
   ```
3. Update the table at the top of this file with the full fingerprint.

### Step 4 — Back up the private key securely

```bash
# Export private key to an encrypted backup (store OFFLINE only)
gpg --armor --export-secret-keys "takologi@proton.me" > electrin-signing-key.private.asc
```

Store the backup on an encrypted USB drive or hardware security module.
**Never** commit private keys to the repository.

### Step 5 — Generate a Rincoin-address signing key (for the in-app update checker)

> **This is NOT a replacement for GPG.**  GPG and Rincoin-address signing
> serve completely different purposes:
>
> | Mechanism | Used for | Verified by |
> |-----------|----------|-------------|
> | **GPG** (Steps 1–4) | Signing release tarballs, git tags, email | Users run `gpg --verify` manually |
> | **Rincoin address** (this step) | Signing version-announcement JSON for the **in-app update checker** | Electrin verifies automatically, in code |
>
> You need **both** for a full release signing workflow.

The in-app update checker (`electrum/gui/qt/update_checker.py`) does NOT
use GPG.  Instead, it fetches a JSON document from the update server:

```json
{
    "version": "4.8.0",
    "signatures": {
        "Rxxxxxxxxxxxxxxxxxxxxxxxxx": "base64-encoded-signature"
    }
}
```

The client verifies the signature using Rincoin's `verifymessage` protocol
(ECDSA sign/verify on the message string, e.g. `"4.8.0"`).  The addresses
it trusts are hardcoded in `VERSION_ANNOUNCEMENT_SIGNING_KEYS` in
`update_checker.py`.

**How to create this key:**

1. **Generate a Rincoin P2PKH address and its private key (WIF).**
   You can use Electrin itself, or any tool that produces Rincoin keys:
   ```bash
   # Using Electrin (once it works reliably):
   electrin create -w /tmp/update-signer
   electrin listaddresses -w /tmp/update-signer   # pick an address
   electrin getprivatekeys <address> -w /tmp/update-signer
   ```

2. **Record the address** (starts with `R`).

3. **Store the WIF private key offline and encrypted.**
   This key will be used to sign each version announcement string before
   publishing it on the update server.  Treat it like a GPG private key.

4. **Add the address to the source code:**
   Edit `electrum/gui/qt/update_checker.py` and add your address to the
   `VERSION_ANNOUNCEMENT_SIGNING_KEYS` tuple (replacing the upstream
   Electrum/Bitcoin addresses that are currently there as placeholders).

5. **When releasing a new version**, sign the version string with the
   WIF key and publish the resulting JSON on the update endpoint:
   ```bash
   # Sign the version string "4.8.0" with the Rincoin address:
   electrin signmessage <address> "4.8.0" -w /path/to/signer-wallet
   # This outputs a base64 signature → put it in the JSON served by the update server.
   ```

6. **Securely destroy** `/tmp/update-signer` after extracting the key.
