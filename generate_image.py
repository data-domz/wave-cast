import pandas as pd
import pysurfline
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

# List of spot IDs and their corresponding names for San Diego beaches
spots = {
    '5842041f4e65fad6a77088cc': 'La Jolla Shores',
    '5842041f4e65fad6a7708841': 'Pacific Beach',
    '5842041f4e65fad6a770883f': 'Ocean Beach',
    '5842041f4e65fad6a7708842': 'Mission Beach',
    '5842041f4e65fad6a770883c': 'Windansea Beach',
    '5842041f4e65fad6a770883b': 'Blacks Beach',
    '5842041f4e65fad6a7708844': 'Imperial Beach',
    '5842041f4e65fad6a7708839': 'Scripps Pier',
    '5842041f4e65fad6a77088ce': 'Coronado Beach',
}

def save_surf_report(spot_name):
    # Normalize spot_name to match the keys in spots dictionary
    normalized_spot_name = spot_name.lower()
    spot_id = next((key for key, value in spots.items() if value.lower() == normalized_spot_name), None)
    
    if not spot_id:
        print(f"Spot ID not found for {spot_name}")
        return

    # Fetch the forecast data for the specific spot
    spot_forecasts = pysurfline.get_spot_forecasts(
        spotId=spot_id,
        days=1,
        intervalHours=2,
    )

    # Convert the forecast data to a DataFrame and adjust the timestamp using utcOffset
    df = spot_forecasts.get_dataframe()
    
    if 'utcOffset' in df.columns:
        df['timestamp_dt'] = pd.to_datetime(df['timestamp_dt'])
        df['local_time'] = df['timestamp_dt'] + pd.to_timedelta(df['utcOffset'], unit='h')
        df['local_time_str'] = df['local_time'].dt.strftime('%H:%M')  # Convert to string format for plotting

    # Plot using the adjusted local times
    plt.figure(figsize=(12, 6))
    plt.bar(df['local_time_str'], df['surf_min'], color='blue', label='Min Surf')
    plt.bar(df['local_time_str'], df['surf_max'], color='lightblue', alpha=0.5, label='Max Surf')
    plt.title(f'{spot_name}')
    plt.xlabel('Time')
    plt.ylabel('Surf Height (m)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Define the path for saving the image
    img_path = os.path.join('static/reports', f'{spot_name}_surf_report.png')
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(img_path), exist_ok=True)

    # Save the current figure using matplotlib
    plt.savefig(img_path)
    
    # Clear the plot to free up memory
    plt.clf()

    print(f"Surf report saved at {img_path}")

if __name__ == '__main__':
    # Loop through all the spots and save their surf reports
    for spot_name in spots.values():
        save_surf_report(spot_name)
