# -*- coding: utf-8 -*-
#
# Electrum-RIN – Fulcrum integration tests
# Phase 3 test gate.
#
# These tests connect to the locally running Fulcrum-RIN server
# (127.0.0.1:50001).  They are automatically SKIPPED when the server
# is not reachable so that they do not break offline CI.
#
# To run explicitly:
#   python -m pytest tests/test_rincoin_integration.py -v

import asyncio
import json
import socket
import unittest

from electrum import constants

_FULCRUM_HOST = '127.0.0.1'
_FULCRUM_PORT = 50001


def _server_reachable() -> bool:
    """Return True if the Fulcrum TCP endpoint is reachable."""
    try:
        with socket.create_connection((_FULCRUM_HOST, _FULCRUM_PORT), timeout=2):
            return True
    except OSError:
        return False


_SKIP_MSG = f'Fulcrum not reachable at {_FULCRUM_HOST}:{_FULCRUM_PORT}'


# ---------------------------------------------------------------------------
# Minimal async Electrum JSON-RPC client (no full wallet stack needed)
# ---------------------------------------------------------------------------

class _ElectrumClient:
    """
    Very small asyncio Electrum TCP client sufficient for integration tests.
    Not a full Electrum client – only supports single request/response pairs.
    """

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._reader = None
        self._writer = None
        self._id = 0

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._port)

    async def close(self):
        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass

    async def request(self, method: str, params: list) -> object:
        self._id += 1
        msg = json.dumps({'id': self._id, 'method': method, 'params': params})
        self._writer.write((msg + '\n').encode())
        await self._writer.drain()
        line = await asyncio.wait_for(self._reader.readline(), timeout=10)
        resp = json.loads(line)
        if 'error' in resp and resp['error'] is not None:
            raise RuntimeError(f"Electrum error: {resp['error']}")
        return resp['result']


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

