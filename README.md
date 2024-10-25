**Weather Monitoring Application**

**Objective**

This project aims to develop a real-time data processing system to monitor weather conditions and provide summarized insights using rollups and aggregates. The system fetches weather data at set intervals, processes it, stores it, and provides visual and textual alerts based on user-defined thresholds.

**Tech Stack**
1. Programming Language: Python
2. API: OpenWeatherMap
3. Database: PostgreSQL
4. Visualization: Matplotlib

**Features**
1. Real-time weather data retrieval
2. Data processing and conversion
3. Daily summaries and aggregates
4. Alerting based on user-defined thresholds
5. Visualization of weather data

**Project Structure**

weather_monitoring/
├── weather_fetcher.py         # Fetches weather data from the API
├── alerting.py                # Manages the alerting based on thresholds
├── visualization.py           # Provides visualizations of the weather data
├── forecast_fetcher.py        # Fetches and aggregates forecast information
├── aggregates.py              # Performs data aggregation
└── main.py                    # Main entry point to start the monitoring process

**Prerequisites**
1. Python 3.8+
2. Git
3. Visual Studio Code (VS Code)


**Installation**

Clone the Repository:
command:

git clone (https://github.com/prasanth1367/weather_monitoring.git)

cd weather_monitoring 


**Create and activate a virtual environment**

command:  python -m venv venv

**Activate the environment:**

1. On Windows: venv\Scripts\activate
2. On macOS/Linux: source venv/bin/activate

**Install Dependencies**

command: pip install -r requirements.txt

**Set Up Database**

This project uses PostgreSQL. Set up a PostgreSQL database with connection details configured in the main script or environment variables.

**Configuration**

Temperature Units: The program will prompt for temperature preferences (Celsius or Kelvin) at the start.
Alerts Thresholds: Configure thresholds for temperature and specific weather conditions in alerting.py.

**Running the Application**

Run the Monitoring Program: Start the main program with:

command: python main.py

**After Running the Application:**

Select Temperature Unit:
1. Celsius (°C)
2. Kelvin (K)

**For Alerting** 
1. Enter the temperature threshold:
2. Enter the humidity threshold (percentage):

**After Running the Application**
1. The application will continuously fetch and process weather data based on the specified configurations.
2. Alerts will be generated if temperature or humidity thresholds are met or exceeded.
3. Visualization plots will be available for better data insights.

**Key Features**
1. Real-time Weather Data Retrieval: Continuously fetches weather data for selected locations at specified intervals.
2. Data Processing and Conversion: Converts raw data into meaningful metrics like temperature in Celsius or Kelvin.
3. Daily Summaries and Aggregates: Aggregates weather data daily, providing metrics such as average, maximum, and minimum temperatures, and common weather conditions.
4. Threshold-Based Alerts: Monitors temperature thresholds and generates alerts when specific conditions are met.
5. Data Storage: Uses PostgreSQL to store historical weather data.
6. Visualization: Creates visual representations of the weather data for better insights.
