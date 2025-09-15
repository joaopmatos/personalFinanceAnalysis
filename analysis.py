import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Map the color to each hue level
custom_palette = {
    "High": "#1f77b4",   # strong blue
    "Medium": "#c4d7f0", # muted blue
    "Low": "#cbddea",    # light blue
}
hue_order = ["Low", "Medium", "High"]

scenario_order = ["Recession Period", "Inflation Period", "Stable Economy"]

finance_data = pd.read_csv("./personal_finance_tracker_dataset.csv", index_col="user_id")
subset = finance_data.head(500).copy()

# Relabel categories
subset["financial_scenario"] = subset["financial_scenario"].replace({
    "recession": "Recession Period",
    "inflation": "Inflation Period",
    "normal": "Stable Economy"
})

sns.set_style("white")
sns.set_context("paper")

# Create boxplot grid
grid = sns.catplot(
    data=subset,
    x="financial_scenario",
    y="monthly_income",
    hue="financial_stress_level",
    kind="bar",
    order=scenario_order,
    hue_order=hue_order,
    palette=custom_palette
)

# grid.fig.subplots_adjust(top=0.9, bottom=0.2, left=0.15, right=0.95)
grid.set_axis_labels("Economic Scenario", "Monthly Income (USD)")
grid._legend.set_title("Financial Stress Level")
plt.title("Monthly Income Distribution by Scenario and Stress Level")

# === Annotate with min/max ===
ax = grid.ax

# Calculate width of grouped boxes for positioning annotations
n_hue = len(hue_order)
bar_width = 0.8 / n_hue  # distribute hues within each category

# Loop through scenarios and stress levels
for i, scenario in enumerate(scenario_order):
    for j, stress in enumerate(hue_order):
        # Subset data for this combination
        data_group = subset[
            (subset["financial_scenario"] == scenario) &
            (subset["financial_stress_level"] == stress)
        ]["monthly_income"]

        if data_group.empty:
            continue

        ymin, ymax, ymedian = data_group.min() - 100, data_group.max() + 100, data_group.median() + 100
        # X-position offset: center each hue within the category
        x_pos = i - 0.4 + j * bar_width + bar_width / 2

        # Annotate min and max
        # ax.text(x_pos, ymin, f"{ymin:.0f}", ha="center", va="top", fontsize=8, color="black")
        # ax.text(x_pos, ymax, f"{ymax:.0f}", ha="center", va="bottom", fontsize=8, color="black")

        # Annotate mean (inside box area, in bold)
        if stress.title() == "High":
            ax.text(x_pos, ymedian, f"{ymedian:.0f}", ha="center", va="center",
                fontsize=11, color="black", fontweight= "normal")

plt.ylim(0)
plt.show()
