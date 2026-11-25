import hashlib
import json
import re
import sys
from itertools import product
from math import lcm
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "ehsandto/cadence-intersection/" + "a" * 40 + "/fixtures/"
ALIGNED = [[6, 2], [8, 4]]
CONFLICT = [[6, 2], [8, 3]]


@pytest.fixture
def index(direct_deploy):
    instance = direct_deploy(str(ROOT / "contracts/CadenceIntersection.py"))
    return instance, sys.modules[type(instance._instance).__module__]


def mock(vm, name, cycles, tampered=False):
    body = (ROOT / "fixtures" / (name + ".json")).read_bytes()
    path = PREFIX + name + ".json"
    vm.clear_mocks()
    vm.mock_web(re.escape("https://raw.githubusercontent.com/" + path) + "$", {
        "method": "GET", "response": {"status": 200, "headers": {}, "body": body + (b" " if tampered else b"")},
    })
    vm.mock_llm(r".*CADENCE INTERSECTION EXTRACTION.*", json.dumps({"cycles": cycles}))
    return path, hashlib.sha256(body).hexdigest()


def test_aligned_manifest_and_blackouts(index, direct_vm):
    contract, _ = index
    args = mock(direct_vm, "aligned", ALIGNED)
    key = contract.index_schedule(*args)
    assert key == args[1]
    assert direct_vm.run_validator()
    record = contract.get_schedule(key)
    assert record["progression"] == {"status": "READY", "period": 24, "phase": 20}
    assert record["merged_blackouts"] == [[19, 23], [44, 45]]
    assert contract.query(key, 0, 100) == {"status": "READY", "count": 2, "first": 68, "last": 92, "skipped": 2}
    assert contract.query(key, 20, 44) == {"status": "READY", "count": 0, "first": None, "last": None, "skipped": 1}


def test_conflict_has_pairwise_witness(index, direct_vm):
    contract, _ = index
    key = contract.index_schedule(*mock(direct_vm, "conflict", CONFLICT))
    assert direct_vm.run_validator()
    assert contract.get_schedule(key)["progression"] == {
        "status": "CONFLICT", "witness": {"indices": [0, 1], "residues": [0, 1], "gcd": 2},
    }
    assert contract.query(key, 0, 100)["count"] == 0


def test_validator_refetches_and_compares_exact_phase(index, direct_vm):
    contract, _ = index
    args = mock(direct_vm, "aligned", ALIGNED)
    contract.index_schedule(*args)
    mock(direct_vm, "aligned", CONFLICT)
    assert not direct_vm.run_validator()
    mock(direct_vm, "aligned", ALIGNED, tampered=True)
    assert not direct_vm.run_validator()
    assert contract.index_schedule(*args) == args[1]


def test_unknown_phase_stays_unresolved(index, direct_vm):
    contract, _ = index
    key = contract.index_schedule(*mock(direct_vm, "aligned", [[6, 2], None]))
    assert direct_vm.run_validator()
    assert contract.query(key, 0, 100) == {
        "status": "UNKNOWN", "count": None, "first": None, "last": None, "skipped": None,
    }


def test_crt_matches_enumeration(index):
    _, module = index
    cycles = [(p, a) for p in range(2, 9) for a in range(p)]
    for (p, a), (q, b) in product(cycles, repeat=2):
        period = lcm(p, q)
        hits = [t for t in range(period) if t % p == a and t % q == b]
        result = module.combine([[p, a], [q, b]])
        if hits:
            assert result == {"status": "READY", "period": period, "phase": hits[0]}
        else:
            assert result["status"] == "CONFLICT"


def test_window_counts_match_brute_force(index):
    _, module = index
    blackouts = module.merge_blackouts([[17, 23], [0, 2], [9, 14], [13, 17], [27, 28]])
    assert blackouts == [[0, 2], [9, 23], [27, 28]]
    for start in range(31):
        for end in range(start, 31):
            aligned = [t for t in range(start, end) if t % 3 == 2]
            hits = [t for t in aligned if not any(a <= t < b for a, b in blackouts)]
            assert module.measure({"status": "READY", "period": 3, "phase": 2}, blackouts, start, end) == {
                "status": "READY", "count": len(hits), "first": hits[0] if hits else None,
                "last": hits[-1] if hits else None, "skipped": len(aligned) - len(hits),
            }
