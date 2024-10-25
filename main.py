import subprocess
import sys
import time
from datetime import datetime

# Function to prompt the user for temperature unit
def get_temperature_unit():
    print("Select Temperature Unit:")
    print("1. Celsius (°C)")
    print("2. Kelvin (K)")
    choice = input("Enter 1 for Celsius or 2 for Kelvin: ").strip()
    
    if choice == '1':
        return '°C'
    elif choice == '2':
        return 'K'
    else:
        print("Invalid choice! Exiting the program.")
        sys.exit(1)

# Function to prompt the user for weather thresholds
def get_weather_thresholds():
    try:
        temp_threshold = float(input("Enter the temperature threshold: ").strip())
        humidity_threshold = float(input("Enter the humidity threshold (percentage): ").strip())
        return temp_threshold, humidity_threshold
    except ValueError:
        print("Invalid input! Please enter valid numeric values.")
        sys.exit(1)

# Function to prompt the user for re-run settings
def get_rerun_settings():
    rerun_choice = input("Do you want to re-run the scripts automatically? (y/n): ").strip().lower()
    if rerun_choice == 'y':
        try:
            interval = int(input("Enter the time interval between runs (in seconds): ").strip())
            if interval <= 0:
                raise ValueError("Interval must be a positive number.")
            
            rerun_times = input("Enter the number of times to re-run (or press Enter to run indefinitely): ").strip()
            if rerun_times and not rerun_times.isdigit():
                raise ValueError("Invalid number of times for re-run.")
                
            return interval, int(rerun_times) if rerun_times.isdigit() else None
        except ValueError as e:
            print(f"Invalid input: {e}. Exiting the program.")
            sys.exit(1)
    elif rerun_choice == 'n':
        return None, None
    else:
        print("Invalid choice! Exiting the program.")
        sys.exit(1)

# Function to run the weather-related scripts
def run_scripts(temp_unit, temp_threshold, humidity_threshold, output_file, run_count=1):
    scripts = [
        'weather_fetcher.py',
        'alerting.py',
        'forecast_fetcher.py',
        'aggregates.py',
        'visualization.py'
    ]
    
    with open(output_file, 'a', encoding='utf-8', errors='replace') as outfile:  # Open in append mode
        # Write the timestamp of when the data is collected
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_header = f"\n----- Run {run_count} (Temperature Unit: {temp_unit}) -----\n"
        log_time = f"Data collected at: {current_time}\n"
        
        print(log_header)
        print(log_time)
        outfile.write(log_header)
        outfile.write(log_time)
        
        for script in scripts:
            try:
                print(f"Running {script}...")
                outfile.write(f"Running {script}...\n")
                
                # Pass the thresholds and temp_unit to alerting.py as arguments
                if script == 'alerting.py':
                    result = subprocess.run([sys.executable, script, temp_unit, str(temp_threshold), str(humidity_threshold)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    result = subprocess.run([sys.executable, script, temp_unit], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Decode output and display it in the console and log file
                output = result.stdout.decode('utf-8', errors='replace')
                error_output = result.stderr.decode('utf-8', errors='replace')
                
                print(output)  # Print the output to the console
                outfile.write(f"Output of {script}:\n")
                outfile.write(output + "\n")  # Write output to log
                
                # Check if there are any errors and log them only if present
                if result.stderr:
                    print(error_output)  # Print error output to the console
                    outfile.write(f"Errors from {script}:\n")
                    outfile.write(error_output + "\n")  # Write errors to log

                print(f"{script} completed.\n")
                outfile.write(f"{script} completed.\n\n")
            except Exception as e:
                error_message = f"Error running {script}: {e}"
                print(error_message)
                outfile.write(error_message + "\n")

# Main function to run the scripts and handle re-runs
def main():
    # Get temperature unit from the user
    temp_unit = get_temperature_unit()

    # Get user-configurable weather thresholds
    temp_threshold, humidity_threshold = get_weather_thresholds()

    # Get re-run settings (interval and re-run times)
    interval, rerun_times = get_rerun_settings()

    # File to store the output
    output_file = 'output.log'

    # Log initial settings
    with open(output_file, 'a', encoding='utf-8', errors='replace') as outfile:
        outfile.write(f"---- Program Start ----\nTemperature Unit: {temp_unit}\n")
        outfile.write(f"Temperature Threshold: {temp_threshold}\n")
        outfile.write(f"Humidity Threshold: {humidity_threshold}\n")
        if interval is not None:
            outfile.write(f"Re-run Interval: {interval} seconds\n")
            if rerun_times is not None:
                outfile.write(f"Number of Re-runs: {rerun_times}\n")
            else:
                outfile.write(f"Re-run: Indefinite\n")

    # Run the scripts initially
    run_scripts(temp_unit, temp_threshold, humidity_threshold, output_file)
    print(f"Initial run completed. Check the output in {output_file}.")

    # Handle re-runs if applicable
    run_count = 1
    while rerun_times is None or run_count < rerun_times:
        if rerun_times is not None:
            run_count += 1
            print(f"Waiting for {interval} seconds before the next run...")
            time.sleep(interval)
            run_scripts(temp_unit, temp_threshold, humidity_threshold, output_file, run_count)
            print(f"Run {run_count} completed. Check the output in {output_file}.")
        else:
            break

# Run the main function
if __name__ == "__main__":
    main()
