import matplotlib.pyplot as plt
import pandas as pd

import os

from clean_data import get_data


if __name__ == '__main__':
    df: pd.DataFrame = get_data()


    df["Success"] = df["Status Mission"].str.strip() == "Success"
    #remove na rocket rows
    df: pd.DataFrame = df.dropna(subset=["Rocket"])

    df = df[df["Success"] == False]

    stats = df.groupby("Company Name").agg(
        cost=("Rocket", "sum"),
    )

    #remove companies with no successful launches
    stats: pd.DataFrame = stats[stats["cost"] > 0]
    stats.sort_values(by="cost", ascending=False, inplace=True)

    companies = stats.index
    x = range(len(companies))
    bar_width = 0.4

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(x, stats["cost"])
    ax.set_xticks(list(x))
    ax.set_xticklabels(companies, rotation=45, ha="right")
    ax.set_xlabel("Company")
    ax.set_ylabel("Total Failure Cost")
    ax.set_title("Cost of failures per company")

    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "..", "output", "total_failure_cost.png"))
