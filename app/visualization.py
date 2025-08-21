# app/visualization.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_base64

def generate_plot(feature: str, plot_type: str, dataset_path="data/milknew.csv"):
    df = pd.read_csv(dataset_path)

    fig, ax = plt.subplots(figsize=(8, 4))

    if plot_type == "Histogram":
        sns.histplot(data=df, x=feature, kde=True, ax=ax)
        ax.set_title(f"Histogram of {feature}")
    elif plot_type == "Box Plot":
        sns.boxplot(data=df, x=feature, ax=ax)
        ax.set_title(f"Box Plot of {feature}")
    elif plot_type == "Violin Plot":
        sns.violinplot(data=df, x=feature, ax=ax)
        ax.set_title(f"Violin Plot of {feature}")
    else:
        return None

    return fig_to_base64(fig)
