import requests
from database import session, ForecastData
import datetime
import sys

API_KEY = '1fa6718532eb116d16802a85e1ad26a0'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Get the temperature unit from command-line arguments
temp_unit = sys.argv[1] if len(sys.argv) > 1 else '°C'  # Default to Celsius if not provided

def convert_temperature(temp_kelvin, unit='°C'):
    if unit == '°C':
        return temp_kelvin - 273.15  # Convert to Celsius
    else:
        return temp_kelvin  # Return Kelvin by default

def fetch_and_store_forecast():
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            forecast_data = response.json()

            total_temp = 0
            total_humidity = 0
            conditions = {}
            count = 0

            # Loop through the forecast list
            for forecast in forecast_data['list']:
                forecast_timestamp_utc = datetime.datetime.fromtimestamp(forecast['dt'], tz=datetime.timezone.utc)

                # Extract data
                temp_kelvin = forecast['main']['temp']
                temp_converted = convert_temperature(temp_kelvin, temp_unit)
                humidity = forecast['main']['humidity']
                condition = forecast['weather'][0]['main']

                # Create and store the forecast data
                forecast_entry = ForecastData(
                    city=city,
                    temperature=temp_converted,
                    condition=condition,
                    humidity=humidity,
                    wind_speed=forecast['wind']['speed'],
                    timestamp=forecast_timestamp_utc
                )
                session.add(forecast_entry)

                # Aggregate data for summaries
                total_temp += temp_converted
                total_humidity += humidity
                conditions[condition] = conditions.get(condition, 0) + 1
                count += 1

            session.commit()
            average_temp = total_temp / count if count > 0 else 0
            average_humidity = total_humidity / count if count > 0 else 0
            most_common_condition = max(conditions, key=conditions.get) if conditions else "Unknown"

            # Generate and print summary
            print(f"Forecast summary for {city}:")
            temp_symbol = "°C" if temp_unit == '°C' else "K"
            print(f"  Average Temperature: {average_temp:.2f} {temp_symbol}")
            print(f"  Average Humidity: {average_humidity:.2f}%")
            print(f"  Most Common Condition: {most_common_condition}")
            print("---------------------------------------------------")

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {city}: {e}")

# Call the function to fetch forecast data
fetch_and_store_forecast()
