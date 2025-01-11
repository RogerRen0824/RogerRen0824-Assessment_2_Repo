import pandas as pd
import matplotlib.pyplot as plt

# Load data
confirmed_global = pd.read_csv('Covid19/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths_global = pd.read_csv('Covid19/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

# Aggregate data by country (last column contains the most recent data)
confirmed_by_country = confirmed_global.groupby('Country/Region').sum().iloc[:, -1]
deaths_by_country = deaths_global.groupby('Country/Region').sum().iloc[:, -1]

# Calculate mortality rate
mortality_rate = (deaths_by_country / confirmed_by_country) * 100

# Create a DataFrame for filtering
data = pd.DataFrame({
    'Country': confirmed_by_country.index,
    'Confirmed': confirmed_by_country.values,
    'Deaths': deaths_by_country.values,
    'Mortality Rate (%)': mortality_rate.values
})

# Set thresholds
confirmed_threshold = 100  # Minimum number of confirmed cases
mortality_rate_threshold = 100  # Maximum reasonable mortality rate in percentage

# Filter data
filtered_data = data[
    (data['Confirmed'] >= confirmed_threshold) & 
    (data['Mortality Rate (%)'] <= mortality_rate_threshold)
]

# Sort by mortality rate
filtered_data = filtered_data.sort_values(by='Mortality Rate (%)', ascending=False).head(20)

# Plot top 20 countries by mortality rate
plt.figure(figsize=(12, 6))
plt.bar(filtered_data['Country'], filtered_data['Mortality Rate (%)'], color='blue')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Country')
plt.ylabel('Mortality Rate (%)')
plt.title('Top 20 Countries by COVID-19 Mortality Rate (Filtered)')
output_path = 'F:/python_environment/Covid19/saved_figure/mortality_rate_rank.png'
plt.savefig(output_path)
plt.tight_layout()
plt.show()
