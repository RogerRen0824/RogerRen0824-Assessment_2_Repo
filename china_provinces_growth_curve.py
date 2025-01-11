import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio  # Import for saving HTML

# Load dataset
file_path = 'Covid19/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
data = pd.read_csv(file_path)

# Filter data where Country/Region == 'China'
china_data = data[data['Country/Region'] == 'China']

# Group by Province/State and keep only columns with date-like headers
china_provinces = china_data.groupby('Province/State').sum()
china_provinces = china_provinces.loc[:, ~china_provinces.columns.isin(['Lat', 'Long'])]  # Exclude non-date columns

# Convert columns to datetime format and transpose the DataFrame
china_provinces.columns = pd.to_datetime(china_provinces.columns, errors='coerce')  # Convert to datetime
china_provinces = china_provinces.T  # Transpose to make dates the index

# Ensure all values are numeric
china_provinces = china_provinces.apply(pd.to_numeric, errors='coerce')  # Convert non-numeric values to NaN

# Create an interactive Plotly graph
fig = go.Figure()

# Add a line for each province
for province in china_provinces.columns:
    fig.add_trace(go.Scatter(
        x=china_provinces.index,
        y=china_provinces[province],
        mode='lines',
        name=province
    ))

# Update layout
fig.update_layout(
    title='Interactive COVID-19 Growth Curves in Provinces of China',
    xaxis_title='Date',
    yaxis_title='Cumulative Number of Infections',
    legend_title='Province',
    template='plotly_white',
    hovermode='x unified'
)

# Save the graph as an HTML file
output_file = "F:/python_environment/Covid19/saved_figure/china_covid_growth_curves.html"
pio.write_html(fig, file=output_file, auto_open=False)  # auto_open=False to prevent it from opening immediately

# Show the interactive graph
fig.show()
