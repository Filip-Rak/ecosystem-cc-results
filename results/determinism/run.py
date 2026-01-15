import subprocess
import hashlib
import sys
from pathlib import Path

PROGRAM = "ecosystem.exe"
RUNS = 5

BASE_ARGS = [
    "--tlog", "1000",
    "--preset", "preset.json"
]

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

outputs = []

for i in range(1, RUNS + 1):
    outdir = f"output/run-{i}"
    args = [PROGRAM, "--output", outdir] + BASE_ARGS
    print("Running:", " ".join(args))
    result = subprocess.run(args)  # live output
    if result.returncode != 0:
        sys.exit(result.returncode)
    outputs.append(outdir)

hashes = []
for folder in outputs:
    p = Path(folder) / "tickData.csv"
    h = hash_file(p)
    hashes.append(h)
    print(folder, h)

if all(h == hashes[0] for h in hashes):
    print("All hashes identical.")
else:
    print("Hashes differ.")
