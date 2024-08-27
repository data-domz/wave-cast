import sqlite3
import pandas as pd
import requests

# NOAA API endpoint
NOAA_API_URL = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"

# List of station IDs and corresponding spot names
stations = {
    '9410230': 'La Jolla Shores',
    '9410170': 'San Diego',
    '9410120': 'Imperial Beach',
    # Add more stations as needed
}

# Function to fetch tide data from NOAA
def fetch_tide_data(station_id, begin_date, end_date):
    params = {
        'station': station_id,
        'begin_date': begin_date,
        'end_date': end_date,
        'product': 'predictions',
        'datum': 'MLLW',
        'units': 'metric',
        'time_zone': 'lst_ldt',
        'format': 'json',
        'interval': 'hilo'
    }
    response = requests.get(NOAA_API_URL, params=params)
    data = response.json()
    return pd.DataFrame(data['predictions'])

# Function to create and populate SQLite database
def create_tide_database(db_name='tide_data.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tides (
            id INTEGER PRIMARY KEY,
            station_name TEXT,
            timestamp TEXT,
            tide_height REAL
        )
    ''')

    # Fetch and insert data for each station
    for station_id, station_name in stations.items():
        tide_data = fetch_tide_data(station_id, '20240827', '20240828')  # Example dates
        tide_data['station_name'] = station_name
        tide_data['timestamp'] = pd.to_datetime(tide_data['t']).dt.strftime('%Y-%m-%d %H:%M:%S')
        tide_data['tide_height'] = tide_data['v'].astype(float)

        tide_data = tide_data[['station_name', 'timestamp', 'tide_height']]
        tide_data.to_sql('tides', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    print(f"Database {db_name} created and populated successfully.")

if __name__ == '__main__':
    create_tide_database()
