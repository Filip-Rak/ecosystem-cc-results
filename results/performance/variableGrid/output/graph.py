import os
import pandas as pd
import matplotlib.pyplot as plt

# -------- CONFIG --------
ROOT_DIR = "."
CSV_NAME = "performanceData.csv"
OUTPUT_PATH = "durationGraph.png"

FIG_WIDTH = 6.5
FIG_HEIGHT = 3.8
DPI = 300 
# ------------------------

data_agents_0 = []
data_agents_other = []

for folder in os.listdir(ROOT_DIR):
    folder_path = os.path.join(ROOT_DIR, folder)

    if not os.path.isdir(folder_path):
        continue

    try:
        _, size_part, agents_str = folder.split("-")
        width, height = map(int, size_part.split("x"))
        agents = int(agents_str)

        label = f"{width}x{height} | {int(width * width / 100)}"
        sort_key = width * height

        csv_path = os.path.join(folder_path, CSV_NAME)
        df = pd.read_csv(csv_path)

        duration = df["frameTime"].iloc[1000:].sum()

        if agents == 0:
            data_agents_0.append((sort_key, label, duration))
        else:
            data_agents_other.append((sort_key, label, duration))

    except Exception as e:
        print(f"Skipping {folder}: {e}")

# -------- SORT DATA --------
data_agents_0.sort(key=lambda x: x[0])
data_agents_other.sort(key=lambda x: x[0])

# -------- PLOTTING --------
plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

if data_agents_0:
    x_labels_0 = [d[1] for d in data_agents_0]
    y_0 = [d[2] for d in data_agents_0]
    plt.plot(x_labels_0, y_0, marker="o", label="Czas obliczeń siatki")

if data_agents_other:
    x_labels_1 = [d[1] for d in data_agents_other]
    y_1 = [d[2] for d in data_agents_other]
    plt.plot(x_labels_1, y_1, marker="o", label="Pełny czas obliczeń")

plt.xlabel("Wielkość siatki | liczba agentów")
plt.ylabel("Czas trwania [s]")
plt.title("Czas trwania zależny od wielkości siatki i liczby agentów\n(100 tysięcy iteracji)")
plt.legend()
plt.grid(True)

plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.show()
