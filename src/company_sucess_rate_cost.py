import matplotlib.pyplot as plt
import pandas as pd

import os

from clean_data import get_data


if __name__ == '__main__':
    df: pd.DataFrame = get_data()


    df["Success"] = df["Status Mission"].str.strip() == "Success"
    #remove na rocket rows
    df: pd.DataFrame = df.dropna(subset=["Rocket"])
    stats = df.groupby("Company Name").agg(
        success_rate=("Success", "mean"),
        avg_cost=("Rocket", "mean"),
    )

    stats["cost_per_success_rate"] = stats["avg_cost"] / stats["success_rate"]
    #remove companies with no successful launches
    stats: pd.DataFrame = stats[stats["success_rate"] > 0]
    stats.sort_values(by="cost_per_success_rate", ascending=False, inplace=True)

    companies = stats.index
    x = range(len(companies))
    bar_width = 0.4

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(x, stats["cost_per_success_rate"], color="blue")
    ax.bar_label(bars, labels=[f"{(r * 100):.1f}%" for r in stats["success_rate"]], padding=3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(companies, rotation=45, ha="right")
    ax.set_xlabel("Company")
    ax.set_ylabel("Cost per Unit Success Rate (M$)")
    ax.set_title("Mission Cost per Success Rate by Company")

    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "..", "output", "mission_cost_per_success_rate.png"))
