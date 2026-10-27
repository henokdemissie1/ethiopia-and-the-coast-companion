"""Verify the distributed companion files before regenerating any outputs.

SPDX-License-Identifier: MIT
Copyright (c) 2026 Henok Kefelegn
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
failures = []
for entry in manifest["files"]:
    relative = Path(entry["path"])
    if relative.is_absolute() or ".." in relative.parts or ":" in entry["path"]:
        failures.append(f"Invalid relative path: {entry['path']}")
        continue
    target = ROOT / relative
    if not target.is_file():
        failures.append(f"Missing file: {entry['path']}")
        continue
    data = target.read_bytes()
    if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
        failures.append(f"Changed file: {entry['path']}")
if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"PASS: all {len(manifest['files'])} manifest-listed files match their distributed hashes.")
print("MANIFEST.json excludes itself. Regenerating outputs may change their hashes.")
