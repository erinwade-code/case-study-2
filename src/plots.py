import matplotlib.pyplot as plt
import pandas as pd


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
    """Create and save a heatmap."""
    plt.figure(figsize=(10, 6))

    plt.imshow(data, aspect="auto")

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.colorbar()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()