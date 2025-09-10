import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

finance_data = pd.read_csv("./YNAB_Plan.csv", index_col="Account")
# ---------------------------------------
# STEP 1: Clean the 'Outflow' column
# ---------------------------------------

# Remove euro signs and commas, strip whitespace
finance_data['Outflow'] = (
    finance_data['Outflow']
    .astype(str)
    .str.replace('€', '', regex=False)   # Remove euro symbol
    .str.replace(',', '', regex=False)   # Remove thousand separators
    .str.strip()
)

# Convert to numeric (handle coercion of bad entries)
finance_data['Outflow'] = pd.to_numeric(finance_data['Outflow'], errors='coerce')

# ---------------------------------------
# STEP 2: Filter out transfers
# ---------------------------------------
# Filter out rows where 'Payee' contains "Transfer:"
# The '~' operator negates the condition, so it keeps rows that DO NOT match
finance_data_filtered = finance_data[~finance_data['Payee'].str.contains('|'.join(['Transfer','Trf']), na=False)]
# finance_data_filtered = finance_data[(finance_data['Payee'].str.contains(["Small","Medium","High"]))]

# ---------------------------------------
# STEP 3: Group and sum by 'Account'
# ---------------------------------------

# Group by 'Account' and sum Outflows
account_outflows = finance_data_filtered.groupby('Account')['Outflow'].sum().reset_index()
# accountsByPayee = finance_data_filtered.groupby('Account', 'Payee')

# Optional: Remove NaNs or zero outflows if you don't want to plot them
account_outflows = account_outflows.dropna()
account_outflows = account_outflows[account_outflows['Outflow'] != 0]

# Sort by total outflow descending (for better visual)
account_outflows = account_outflows.sort_values('Outflow', ascending=False)

# ---------------------------------------
# STEP 4: Plot using seaborn
# ---------------------------------------

sns.barplot(data=account_outflows, x='Outflow', y='Account', orient="y")

plt.title("Total Outflow by Account")
plt.ylabel("Account")
plt.xlabel("Total Outflow (€)")
plt.tight_layout()
plt.show()
