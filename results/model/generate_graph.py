import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "output/continents/tickData.csv"
OUTPUT_PATH = "media/graph/continents_live_agents.png"

TITLE = "Zmiana liczebności populacji w kolejnych iteracjach"
X_LABEL = "Iteracja"
Y_LABEL = "Populacja"

DOWNSAMPLE = 1000
SMOOTHING_WINDOW = 10

FIG_WIDTH = 6.5
FIG_HEIGHT = 3.8
DPI = 300 

plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 14,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,

    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,

    "figure.autolayout": True,
})

df = pd.read_csv(CSV_PATH)
df_ds = df.iloc[::DOWNSAMPLE].copy()

plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

plt.plot(
    df_ds["iteration"],
    df_ds["liveAgents"],
    label=f"Every {DOWNSAMPLE}th record"
)

plt.title(TITLE)
plt.xlabel(X_LABEL)
plt.ylabel(Y_LABEL)

plt.savefig(OUTPUT_PATH, dpi=DPI)

# plt.show()
