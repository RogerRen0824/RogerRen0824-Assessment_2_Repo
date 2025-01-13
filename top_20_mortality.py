import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
confirmed_global = pd.read_csv('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_global = pd.read_csv('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_global = pd.read_csv('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

# Aggregate data for each country
def aggregate_data(df):
    df = df.drop(columns=["Lat", "Long", "Province/State"], errors="ignore")  # Drop unnecessary columns
    df = df.groupby("Country/Region").sum()  # Aggregate by country
    return df

# Process datasets
confirmed_by_country = aggregate_data(confirmed_global)
deaths_by_country = aggregate_data(deaths_global)

# Extract the latest data
latest_confirmed = confirmed_by_country.iloc[:, -1]
latest_deaths = deaths_by_country.iloc[:, -1]

# Calculate Mortality Rate (%)
mortality_rate = (latest_deaths / latest_confirmed) * 100

# Replace NaN or infinite values with 0
mortality_rate.fillna(0, inplace=True)
mortality_rate.replace([float('inf'), -float('inf')], 0, inplace=True)

# Create a DataFrame for visualization
mortality_rate_df = pd.DataFrame({
    "Country/Region": mortality_rate.index,
    "Mortality Rate (%)": mortality_rate.values
})

# Filter out countries with unreasonable values
mortality_rate_df = mortality_rate_df[mortality_rate_df["Mortality Rate (%)"] < 100]

# Sort by Mortality Rate in descending order
top_20_mortality = mortality_rate_df.sort_values(by="Mortality Rate (%)", ascending=False).head(20)

# Plot
plt.figure(figsize=(12, 6))
plt.bar(top_20_mortality["Country/Region"], top_20_mortality["Mortality Rate (%)"], color="red")
plt.xlabel("Country")
plt.ylabel("Mortality Rate (%)")
plt.title("Top 20 Countries by COVID-19 Mortality Rate")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("saved_figure/top_20_mortality_rate.png")
plt.show()
