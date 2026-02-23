# Copyright (C) 2024-2025 The Rincoin/electrum-rin developers
# Distributed under the MIT software license.
#
# RinHash: the proof-of-work and block-ID hash function for the Rincoin network.
#
# Algorithm (mirrors rincoin/src/crypto/rinhash.cpp):
#   1. BLAKE3  of the 80-byte serialised block header
#   2. Argon2d with salt="RinCoinSalt", t=2, m=64 KiB, p=1, output_len=32
#   3. SHA3-256 of the Argon2d output
#
# Usage:
#   from .rinhash import rinhash
#   raw_bytes = rinhash(header_bytes)   # returns 32 bytes

import hashlib

try:
    import blake3 as _blake3_mod
    _have_blake3 = True
except ImportError as e:
    import logging as _logging
    _logging.getLogger(__name__).error(f"Failed to import blake3: {e}")
    _have_blake3 = False

try:
    from argon2.low_level import hash_secret_raw as _argon2d_raw, Type as _Argon2Type
    _have_argon2 = True
except ImportError:
    _have_argon2 = False

_ARGON2_SALT = b"RinCoinSalt"
_ARGON2_T_COST = 2
_ARGON2_M_COST = 64   # kibibytes
_ARGON2_PARALLELISM = 1
_ARGON2_HASH_LEN = 32


def rinhash(header_bytes: bytes) -> bytes:
    """Return the 32-byte RinHash of *header_bytes* (an 80-byte block header).

    Parameters
    ----------
    header_bytes:
        Exactly 80 bytes of a serialised Rincoin block header.

    Returns
    -------
    bytes
        32-byte hash in *internal* (little-endian) byte order, ready to be
        passed to :func:`~electrum.bitcoin.hash_encode` for display.

    Raises
    ------
    ImportError
        If ``blake3`` or ``argon2-cffi`` is not installed.
    """
    if not _have_blake3:
        raise ImportError(
            "The 'blake3' package is required for Rincoin support. "
            "Install it with:  pip install blake3"
        )
    if not _have_argon2:
        raise ImportError(
            "The 'argon2-cffi' package is required for Rincoin support. "
            "Install it with:  pip install argon2-cffi"
        )

    # Step 1 — BLAKE3
    b3: bytes = _blake3_mod.blake3(header_bytes).digest()

    # Step 2 — Argon2d
    a2: bytes = _argon2d_raw(
        secret=b3,
        salt=_ARGON2_SALT,
        time_cost=_ARGON2_T_COST,
        memory_cost=_ARGON2_M_COST,
        parallelism=_ARGON2_PARALLELISM,
        hash_len=_ARGON2_HASH_LEN,
        type=_Argon2Type.D,
    )

    # Step 3 — SHA3-256
    return hashlib.sha3_256(a2).digest()
