import os
import re
import pandas as pd
import matplotlib.pyplot as plt


CSV_NAME = "performanceData.csv"
WARMUP_ITERS = 1000
BENCHMARK_PREFIX = "benchmark"


def extract_live_agents_from_dirname(dirname: str) -> int:
    """
    Extract the number from a directory name like 'benchmark100' or 'benchmark-100'.
    """
    m = re.search(r"(\d+)", dirname)
    return int(m.group(1)) if m else None


def find_benchmark_dirs(base_dir: str = "."):
    """
    Find all subdirectories of base_dir whose names start with BENCHMARK_PREFIX.
    """
    dirs = []
    for name in os.listdir(base_dir):
        path = os.path.join(base_dir, name)
        if os.path.isdir(path) and name.startswith(BENCHMARK_PREFIX):
            dirs.append(name)
    return dirs


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

    max_iteration = df["iteration"].max()
    df = df[(df["iteration"] > WARMUP_ITERS) & (df["iteration"] < max_iteration)].copy()
    df["iteration"] = df["iteration"] - WARMUP_ITERS

    avg_tick = df["tickTime"].mean()
    median_tick = df["tickTime"].median()
    avg_live_agents = df["liveAgents"].mean()

    avg_frame = df["frameTime"].mean()
    median_frame = df["frameTime"].median()

    avg_updates_per_sec = avg_live_agents / avg_tick if avg_tick > 0 else float("nan")
    nominal_live_agents = extract_live_agents_from_dirname(dirname)

    return {
        "benchmark": dirname,
        "liveAgents_nominal": nominal_live_agents,
        "liveAgents_avg": avg_live_agents,
        "avg_tickTime": avg_tick,
        "median_tickTime": median_tick,
        "avg_frameTime": avg_frame,
        "median_frameTime": median_frame,
        "avg_updates_per_sec": avg_updates_per_sec,
    }



def main():
    results = []

    benchmark_dirs = find_benchmark_dirs(".")
    if not benchmark_dirs:
        print("No benchmark* directories found.")
        return

    benchmark_dirs = sorted(
        benchmark_dirs,
        key=lambda d: (extract_live_agents_from_dirname(d) or float("inf")),
    )

    for d in benchmark_dirs:
        try:
            stats = process_benchmark_dir(d)
            results.append(stats)
        except Exception as e:
            print(f"Error processing {d}: {e}")

    if not results:
        print("No benchmarks processed successfully.")
        return

    res_df = pd.DataFrame(results)
    res_df["liveAgents_for_plot"] = res_df["liveAgents_nominal"].fillna(
        res_df["liveAgents_avg"]
    )

    res_df = res_df.sort_values("liveAgents_for_plot")
    print("\n=== Benchmark Summary ===")
    print(
        res_df[
            [
                "benchmark",
                "liveAgents_for_plot",
                "avg_tickTime",
                "median_tickTime",
                "avg_frameTime", 
                "median_frameTime",
                "avg_updates_per_sec",
            ]
        ].to_string(index=False)
    )

    res_df.to_csv("benchmark_summary.csv", index=False)

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


if __name__ == "__main__":
    main()
