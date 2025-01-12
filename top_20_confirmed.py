import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
confirmed_global = pd.read_csv('Covid19/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_global = pd.read_csv('Covid19/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

# Aggregate data for each country
def aggregate_data(df):
    df = df.drop(columns=["Lat", "Long", "Province/State"], errors="ignore")  # Drop unnecessary columns
    df = df.groupby("Country/Region").sum()  # Aggregate by country
    return df

# Process datasets
confirmed_by_country = aggregate_data(confirmed_global)
recovered_by_country = aggregate_data(recovered_global)

# Extract the latest data
latest_confirmed = confirmed_by_country.iloc[:, -1]
latest_recovered = recovered_by_country.max(axis=1)  # Use maximum recovery data for each country

# Combine data
combined_data = pd.DataFrame({
    "Country/Region": confirmed_by_country.index,
    "Confirmed": latest_confirmed.values,
    "Recoveries": latest_recovered.values
})

# Filter the top 20 countries by confirmed cases
top_20_confirmed = combined_data.sort_values(by="Confirmed", ascending=False).head(20)

# Plot
fig, ax = plt.subplots(figsize=(14, 8))

bar_width = 0.4
x = range(len(top_20_confirmed))

# Plot Confirmed cases
ax.bar(x, top_20_confirmed["Confirmed"], width=bar_width, label="Confirmed Cases", color="blue", align="center")

# Plot Recovery cases
ax.bar([i + bar_width for i in x], top_20_confirmed["Recoveries"], width=bar_width, label="Recoveries", color="green", align="center")

# Add labels, title, and legend
ax.set_xlabel("Country", fontsize=12)
ax.set_ylabel("Number of Cases", fontsize=12)
ax.set_title("Top 20 Countries by Confirmed Cases and Recoveries", fontsize=14)
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(top_20_confirmed["Country/Region"], rotation=45, ha="right")
ax.legend()

plt.tight_layout()
plt.savefig("F:/python_environment/Covid19/saved_figure/top_20_confirmed_vs_recoveries.png")
plt.show()

