
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load Datasets ---
lt_breached = pd.read_csv("Long term financial data breached firms thesis IM correct.csv", encoding="ISO-8859-1", sep=None, engine="python", on_bad_lines='skip')
lt_control = pd.read_csv("Long term financial data control firms thesis IM correct.csv", encoding="ISO-8859-1", sep=None, engine="python", on_bad_lines='skip')
st_breached = pd.read_csv("Short term financial data breached firms thesis IM correct.csv", encoding="ISO-8859-1", sep=None, engine="python", on_bad_lines='skip')
st_control = pd.read_csv("Short term financial data control firms thesis IM correct.csv", encoding="ISO-8859-1", sep=None, engine="python", on_bad_lines='skip')

# --- Clean Column Names ---
for df in [lt_breached, lt_control, st_breached, st_control]:
    df.columns = df.columns.str.strip()

# --- Process Long-Term Financials ---
for df in [lt_breached, lt_control]:
    for col in ["S - 1", "S + 1", "S + 2"]:
        df[col] = df[col].astype(str).str.replace(",", "").str.replace("X", "").replace("", pd.NA).astype(float)
    df["Change S+1 (%)"] = ((df["S + 1"] - df["S - 1"]) / df["S - 1"]) * 100
    df["Change S+2 (%)"] = ((df["S + 2"] - df["S - 1"]) / df["S - 1"]) * 100

# --- Long-Term Summary ---
print("\n--- Long-Term Financial Impact ---")
print("Breached Firms (S+2):\n", lt_breached["Change S+2 (%)"].describe().round(2))
print("\nControl Firms (S+2):\n", lt_control["Change S+2 (%)"].describe().round(2))

# --- Process Short-Term Financials ---
for df in [st_breached, st_control]:
    df['Percentage change'] = df['Percentage change'].astype(str).str.replace(",", ".").str.replace("+", "").str.replace("%", "").astype(float)

st_breached['Group'] = 'Breached Firms'
st_control['Group'] = 'Control Firms'

st_combined = pd.concat([
    st_breached[['Ticker', 'Percentage change', 'Group']],
    st_control[['Ticker', 'Percentage change', 'Group']]
])

# --- Short-Term Summary ---
print("\n--- Short-Term Stock Performance ---")
print(st_combined.groupby('Group')["Percentage change"].agg(['mean', 'median', 'std', 'count']).round(2))

# --- Boxplot: Short-Term Stock Change ---
plt.figure(figsize=(8, 6))
sns.boxplot(data=st_combined, x='Group', y='Percentage change', palette='Set3')
plt.axhline(0, linestyle='--', color='gray')
plt.title("Short-Term Stock Price Change: Breached vs Control Firms")
plt.ylabel("Daily % Change in Stock Price")
plt.xlabel("Firm Group")
plt.tight_layout()
plt.savefig("short_term_comparison_boxplot.png")
plt.close()
print("Saved: short_term_comparison_boxplot.png")

# --- Boxplot: Long-Term Revenue Change (S+2) ---
lt_breached['Group'] = 'Breached Firms'
lt_control['Group'] = 'Control Firms'
lt_combined = pd.concat([
    lt_breached[['Ticker', 'Change S+2 (%)', 'Group']],
    lt_control[['Ticker', 'Change S+2 (%)', 'Group']]
])

plt.figure(figsize=(8, 6))
sns.boxplot(data=lt_combined, x='Group', y='Change S+2 (%)', palette='Set2')
plt.axhline(0, linestyle='--', color='gray')
plt.title("Long-Term Revenue Change (S+2 vs. S-1): Breached vs Control Firms")
plt.ylabel("Revenue % Change (S+2)")
plt.xlabel("Firm Group")
plt.tight_layout()
plt.savefig("long_term_comparison_boxplot.png")
plt.close()
print("Saved: long_term_comparison_boxplot.png")