@unittest.skipUnless(_server_reachable(), _SKIP_MSG)
class TestRincoinFulcrumIntegration(unittest.IsolatedAsyncioTestCase):
    """Integration tests that require the local Fulcrum-RIN server."""

    async def asyncSetUp(self):
        constants.RincoinMainnet.set_as_network()
        self.client = _ElectrumClient(_FULCRUM_HOST, _FULCRUM_PORT)
        await self.client.connect()

    async def asyncTearDown(self):
        await self.client.close()
        constants.BitcoinMainnet.set_as_network()

    # ── Server identity ────────────────────────────────────────────────────

    async def test_server_features_genesis_hash(self):
        """genesis_hash in server.features must match our RincoinMainnet constant."""
        features = await self.client.request('server.features', [])
        self.assertEqual(
            features['genesis_hash'],
            constants.RincoinMainnet.GENESIS,
            "genesis_hash mismatch – chain params or GENESIS constant is wrong",
        )

    async def test_server_features_hash_function(self):
        """Fulcrum-RIN reports hash_function='sha256' (RinHash, not sha256d)."""
        features = await self.client.request('server.features', [])
        self.assertEqual(features['hash_function'], 'sha256')

    async def test_server_features_protocol_versions(self):
        features = await self.client.request('server.features', [])
        proto_min = tuple(int(x) for x in features['protocol_min'].split('.'))
        proto_max = tuple(int(x) for x in features['protocol_max'].split('.'))
        self.assertGreaterEqual(proto_min, (1, 4))
        self.assertGreaterEqual(proto_max, proto_min)

    async def test_server_banner(self):
        banner = await self.client.request('server.banner', [])
        self.assertIsInstance(banner, str)
        self.assertGreater(len(banner), 0)

    # ── Block header verification ──────────────────────────────────────────

    async def test_genesis_block_header(self):
        """
        Genesis block header at height 0 must match the known raw bytes.
        The first 4 bytes are the block version (01000000 little-endian = 1).
        """
        GENESIS_HEADER_HEX = (
            '0100000000000000000000000000000000000000000000000000000000000000'
            '00000000adcd471c60b9dc56b5dc049e567106388fdf078f936a722b42edd230'
            '85c0908500e8e467ffff001f28850000'
        )
        result = await self.client.request('blockchain.block.header', [0])
        self.assertEqual(result, GENESIS_HEADER_HEX)

    async def test_genesis_header_version_bytes(self):
        result = await self.client.request('blockchain.block.header', [0])
        version_le = bytes.fromhex(result[:8])
        version = int.from_bytes(version_le, 'little')
        self.assertEqual(version, 1)

    # ── Chain tip ─────────────────────────────────────────────────────────

    async def test_headers_subscribe_returns_tip(self):
        """
        blockchain.headers.subscribe returns the current chain tip.
        We just passed block 459,722 in Phase 0; the chain should be well ahead.
        """
        tip = await self.client.request('blockchain.headers.subscribe', [])
        self.assertIn('height', tip)
        self.assertIn('hex', tip)
        self.assertGreater(tip['height'], 450_000)
        # Verify the hex is a valid 80-byte block header
        self.assertEqual(len(bytes.fromhex(tip['hex'])), 80)

    # ── Scripthash protocol ────────────────────────────────────────────────

    async def test_scripthash_get_history_returns_list(self):
        """
        blockchain.scripthash.get_history for a test-only (unfunded) address
        must return an empty list — not an error.  This verifies that Fulcrum
        accepts the exact SHA256(scriptPubKey)[::-1] hex that our
        address_to_scripthash() produces.
        """
        # P2PKH scripthash for key1 (0x01*32) on RincoinMainnet
        TEST_SH = '3f3a51af7593482038529b8f4338f0ab068b9e52489971ad4052ed7f9d341b6f'
        result = await self.client.request(
            'blockchain.scripthash.get_history', [TEST_SH])
        self.assertIsInstance(result, list)

    async def test_scripthash_get_balance_returns_dict(self):
        """
        blockchain.scripthash.get_balance must return a dict with 'confirmed'
        and 'unconfirmed' keys, even for an unfunded address.
        """
        TEST_SH = '3f3a51af7593482038529b8f4338f0ab068b9e52489971ad4052ed7f9d341b6f'
        result = await self.client.request(
            'blockchain.scripthash.get_balance', [TEST_SH])
        self.assertIn('confirmed', result)
        self.assertIn('unconfirmed', result)
        # Test address is unfunded
        self.assertEqual(result['confirmed'], 0)

    async def test_p2wpkh_scripthash_accepted(self):
        """Fulcrum must accept P2WPKH scripthashes as well as P2PKH."""
        # P2WPKH scripthash for key1 (0x01*32) on RincoinMainnet
        TEST_SH = '034d384e7bb98692522016f8d99b0c07cd4b50ef149dcfa1ba399156b089439f'
        result = await self.client.request(
            'blockchain.scripthash.get_history', [TEST_SH])
        self.assertIsInstance(result, list)

    # ── Block header fetch range ───────────────────────────────────────────

    async def test_block_headers_chunk(self):
        """
        blockchain.block.headers returns count headers starting at start_height.
        Each header is 80 bytes = 160 hex chars.
        """
        result = await self.client.request('blockchain.block.headers', [0, 3])
        self.assertIn('count', result)
        self.assertEqual(result['count'], 3)
        payload = bytes.fromhex(result['hex'])
        self.assertEqual(len(payload), 3 * 80)
        # First 80 bytes must be the genesis header
        GENESIS_HEADER_HEX = (
            '0100000000000000000000000000000000000000000000000000000000000000'
            '00000000adcd471c60b9dc56b5dc049e567106388fdf078f936a722b42edd230'
            '85c0908500e8e467ffff001f28850000'
        )
        genesis_bytes = bytes.fromhex(GENESIS_HEADER_HEX)
        self.assertEqual(payload[:80], genesis_bytes)


if __name__ == '__main__':
    unittest.main()
