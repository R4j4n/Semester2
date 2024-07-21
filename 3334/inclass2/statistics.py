import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


def print_summary_statistics(df, column_name):
    # Calculate summary statistics
    mean = df[column_name].mean()
    standard_error = stats.sem(df[column_name])
    median = df[column_name].median()
    mode = df[column_name].mode()[0]  # Taking the first mode in case there are multiple
    std_dev = df[column_name].std()
    sample_variance = df[column_name].var()
    kurtosis = df[column_name].kurtosis()
    skewness = df[column_name].skew()
    data_range = df[column_name].max() - df[column_name].min()
    minimum = df[column_name].min()
    maximum = df[column_name].max()
    count = df[column_name].count()

    # Calculate percentiles
    percentiles = np.percentile(df[column_name], [10, 25, 50, 75, 90, 99])

    # Print summary statistics
    print(f"Summary Statistics for {column_name}:")
    print(f"Mean: {mean:.2f} mAh")
    print(f"Standard Error: {standard_error:.2f}")
    print(f"Median: {median} mAh")
    print(f"Mode: {mode} mAh")
    print(f"Standard Deviation: {std_dev:.2f} mAh")
    print(f"Sample Variance: {sample_variance:.2f}")
    print(f"Kurtosis: {kurtosis:.2f}")
    print(f"Skewness: {skewness:.2f}")
    print(f"Range: {data_range} mAh")
    print(f"Minimum: {minimum} mAh")
    print(f"Maximum: {maximum} mAh")
    print(f"Count: {count}")
    print()
    print("Percentiles for Battery Power:")
    print(f"10th Percentile: {percentiles[0]:.1f} mAh")
    print(f"25th Percentile: {percentiles[1]:.2f} mAh")
    print(f"50th Percentile (Median): {percentiles[2]} mAh")
    print(f"75th Percentile: {percentiles[3]:.2f} mAh")
    print(f"90th Percentile: {percentiles[4]:.2f} mAh")
    print(f"99th Percentile: {percentiles[5]:.2f} mAh")

    # Create a detailed box-and-whisker plot
    plt.figure(figsize=(12, 6))
    boxplot = plt.boxplot(
        df[column_name],
        vert=False,
        patch_artist=True,
        notch=True,
        showmeans=True,
        meanline=True,
    )

    # Adding colors
    colors = ["lightblue"]
    for patch, color in zip(boxplot["boxes"], colors):
        patch.set_facecolor(color)

    # Adding labels for Q1, Q2, mean, etc.
    plt.annotate(
        f"Q1: {percentiles[1]:.2f}",
        xy=(percentiles[1], 1),
        xytext=(percentiles[1], 1.1),
        arrowprops=dict(facecolor="black", shrink=0.05),
    )
    plt.annotate(
        f"Median: {median}",
        xy=(median, 1),
        xytext=(median, 1.15),
        arrowprops=dict(facecolor="black", shrink=0.05),
    )
    plt.annotate(
        f"Mean: {mean:.2f}",
        xy=(mean, 1),
        xytext=(mean, 0.85),
        arrowprops=dict(facecolor="black", shrink=0.05),
    )
    plt.annotate(
        f"Q3: {percentiles[3]:.2f}",
        xy=(percentiles[3], 1),
        xytext=(percentiles[3], 1.1),
        arrowprops=dict(facecolor="black", shrink=0.05),
    )
    plt.annotate(
        f"Min: {minimum}",
        xy=(minimum, 1),
        xytext=(minimum, 1.1),
        arrowprops=dict(facecolor="black", shrink=0.05),
    )
    plt.annotate(
        f"Max: {maximum}",
        xy=(maximum, 1),
        xytext=(maximum, 1.1),
        arrowprops=dict(facecolor="black", shrink=0.05),
    )

    # Styling the plot
    plt.title(f"Box-and-Whisker Plot for {column_name}")
    plt.xlabel("mAh")
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.show()


# read the dataframe
df = pd.read_excel("train.xlsx")
print_summary_statistics(df, "battery_power")
print_summary_statistics(df, "clock_speed")
