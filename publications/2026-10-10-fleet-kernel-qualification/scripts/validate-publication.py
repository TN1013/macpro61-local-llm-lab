#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
base = Path(__file__).resolve().parent.parent
bad = False
for line in (base/"SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    digest, rel = line.split(None, 1)
    rel = rel.strip().lstrip("*")
    got = hashlib.sha256((base/rel).read_bytes()).hexdigest()
    ok = got == digest
    print(f"{rel}: {'OK' if ok else 'FAILED'}")
    bad |= not ok
sys.exit(1 if bad else 0)
