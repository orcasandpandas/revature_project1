import matplotlib.pyplot as plt
import pandas as pd

import os

from clean_data import get_data


if __name__ == '__main__':
    df: pd.DataFrame = get_data()


    df["Success"] = df["Status Mission"].str.strip() == "Success"
    stats = df.groupby("Location").agg(
        total=("Location", "size"),
    )

    stats.info()

    stats = stats.sort_values(by="total", ascending=False).head(20)

    location = stats.index
    x = range(len(location))
    bar_width = 0.4

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(x, stats["total"])
    ax.bar_label(bars, labels=[f"{t:.0f}" for t in stats["total"]], padding=3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(location, rotation=45, ha="right")
    ax.set_xlabel("Location")
    ax.set_ylabel("Launches")
    ax.set_title("Launches Per Location")

    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "..", "output", "launches_per_location.png"))

