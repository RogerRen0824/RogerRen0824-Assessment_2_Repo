import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
confirmed_global = pd.read_csv('Covid19/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_global = pd.read_csv('Covid19/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
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
latest_recovered = recovered_by_country.max(axis=1)  # Take the maximum value for recovery data

# Calculate Recovery Rate (%)
recovery_rate = (latest_recovered / latest_confirmed) * 100

# Replace NaN or infinite values with 0
recovery_rate.fillna(0, inplace=True)
recovery_rate.replace([float('inf'), -float('inf')], 0, inplace=True)

# Create a DataFrame for visualization
recovery_rate_df = pd.DataFrame({
    "Country/Region": recovery_rate.index,
    "Recovery Rate (%)": recovery_rate.values
})

# Sort by Recovery Rate in descending order
top_20_recovery = recovery_rate_df.sort_values(by="Recovery Rate (%)", ascending=False).head(20)

# Plot
plt.figure(figsize=(12, 6))
plt.bar(top_20_recovery["Country/Region"], top_20_recovery["Recovery Rate (%)"], color="green")
plt.xlabel("Country")
plt.ylabel("Recovery Rate (%)")
plt.title("Top 20 Countries by COVID-19 Recovery Rate")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("F:/python_environment/Covid19/saved_figure/top_20_recovery_rate.png")
plt.show()
