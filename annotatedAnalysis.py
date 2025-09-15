import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statannotations.Annotator import Annotator
from itertools import product

# Map the color to each hue level
custom_palette = {
    "High": "#1f77b4",   # strong blue
    "Medium": "#aec7e8", # muted blue
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

# Create the bar plot
boxPlot = sns.catplot(
    data=subset,
    x="financial_scenario",
    y="monthly_income",
    hue="financial_stress_level",
    kind="box",
    order=scenario_order,
    hue_order=hue_order,
    palette=custom_palette
)

# Define pairs for annotation: compare stress levels within each scenario
pairs = [
    ((scenario, "Low"), (scenario, "High"))
    for scenario in scenario_order
]

# Add annotator
ax = boxPlot.ax
annotator = Annotator(ax, pairs, data=subset, x="financial_scenario", y="monthly_income", hue="financial_stress_level")
annotator.configure(test="Mann-Whitney", text_format="simple")
annotator.apply_and_annotate()

# Labels and title
boxPlot.set_axis_labels("Economic Scenario", "Monthly Income (USD)")
boxPlot._legend.set_title("Financial Stress Level")
plt.title("Monthly Income Distribution by Scenario and Stress Level")
plt.ylim(0)

plt.show()
