import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import session, WeatherData
import sys
import os
from datetime import datetime

# Get the temperature unit from command-line arguments
temp_unit = sys.argv[1] if len(sys.argv) > 1 else '°C'  # Default to Celsius if not provided

# Directory to save images
image_directory = 'weather_visualizations'

# Create the directory if it doesn't exist
os.makedirs(image_directory, exist_ok=True)

def fetch_weather_data():
    # Fetch data for all cities and calculate daily averages
    data = session.query(WeatherData).all()
    
    # Create a DataFrame from the fetched data
    df = pd.DataFrame([(d.city, d.timestamp.date(), d.temperature, d.humidity) for d in data],
                      columns=['City', 'Date', 'Temperature', 'Humidity'])
    
    # Convert temperature to the selected unit
    if temp_unit == 'K':
        df['Temperature'] += 273.15  # Convert Celsius to Kelvin

    # Group by City and Date to get averages
    df_grouped = df.groupby(['City', 'Date']).agg({'Temperature': 'mean', 'Humidity': 'mean'}).reset_index()

    return df_grouped

def generate_file_name(base_name):
    # Generate a timestamp for the file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(image_directory, f"{base_name}_{timestamp}.png")  # Save in the specified directory

def add_timestamp(ax):
    # Get current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add the timestamp to the plot in the top right corner
    ax.text(0.99, 0.99, current_time, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

def plot_heat_maps(df):
    # Pivot the DataFrame for heat map
    temp_pivot = df.pivot(index="Date", columns="City", values="Temperature")
    hum_pivot = df.pivot(index="Date", columns="City", values="Humidity")

    # Set up the matplotlib figure with adjusted size
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # Increased size

    # Heat map for Temperature
    sns.heatmap(temp_pivot, cmap="YlGnBu", ax=axs[0], cbar_kws={'label': f'Temperature ({temp_unit})'})
    axs[0].set_title('Temperature Heatmap', fontsize=16)
    axs[0].set_xlabel('City', fontsize=12)
    axs[0].set_ylabel('Date', fontsize=12)
    add_timestamp(axs[0])  # Add timestamp to the temperature heatmap

    # Heat map for Humidity
    sns.heatmap(hum_pivot, cmap="YlGnBu", ax=axs[1], cbar_kws={'label': 'Humidity (%)'})
    axs[1].set_title('Humidity Heatmap', fontsize=16)
    axs[1].set_xlabel('City', fontsize=12)
    axs[1].set_ylabel('Date', fontsize=12)
    add_timestamp(axs[1])  # Add timestamp to the humidity heatmap

    plt.tight_layout()
    plt.savefig(generate_file_name('heatmaps'))  # Save the plot as an image
    plt.close()  # Close the plot to avoid display issues

def plot_daily_weather_summary(df):
    # Plotting daily summaries (average temperature and humidity per city)
    plt.figure(figsize=(14, 7))
    for city in df['City'].unique():
        city_data = df[df['City'] == city]
        plt.plot(city_data['Date'], city_data['Temperature'], marker='o', label=city)
    
    plt.title('Daily Weather Summary', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel(f'Temperature ({temp_unit})', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    add_timestamp(plt.gca())  # Add timestamp to the current axis
    plt.tight_layout()
    plt.savefig(generate_file_name('daily_weather_summary'))  # Save the plot as an image
    plt.close()  # Close the plot to avoid display issues

def plot_historical_trends(df):
    # Historical trends: average temperature and humidity over time
    plt.figure(figsize=(14, 7))
    
    avg_temp = df.groupby('Date')['Temperature'].mean()
    avg_hum = df.groupby('Date')['Humidity'].mean()

    plt.plot(avg_temp.index, avg_temp, label='Avg Temperature', color='orange', marker='o')
    plt.plot(avg_hum.index, avg_hum, label='Avg Humidity', color='blue', marker='o')

    plt.title('Historical Trends of Temperature and Humidity', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Values', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend()
    add_timestamp(plt.gca())  # Add timestamp to the current axis
    plt.tight_layout()
    plt.savefig(generate_file_name('historical_trends'))  # Save the plot as an image
    plt.close()  # Close the plot to avoid display issues

def plot_triggered_alerts(df):
    # Example condition for alerts (e.g., temperature above 30 degrees)
    alert_condition = df['Temperature'] > 30  # Adjust this condition as necessary
    alerts = df[alert_condition]

    if not alerts.empty:
        plt.figure(figsize=(14, 7))

        # Group alerts by city and date
        grouped_alerts = alerts.groupby(['City', 'Date']).agg({'Temperature': 'max'}).reset_index()

        # Create a multi-bar graph
        cities = grouped_alerts['City'].unique()
        num_cities = len(cities)
        width = 0.15  # Width of the bars

        # Set the positions of the bars on the x-axis
        dates = grouped_alerts['Date'].unique()
        x = range(len(dates))

        # Loop through each city and create bars
        for i, city in enumerate(cities):
            city_alerts = grouped_alerts[grouped_alerts['City'] == city]

            # Ensure x-values and heights have the same length
            if len(city_alerts) > 0:  # Check if there are alerts for the city
                # Aligning x-values to the alert dates
                city_x = [x_val + (i * width) for x_val in range(len(city_alerts))]
                plt.bar(city_x, city_alerts['Temperature'], width=width, label=city)

        plt.title('Triggered Alerts by City', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Temperature', fontsize=12)
        plt.xticks([x_val + (num_cities * width) / 2 for x_val in x], dates, rotation=45)  # Center x-ticks
        plt.legend(title='Cities')
        add_timestamp(plt.gca())  # Add timestamp to the current axis
        plt.tight_layout()
        plt.savefig(generate_file_name('triggered_alerts'))  # Save the plot as an image
        plt.close()  # Close the plot to avoid display issues
    else:
        print("No alerts triggered.")

# Call the functions to plot visualizations
if __name__ == "__main__":
    df = fetch_weather_data()
    plot_heat_maps(df)
    plot_daily_weather_summary(df)
    plot_historical_trends(df)
    plot_triggered_alerts(df)
