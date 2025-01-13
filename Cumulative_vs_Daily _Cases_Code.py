import pandas as pd
import matplotlib.pyplot as plt

# File paths (replace with your actual paths)
confirmed_path = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deaths_path = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

# Load datasets
confirmed = pd.read_csv(confirmed_path)
deaths = pd.read_csv(deaths_path)

# Filter for China
confirmed = confirmed[confirmed['Country/Region'] == 'China']
deaths = deaths[deaths['Country/Region'] == 'China']

# Group and sum across dates
confirmed_data = confirmed.groupby('Province/State').sum().iloc[:, 4:].sum()
deaths_data = deaths.groupby('Province/State').sum().iloc[:, 4:].sum()

# Convert index to datetime
confirmed_data.index = pd.to_datetime(confirmed_data.index, errors='coerce')
deaths_data.index = pd.to_datetime(deaths_data.index, errors='coerce')

# Calculate daily new cases
daily_new_cases = confirmed_data.diff()

# Calculate rolling averages (7-day)
rolling_new_cases = daily_new_cases.rolling(7).mean()

# Calculate transmission rate (percentage change in confirmed cases)
transmission_rate = confirmed_data.pct_change() * 100
rolling_transmission_rate = transmission_rate.rolling(7).mean()

# Define significant events
events = {
    '2020-01-23': 'Wuhan Lockdown',
    '2020-03-11': 'WHO Declares Pandemic',
    '2020-04-08': 'Wuhan Reopens',
    '2021-01-01': 'New Year 2021',
    '2022-01-01': 'New Year 2022',
}

# Visualization
fig, ax1 = plt.subplots(figsize=(16, 10))

# Plot daily new cases and rolling average
ax1.plot(daily_new_cases.index, daily_new_cases, label='Daily New Cases', color='blue', alpha=0.5)
ax1.plot(rolling_new_cases.index, rolling_new_cases, label='7-Day Rolling Avg of New Cases', color='blue', linestyle='--')
ax1.set_ylabel('Number of Daily New Cases', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Plot transmission rate on secondary y-axis
ax2 = ax1.twinx()
ax2.plot(transmission_rate.index, transmission_rate, label='Daily Transmission Rate (%)', color='orange', alpha=0.5)
ax2.plot(rolling_transmission_rate.index, rolling_transmission_rate, label='7-Day Rolling Avg Transmission Rate', color='orange', linestyle='--')
ax2.set_ylabel('Transmission Rate (%)', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Add event markers
for date, label in events.items():
    event_date = pd.to_datetime(date)
    plt.axvline(event_date, color='red', linestyle='--', alpha=0.7)
    # Add annotations with adjusted positions
    ax1.annotate(
        label,
        xy=(event_date, ax1.get_ylim()[1] * 0.9),  # Adjust placement above plot
        xytext=(event_date, ax1.get_ylim()[1] * 1.05),  # Move text above the plot
        arrowprops=dict(facecolor='red', arrowstyle='wedge,tail_width=0.7'),  # Arrow styling
        fontsize=10,
        color='red',
        rotation=45,
        ha='center',
        va='bottom'
    )

# Simplify x-axis ticks
tick_locations = pd.date_range(start=confirmed_data.index.min(), end=confirmed_data.index.max(), freq='3M')
plt.xticks(
    ticks=tick_locations,
    labels=[date.strftime('%Y-%m') for date in tick_locations],
    rotation=45
)

# Add title and legends
fig.suptitle('COVID-19 Trends in China: Daily Cases and Transmission Rate with Key Events')
ax1.set_xlabel('Date')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Save and show the plot
output_path = 'saved_figure/cumulative_vs_daily_cases_dual_axis.png'
plt.savefig(output_path)
plt.tight_layout()
plt.show()

print(f"Figure saved to: {output_path}")