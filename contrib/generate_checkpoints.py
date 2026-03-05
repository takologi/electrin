#!/usr/bin/env python3
"""Generate Electrin/Electrum-format checkpoints from a running Rincoin Core node.

Usage:
    python3 contrib/generate_checkpoints.py [--rpc-url URL] [--output FILE]

This script connects to a Rincoin Core RPC endpoint and produces the
checkpoints.json file used by Electrin for SPV chain validation.

== Checkpoint format ==

The file is a JSON array of [hash, target] pairs, one per 2016-block chunk:

    [
        ["<hash of block 2015>",  <target as int>],
        ["<hash of block 4031>",  <target as int>],
        ...
    ]

Because Rincoin uses DGW v3 (difficulty adjusts every block from height 30000)
and Electrin sets SPV_SKIP_DA_BITS_CHECK = True, the `target` field is not
used for validation. We store zero for all entries.

== Rincoin difficulty algorithm: Dark Gravity Wave v3 ==

DGW v3 (activated at height 30000 on Rincoin mainnet) re-calculates the
difficulty target for every single block, using the timestamps and targets of
the most recent 24 blocks. Before height 30000, Rincoin uses a classic
Bitcoin-style 2016-block retarget. The relevant parameters from
rincoin/src/chainparams.cpp are:

    consensus.nPowTargetTimespan = 33 * 60 * 60   # 33 hours
    consensus.nPowTargetSpacing  = 60              # 1 minute blocks
    consensus.DGWHeight          = 30000           # DGW activation height
    consensus.powLimit = uint256S("0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")

An SPV wallet cannot independently recompute the DGW target without downloading
all 24 ancestor headers for every block. Electrin therefore trusts the `bits`
field declared in each header and only verifies that
`RinHash(header) <= bits_to_target(bits)`. Checkpoints provide a second layer
of assurance: the hash of the last block in each 2016-block segment is pinned,
preventing header-chain replacement within the checkpointed range.

== Prerequisites ==

    pip install requests

== Example ==

    # Generate from local node (default 127.0.0.1:9555)
    python3 contrib/generate_checkpoints.py \\
        --rpc-url http://rpcuser:rpcpassword@127.0.0.1:9555 \\
        --output electrum/chains/rincoin/checkpoints.json

Then commit the updated checkpoints.json.
"""

import argparse
import json
import sys
try:
    import requests
except ImportError:
    sys.exit("Error: 'requests' package required.  pip install requests")

CHUNK_SIZE = 2016


def rpc_call(url: str, method: str, params=None):
    """Issue a JSON-RPC call to Rincoin Core."""
    payload = {
        "jsonrpc": "1.0",
        "id": "electrin-checkpoints",
        "method": method,
        "params": params or [],
    }
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    result = r.json()
    if result.get("error"):
        raise RuntimeError(f"RPC error: {result['error']}")
    return result["result"]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rpc-url", default="http://rpcuser:rpcpassword@127.0.0.1:9555",
                        help="Rincoin Core JSON-RPC URL (default: http://rpcuser:rpcpassword@127.0.0.1:9555)")
    parser.add_argument("--output", default="electrum/chains/rincoin/checkpoints.json",
                        help="Output file path (default: electrum/chains/rincoin/checkpoints.json)")
    args = parser.parse_args()

    print(f"Connecting to Rincoin Core at {args.rpc_url} ...")
    info = rpc_call(args.rpc_url, "getblockchaininfo")
    tip_height = info["blocks"]
    print(f"Chain tip: height {tip_height}")

    num_chunks = tip_height // CHUNK_SIZE  # complete chunks only
    print(f"Generating {num_chunks} checkpoints ({num_chunks * CHUNK_SIZE} blocks) ...")

    checkpoints = []
    for i in range(num_chunks):
        height = (i + 1) * CHUNK_SIZE - 1  # last block in chunk
        block_hash = rpc_call(args.rpc_url, "getblockhash", [height])
        # Store target as 0 — Electrin's SPV_SKIP_DA_BITS_CHECK ignores it
        checkpoints.append([block_hash, 0])
        if (i + 1) % 50 == 0 or i == num_chunks - 1:
            print(f"  ... {i + 1}/{num_chunks} (height {height})")

    with open(args.output, "w") as f:
        json.dump(checkpoints, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(checkpoints)} checkpoints to {args.output}")


if __name__ == "__main__":
    main()
