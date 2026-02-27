<p align="center">
  <img src="electrum/gui/icons/electrum_text.png" alt="Electrin" height="60">
  <br>
  <img src="electrum/gui/icons/Electrum_512.png" alt="Electrin logo" width="128">
</p>

<h1 align="center">Electrin — Lightweight Rincoin Wallet</h1>

```
Licence: MIT Licence
Author: Takologi
Language: Python (>= 3.10)
Homepage: https://electrin.net
Based on: Electrum by Thomas Voegtlin (https://electrum.org)
```

**Electrin** is a lightweight Rincoin wallet forked from
[Electrum](https://github.com/spesmilo/electrum), the widely trusted
Bitcoin wallet created by Thomas Voegtlin and the Electrum developers.
Electrin connects to [Fulcrum-rin](https://github.com/takologi/Fulcrum-rin)
servers and does not require running a full Rincoin node.

---

## Status

| Target | Status |
|--------|--------|
| Rincoin adaptation | done |
| Name & icon rebrand | done |
| Dark / light theme switching (no restart) | done |
| Windows | done |
| Linux (AppImage) | done |
| Android (APK) | done |
| iOS | planned |
| Preliminary alpha testing | done |
| Functional beta testing | done |
| Thorough release-grade testing | planned |

Rincoin adaptation details:

- [x] Currency units, blockchain parameters, consensus rules
- [x] Wallet address formats (P2PKH, P2SH, bech32 with `rin` HRP)
- [x] Fulcrum-rin server connection
- [x] Lightning support hidden (not applicable to Rincoin)
- [x] Block explorers updated

---

## Getting started

_(If you just want to run Electrin,
[download the latest release](https://github.com/takologi/electrin/releases).)_

Electrin itself is pure Python, and so are most of the required dependencies,
but not everything. The following sections describe how to run from source, but here
is a TL;DR:

```
$ sudo apt-get install libsecp256k1-dev
$ ELECTRUM_ECC_DONT_COMPILE=1 python3 -m pip install --user ".[gui,crypto]"
```

### Not pure-python dependencies

#### RinHash (Rincoin proof-of-work)

Rincoin uses RinHash (BLAKE3 → Argon2d → SHA3-256) for block hashing.
Two additional Python packages are required:

```
$ pip install blake3 argon2-cffi
```

`blake3` contains a compiled C extension; on most platforms a binary wheel is
available. If not, you will need a C compiler and Rust toolchain.
`argon2-cffi` also ships binary wheels; building from source requires
`libffi-dev`:

```
$ sudo apt-get install libffi-dev   # only needed if building argon2-cffi from source
```

Both packages are listed in `contrib/requirements/requirements.txt` and will
be installed automatically by `pip install .`.

#### Qt GUI

If you want to use the Qt interface, install the Qt dependencies:
```
$ sudo apt-get install python3-pyqt6
```

#### libsecp256k1

For elliptic curve operations,
[libsecp256k1](https://github.com/bitcoin-core/secp256k1)
is a required dependency.

If you "pip install" Electrin, by default libsecp will get compiled locally,
as part of the `electrum-ecc` dependency. This can be opted-out of,
by setting the `ELECTRUM_ECC_DONT_COMPILE=1` environment variable.
For the compilation to work, besides a C compiler, you need at least:
```
$ sudo apt-get install automake libtool
```
If you opt out of the compilation, you need to provide libsecp in another way, e.g.:
```
$ sudo apt-get install libsecp256k1-dev
```

#### cryptography

Due to the need for fast symmetric ciphers,
[cryptography](https://github.com/pyca/cryptography) is required.
Install from your package manager (or from pip):
```
$ sudo apt-get install python3-cryptography
```


### Running from tar.gz

If you downloaded the official package (tar.gz), you can run
Electrin from its root directory without installing it on your
system; all the pure python dependencies are included in the 'packages'
directory. To run Electrin from its root directory, just do:
```
$ ./run_electrum
```

You can also install Electrin on your system, by running this command:
```
$ sudo apt-get install python3-setuptools python3-pip
$ python3 -m pip install --user .
```

This will download and install the Python dependencies used by
Electrin instead of using the 'packages' directory.
It will also place an executable named `electrin` in `~/.local/bin`,
so make sure that is on your `PATH` variable.


### Development version (git clone)

_(For OS-specific instructions, see [here for Windows](contrib/build-wine/README_windows.md),
and [for macOS](contrib/osx/README_macos.md))_

Check out the code from GitHub:
```
$ git clone https://github.com/takologi/electrin.git
$ cd electrin
$ git submodule update --init
```

Run install (this should install dependencies):
```
$ python3 -m pip install --user -e .
```

Create translations (optional):
```
$ sudo apt-get install gettext
$ ./contrib/locale/build_locale.sh electrum/locale/locale electrum/locale/locale
```

Finally, to start Electrin:
```
$ ./run_electrum
```

### Run tests

Run unit tests with `pytest`:
```
$ pytest tests -v
```
(can be parallelized with `-n auto` option, using [`pytest-xdist`](https://github.com/pytest-dev/pytest-xdist) plugin)

To run a single file, specify it directly like this:
```
$ pytest tests/test_bitcoin.py -v
```

## Creating Binaries

- [Linux (tarball)](contrib/build-linux/sdist/README.md)
- [Linux (AppImage)](contrib/build-linux/appimage/README.md)
- [macOS](contrib/osx/README.md)
- [Windows](contrib/build-wine/README.md)
- [Android](contrib/android/Readme.md)


## Upstream Credit

Electrin is a fork of [Electrum](https://github.com/spesmilo/electrum),
created by **Thomas Voegtlin** and maintained by the
[Electrum developers](https://github.com/spesmilo/electrum/blob/master/AUTHORS).
We are deeply grateful for their work in building the premier lightweight
Bitcoin wallet — without it, Electrin would not exist.

See the [LICENCE](LICENCE) file for the full MIT licence text, which
covers both the original Electrum code and the Electrin modifications.


## Contributing

Any help testing the software, reporting or fixing bugs, reviewing pull requests
and recent changes, writing tests, or helping with outstanding issues is very welcome.
Implementing new features, or improving/refactoring the codebase, is of course
also welcome, but to avoid wasted effort, especially for larger changes,
we encourage discussing these on the issue tracker first.

Development discussion: [GitHub Issues](https://github.com/takologi/electrin/issues)


## Licence

MIT — see [LICENCE](LICENCE) for details.
