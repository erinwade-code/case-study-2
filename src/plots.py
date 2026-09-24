import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def make_bar_plot(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    x_label: str,
    y_label: str,
    output_path: str,
) -> None:
    """Create and save a bar plot."""
    plt.figure(figsize=(10, 6))

    plt.bar(data[x_column], data[y_column])

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def make_heatmap(
    data: pd.DataFrame,
    title: str,
    x_label: str,
    y_label: str,
    output_path: str,
) -> None:
    """Create and save a Seaborn heatmap."""
    plt.figure(figsize=(12, 24))

    vmax = data.stack().quantile(0.99)

    sns.heatmap(
        data,
        cmap="YlOrRd",
        linewidths=0.2,
        linecolor="white",
        vmin=0,
        vmax=vmax,
        cbar_kws={"label": "Dutiable Value (PHP)"},
    )

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=0)
    plt.yticks(fontsize=6)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()