import subprocess
import time

PROGRAM = "ecosystem.exe"

# Constants or common arguments
BASE_ARGS = [
    "--test-performance",
    "--tlog", "1000000",
    "--preset", "benchmarkPreset.json"
]

# Values corresponding to your preset suffixes
BENCH_VALUES = [100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]

# Delay between runs (in seconds)
PAUSE_BETWEEN_RUNS = 3


def run_once(value):
    print(f"\n===== Running benchmark {value} =====")

    # Construct command arguments
    args = [
        PROGRAM,
        "--agents", f"{value}",
        "--output", f"output/benchmark-{value}"
    ] + BASE_ARGS

    print("Running:", " ".join(args))

    result = subprocess.run(args)

    if result.returncode == 0:
        print(f"Finished benchmark {value}")
    else:
        print(f"Benchmark {value} failed with return code {result.returncode}")


def main():
    for val in BENCH_VALUES:
        run_once(val)
        print(f"Waiting {PAUSE_BETWEEN_RUNS} seconds…\n")
        time.sleep(PAUSE_BETWEEN_RUNS)

    print("\nAll benchmarks complete\n")


if __name__ == "__main__":
    main()
