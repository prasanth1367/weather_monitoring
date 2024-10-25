from database import session, WeatherData
import sys

# Get the temperature unit and thresholds from command-line arguments
temp_unit = sys.argv[1] if len(sys.argv) > 1 else '°C'  # Default to Celsius if not provided
temp_threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 35.0
humidity_threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 80.0

def check_alerts():
    # Adjust temperature threshold based on user preference
    temp_threshold_final = temp_threshold if temp_unit == 'C' else temp_threshold + 273.15  # Convert to Kelvin if needed
    
    # Create sets to track alerts
    alerted_cities_temp = set()
    alerted_cities_humidity = set()
    
    # Alert for high temperature
    high_temp_data = session.query(WeatherData).filter(WeatherData.temperature > temp_threshold_final).all()
    for data in high_temp_data:
        if data.city not in alerted_cities_temp:
            alerted_cities_temp.add(data.city)  # Add to set to avoid duplicate alerts
            if temp_unit == '°C':
                print(f"Alert! {data.city} temperature is above {temp_threshold}°C: {data.temperature:.2f}°C")
            else:
                kelvin_temp = data.temperature + 273.15
                print(f"Alert! {data.city} temperature is above {temp_threshold + 273.15:.2f}K: {kelvin_temp:.2f}K")  # Correct Kelvin conversion

    # Alert for high humidity
    high_humidity_data = session.query(WeatherData).filter(WeatherData.humidity > humidity_threshold).all()
    for data in high_humidity_data:
        if data.city not in alerted_cities_humidity:
            alerted_cities_humidity.add(data.city)  # Add to set to avoid duplicate alerts
            print(f"Alert! {data.city} humidity is above {humidity_threshold}%: {data.humidity}%")

check_alerts()
