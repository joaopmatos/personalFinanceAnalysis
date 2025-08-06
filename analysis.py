
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns #plotting library
import matplotlib.pyplot as plt

# Map the color to each hue level
custom_palette = {
    "High": "#1f77b4",   # strong blue (highlighted)
    "Medium": "#aec7e8", # muted blue
    "Low": "#cbddea",    # even lighter blue
}
hue_order = ["Low", "Medium", "High"]

scenario_order = ["Recession Period", "Inflation Period", "Stable Economy"]

finance_data = pd.read_csv("./personal_finance_tracker_dataset.csv", index_col="user_id")
subset = finance_data.head(500)

# Relabel categories in the DataFrame
subset["financial_scenario"] = subset["financial_scenario"].replace({
    "recession": "Recession Period",
    "inflation": "Inflation Period",
    "normal": "Stable Economy"
})

sns.axes_style("white")
sns.set_context("paper")
grid = sns.catplot(
    data=subset,
    x="financial_scenario",
    y="monthly_income",
    hue="financial_stress_level",
    kind="box",
    order=scenario_order,
    hue_order=hue_order,
    palette=custom_palette
)

grid.fig.subplots_adjust(top=0.9, bottom=0.2, left=0.15, right=0.95)

grid.set_axis_labels("Economic Scenario", "Monthly Income (USD)")
grid._legend.set_title("Financial Stress Level")

plt.title("Monthly Income Distribution by Scenario and Stress Level")
plt.ylim(0)
plt.show()