"""Tests for the Python RinHash implementation (electrum.rinhash).

Test vectors are derived from Fulcrum-RIN BTC.cpp::testRinHash() which
validates block 0 (genesis) and block 1 against the Rincoin reference node.
"""

import unittest

from electrum import constants
from electrum.rinhash import rinhash
from electrum.bitcoin import hash_encode
from electrum.blockchain import hash_raw_header


# 80-byte block headers as hex (from Fulcrum-RIN src/BTC.cpp::testRinHash)
_GENESIS_HEX = (
    "0100000000000000000000000000000000000000000000000000000000000000"
    "00000000adcd471c60b9dc56b5dc049e567106388fdf078f936a722b42edd230"
    "85c0908500e8e467ffff001f28850000"
)
_BLOCK1_HEX = (
    "00000020dbc9a8c73baa8093e74eb368f8e36fba9a606fbd4e079ba83c61e4d6"
    "bd960000902e3faad09b8f350a530702e126b19107be3218521dbf9eb5b394ca"
    "40e11278d9ebe767ffff001fa1070100"
)

# Expected hashes (big-endian Electrum convention = what hash_encode produces)
_GENESIS_HASH = "000096bdd6e4613ca89b074ebd6f609aba6fe3f868b34ee79380aa3bc7a8c9db"
_BLOCK1_HASH  = "00002adfb206d5d942abc963b93fa2edb479eb7b6f589f5318ddda5cd732ec19"


class TestRinHash(unittest.TestCase):

    def setUp(self):
        # Ensure we are operating under RincoinMainnet so hash_raw_header
        # dispatches to rinhash() rather than sha256d().
        constants.RincoinMainnet.set_as_network()

    def test_genesis_raw_bytes(self):
        """rinhash() on the raw genesis header bytes returns the correct hash."""
        raw = rinhash(bytes.fromhex(_GENESIS_HEX))
        self.assertEqual(len(raw), 32)
        # hash_encode reverses bytes (little→big endian) and hex-encodes
        self.assertEqual(hash_encode(raw), _GENESIS_HASH)

    def test_block1_raw_bytes(self):
        """rinhash() on the raw block-1 header bytes returns the correct hash."""
        raw = rinhash(bytes.fromhex(_BLOCK1_HEX))
        self.assertEqual(len(raw), 32)
        self.assertEqual(hash_encode(raw), _BLOCK1_HASH)

    def test_hash_raw_header_genesis(self):
        """hash_raw_header() dispatches to RinHash under RincoinMainnet."""
        result = hash_raw_header(bytes.fromhex(_GENESIS_HEX))
        self.assertEqual(result, _GENESIS_HASH)

    def test_hash_raw_header_block1(self):
        """hash_raw_header() dispatches to RinHash under RincoinMainnet."""
        result = hash_raw_header(bytes.fromhex(_BLOCK1_HEX))
        self.assertEqual(result, _BLOCK1_HASH)

    def test_chain_linkage(self):
        """Block 1's prev_block_hash field must equal the genesis hash."""
        block1 = bytes.fromhex(_BLOCK1_HEX)
        # prev_block_hash occupies bytes 4-35 in little-endian order
        prev_le = block1[4:36]
        prev_hash_be = hash_encode(prev_le)  # reverse + hex → big-endian
        self.assertEqual(prev_hash_be, _GENESIS_HASH,
                         "block 1 prev_block_hash does not match genesis hash")

    def test_bitcoin_mainnet_uses_sha256d(self):
        """hash_raw_header() must still use SHA256d on Bitcoin mainnet."""
        constants.BitcoinMainnet.set_as_network()
        try:
            from electrum.crypto import sha256d
            header_bytes = bytes(80)
            expected = hash_encode(sha256d(header_bytes))
            self.assertEqual(hash_raw_header(header_bytes), expected)
        finally:
            constants.RincoinMainnet.set_as_network()


if __name__ == "__main__":
    unittest.main()
