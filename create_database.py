import sqlite3
import pandas as pd
import pysurfline

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
    '5842041f4e65fad6a7708840': 'Sunset Cliffs'
}

# Function to fetch forecast data
def fetch_forecast_data():
    all_forecasts = []
    for spot_id, spot_name in spots.items():
        spot_forecasts = pysurfline.get_spot_forecasts(
            spotId=spot_id,
            days=2,
            intervalHours=2,
        )
        forecast_data = spot_forecasts.get_dataframe()
        forecast_data['spot_name'] = spot_name  # Add spot name to the data
        all_forecasts.append(forecast_data)
    
    all_forecasts_df = pd.concat(all_forecasts, ignore_index=True)
    return all_forecasts_df

# Function to create and populate SQLite database
def create_database(db_name='surf_forecast.db'):
    # Fetch the data
    df = fetch_forecast_data()
    
    # Create a SQLite database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY,
            spot_name TEXT,
            timestamp_dt TEXT,
            timestamp_timestamp INTEGER,
            probability REAL,
            utcOffset INTEGER,
            surf_min REAL,
            surf_max REAL,
            surf_optimalScore INTEGER,
            surf_plus BOOLEAN,
            surf_humanRelation TEXT,
            surf_raw_min REAL,
            surf_raw_max REAL,
            power REAL,
            swells_0_height REAL,
            swells_0_period INTEGER,
            swells_0_impact REAL,
            swells_0_power REAL,
            swells_0_direction REAL,
            swells_0_directionMin REAL,
            swells_0_optimalScore INTEGER,
            swells_1_height REAL,
            swells_1_period INTEGER,
            swells_1_impact REAL,
            swells_1_power REAL,
            swells_1_direction REAL,
            swells_1_directionMin REAL,
            swells_1_optimalScore INTEGER,
            swells_2_height REAL,
            swells_2_period INTEGER,
            swells_2_impact REAL,
            swells_2_power REAL,
            swells_2_direction REAL,
            swells_2_directionMin REAL,
            swells_2_optimalScore INTEGER,
            swells_3_height REAL,
            swells_3_period INTEGER,
            swells_3_impact REAL,
            swells_3_power REAL,
            swells_3_direction REAL,
            swells_3_directionMin REAL,
            swells_3_optimalScore INTEGER,
            swells_4_height REAL,
            swells_4_period INTEGER,
            swells_4_impact REAL,
            swells_4_power REAL,
            swells_4_direction REAL,
            swells_4_directionMin REAL,
            swells_4_optimalScore INTEGER,
            swells_5_height REAL,
            swells_5_period INTEGER,
            swells_5_impact REAL,
            swells_5_power REAL,
            swells_5_direction REAL,
            swells_5_directionMin REAL,
            swells_5_optimalScore INTEGER,
            speed REAL,
            direction REAL,
            directionType TEXT,
            gust REAL,
            optimalScore INTEGER,
            temperature REAL,
            condition TEXT,
            pressure INTEGER
        )
    ''')
    
    # Insert data into table
    df.to_sql('forecasts', conn, if_exists='replace', index=False)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print(f'Database {db_name} created and populated successfully.')

if __name__ == '__main__':
    create_database()
