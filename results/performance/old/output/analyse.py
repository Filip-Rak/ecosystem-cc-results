import os
import re
import pandas as pd
import matplotlib.pyplot as plt


# Directories we want to process
BENCHMARK_DIRS = [
    "benchmark-100",
    "benchmark-250",
    "benchmark-500",
    "benchmark-750",
    "benchmark-1000",
    "benchmark-10000",
]

CSV_NAME = "performanceData.csv"
WARMUP_ITERS = 1000  # <-- first 1000 iterations are warmup


def extract_live_agents_from_dirname(dirname: str) -> int:
    """
    Extract the number from a directory name like 'benchmark100'.
    """
    m = re.search(r"(\d+)", dirname)
    return int(m.group(1)) if m else None


def process_benchmark_dir(dirname: str):
    """
    Load performanceData.csv from a benchmark directory, apply
    iteration filtering/shift, and compute stats.
    Returns a dict with stats for this benchmark.
    """
    
    csv_path = os.path.join(dirname, CSV_NAME)
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    required_cols = {"iteration", "liveAgents", "frameTime", "tickTime"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"{csv_path} is missing columns: {missing}")

    print(f"{dirname}: read {len(df)} rows")


    # Determine max iteration dynamically (should be 101001 if you log them all)
    max_iteration = df["iteration"].max()

    # Keep iterations (WARMUP_ITERS, max_iteration) exclusive of both ends:
    #   (WARMUP_ITERS + 1) .. (max_iteration - 1)
    df = df[(df["iteration"] > WARMUP_ITERS) & (df["iteration"] < max_iteration)].copy()

    # Shift iteration numbers down by WARMUP_ITERS so analysis starts at 1
    df["iteration"] = df["iteration"] - WARMUP_ITERS

    # Compute stats
    avg_tick = df["tickTime"].mean()
    median_tick = df["tickTime"].median()
    avg_live_agents = df["liveAgents"].mean()

    # As per your definition: average updates/sec = liveAgents / average tickTime
    avg_updates_per_sec = avg_live_agents / avg_tick if avg_tick > 0 else float("nan")

    nominal_live_agents = extract_live_agents_from_dirname(dirname)

    return {
        "benchmark": dirname,
        "liveAgents_nominal": nominal_live_agents,
        "liveAgents_avg": avg_live_agents,
        "avg_tickTime": avg_tick,
        "median_tickTime": median_tick,
        "avg_updates_per_sec": avg_updates_per_sec,
    }


def main():
    results = []

    for d in BENCHMARK_DIRS:
        if not os.path.isdir(d):
            print(f"Warning: directory not found, skipping: {d}")
            continue

        stats = process_benchmark_dir(d)
        results.append(stats)

    if not results:
        print("No benchmarks processed.")
        return

    res_df = pd.DataFrame(results)

    # Use nominal liveAgents (from dir name) if available
    res_df["liveAgents_for_plot"] = res_df["liveAgents_nominal"].fillna(
        res_df["liveAgents_avg"]
    )

    # Sort by liveAgents so the plot looks nice
    res_df = res_df.sort_values("liveAgents_for_plot")

    print("\n=== Benchmark Summary ===")
    print(
        res_df[
            [
                "benchmark",
                "liveAgents_for_plot",
                "avg_tickTime",
                "median_tickTime",
                "avg_updates_per_sec",
            ]
        ].to_string(index=False)
    )

    # Optional: save summary
    res_df.to_csv("benchmark_summary.csv", index=False)

    # Plot: average agent updates per second vs live agents
    plt.figure(figsize=(8, 5))
    plt.plot(
        res_df["liveAgents_for_plot"],
        res_df["avg_updates_per_sec"],
        marker="o",
    )
    plt.xlabel("Live agents")
    plt.ylabel("Average agent updates per second")
    plt.title("Average agent updates per second vs live agents")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    res_df.to_csv("benchmark_summary.csv", index=False)


if __name__ == "__main__":
    main()