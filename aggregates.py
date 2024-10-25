import requests
from database import session, WeatherData
import sys

API_KEY = '1fa6718532eb116d16802a85e1ad26a0'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Get the temperature unit from command-line arguments
temp_unit = sys.argv[1] if len(sys.argv) > 1 else '°C'  # Default to Celsius if not provided

# Function to convert temperature
def convert_temperature(temp_kelvin, unit='°C'):
    if temp_kelvin is None:
        return None
    if unit == '°C':
        return temp_kelvin - 273.15  # Convert to Celsius
    else:
        return temp_kelvin  # Return Kelvin by default

def fetch_and_store_weather():
    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if 'main' in data and 'wind' in data:
                temp_kelvin = data['main']['temp']
                temp_converted = convert_temperature(temp_kelvin, temp_unit)
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                condition = data['weather'][0]['main'] if 'weather' in data and len(data['weather']) > 0 else "Unknown"
                
                # Handle possible missing data
                if temp_converted is None or humidity is None or wind_speed is None:
                    print(f"Incomplete weather data for {city}.")
                    continue
                
                # Save to database
                weather_entry = WeatherData(
                    city=city, 
                    temperature=temp_converted, 
                    humidity=humidity, 
                    wind_speed=wind_speed, 
                    condition=condition
                )
                session.add(weather_entry)
                session.commit()

                temp_symbol = "°C" if temp_unit == '°C' else "K"
                print(f"Weather data for {city} stored: {temp_converted:.2f}{temp_symbol}, {humidity}% humidity, {wind_speed:.2f} m/s wind")
            else:
                print(f"Error fetching weather data for {city}: {data.get('message', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed for {city}: {e}")

# Call the function once to fetch data
fetch_and_store_weather()
