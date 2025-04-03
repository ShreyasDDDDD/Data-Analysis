
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



# --- S&P 500 Index Benchmark Comparison ---
# Load and prepare S&P 500 index data
sp500_index = pd.read_csv("S&P500 market index thesis IM correct.csv", encoding="ISO-8859-1", sep=None, engine="python", on_bad_lines='skip')
sp500_index.columns = sp500_index.columns.str.strip()

# Clean and convert percentage values
sp500_index['Percentage change'] = (
    sp500_index['Percentage change']
    .astype(str)
    .str.replace(",", ".")
    .str.replace("+", "")
    .str.replace("%", "")
    .astype(float)
)

# Parse and sort dates
sp500_index['Date'] = pd.to_datetime(sp500_index['Date'], format="%d-%b-%Y", errors='coerce')
sp500_index = sp500_index.dropna(subset=['Date']).sort_values(by='Date')

# Plot daily change
plt.figure(figsize=(12, 5))
sns.lineplot(data=sp500_index, x='Date', y='Percentage change')
plt.title("S&P 500 Daily Percentage Change Over Time")
plt.axhline(0, linestyle='--', color='gray')
plt.ylabel("Daily % Change")
plt.xlabel("Date")
plt.tight_layout()
plt.savefig("sp500_index_trend.png")
plt.close()

# Compute monthly and 3-month rolling returns
sp500_index['Month'] = sp500_index['Date'].dt.to_period('M')
monthly_index = sp500_index.groupby('Month')['Percentage change'].sum().reset_index()
monthly_index['Month'] = monthly_index['Month'].dt.to_timestamp()
monthly_index['Rolling_3mo_change'] = monthly_index['Percentage change'].rolling(window=3).sum()

# Plot rolling 3-month returns
plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly_index, x='Month', y='Rolling_3mo_change')
plt.title("S&P 500 Rolling 3-Month Performance (Proxy for S-1 to S+2)")
plt.axhline(0, linestyle='--', color='gray')
plt.ylabel("3-Month % Change")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig("sp500_rolling_3mo_trend.png")
plt.close()

# Summary statistics
rolling_summary = monthly_index['Rolling_3mo_change'].describe().round(2)
print("\n--- S&P 500 3-Month Rolling Summary ---")
print(rolling_summary)
