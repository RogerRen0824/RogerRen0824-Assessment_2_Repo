import pandas as pd
from tabulate import tabulate
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
deaths_by_country = aggregate_data(deaths_global)
recovered_by_country = aggregate_data(recovered_global)

# Extract latest data
latest_confirmed = confirmed_by_country.iloc[:, -1]
latest_deaths = deaths_by_country.iloc[:, -1]
latest_recovered = recovered_by_country.max(axis=1)  # Use max value for each row for recovery data

# Combine data into one dataframe
combined_data = pd.DataFrame({
    "Country/Region": confirmed_by_country.index,
    "Confirmed": latest_confirmed.values,
    "Deaths": latest_deaths.values,
    "Recoveries": latest_recovered.values
})

# Calculate Mortality Rate and Recovery Rate
combined_data["Mortality Rate (%)"] = (combined_data["Deaths"] / combined_data["Confirmed"]) * 100
combined_data["Recovery Rate (%)"] = (combined_data["Recoveries"] / combined_data["Confirmed"]) * 100

# Replace NaN or infinite values with 0
combined_data.fillna(0, inplace=True)
combined_data.replace([float('inf'), -float('inf')], 0, inplace=True)

# Select relevant columns for the final output
final_data = combined_data[[
    "Country/Region", 
    "Confirmed", 
    "Deaths", 
    "Recoveries", 
    "Mortality Rate (%)", 
    "Recovery Rate (%)"
]]

# Sort by confirmed cases in descending order
final_data = final_data.sort_values(by="Confirmed", ascending=False)

# Display the result
print(tabulate(final_data.head(20), headers="keys", tablefmt="pretty"))

# Save the cleaned data to a CSV file
final_data.to_csv("F:/python_environment/Covid19/cleaned_covid_data.csv", index=False)

# Save the table as an image
fig, ax = plt.subplots(figsize=(10, 6))  # Adjust size as needed
ax.axis("tight")
ax.axis("off")
table = ax.table(
    cellText=final_data.head(20).round(2).values,
    colLabels=final_data.columns,
    cellLoc="center",
    loc="center",
)

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(final_data.columns))))

# Save the table as an image
plt.title("Top 20 Countries by COVID-19 Data", fontsize=14)
output_path = 'F:/python_environment/Covid19/saved_figure/top_20_countries_covid_data.png'
plt.savefig(output_path)
plt.show()

# Optional: Visualize the top 10 countries by recovery rate
top_10_recovery_rate = final_data.sort_values(by="Recovery Rate (%)", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.bar(top_10_recovery_rate["Country/Region"], top_10_recovery_rate["Recovery Rate (%)"], color="green")
plt.xlabel("Country")
plt.ylabel("Recovery Rate (%)")
plt.title("Top 10 Countries by Recovery Rate")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
output_path = 'F:/python_environment/Covid19/saved_figure/top_10_recovery_rate.png'
plt.savefig(output_path)
plt.show()

