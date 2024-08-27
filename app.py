from flask import Flask, jsonify, render_template, send_file
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import io
import pysurfline

app = Flask(__name__)

# Define the spot IDs and names for San Diego beaches (reuse from create_database.py)
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

# Function to read data from the SQLite database
def read_database(query, db_name='surf_forecast.db'):
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/surf-forecast', methods=['GET'])
def get_surf_forecast():
    query = """
        SELECT 
            spot_name,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN surf_raw_min END) as morning_surf_raw_min,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN surf_raw_max END) as morning_surf_raw_max,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN speed * 1.94384 END) as morning_speed_kts,  -- Convert to knots
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN direction END) as morning_direction,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN power END) as morning_power,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_0_height END) as morning_swells_0_height,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_0_period END)) as morning_swells_0_period,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_0_impact END) as morning_swells_0_impact,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_0_direction END)) as morning_swells_0_direction,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_1_height END) as morning_swells_1_height,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_1_period END)) as morning_swells_1_period,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_1_impact END) as morning_swells_1_impact,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_1_direction END)) as morning_swells_1_direction,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_2_height END) as morning_swells_2_height,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_2_period END)) as morning_swells_2_period,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_2_impact END) as morning_swells_2_impact,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN swells_2_direction END)) as morning_swells_2_direction,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '06' AND '11' THEN temperature END) as morning_temperature,

            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN surf_raw_min END) as afternoon_surf_raw_min,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN surf_raw_max END) as afternoon_surf_raw_max,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN speed * 1.94384 END) as afternoon_speed_kts,  -- Convert to knots
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN direction END) as afternoon_direction,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN power END) as afternoon_power,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_0_height END) as afternoon_swells_0_height,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_0_period END)) as afternoon_swells_0_period,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_0_impact END) as afternoon_swells_0_impact,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_0_direction END)) as afternoon_swells_0_direction,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_1_height END) as afternoon_swells_1_height,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_1_period END)) as afternoon_swells_1_period,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_1_impact END) as afternoon_swells_1_impact,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_1_direction END)) as afternoon_swells_1_direction,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_2_height END) as afternoon_swells_2_height,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_2_period END)) as afternoon_swells_2_period,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_2_impact END) as afternoon_swells_2_impact,
            ROUND(AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN swells_2_direction END)) as afternoon_swells_2_direction,
            AVG(CASE WHEN strftime('%H', timestamp_dt) BETWEEN '12' AND '17' THEN temperature END) as afternoon_temperature
        FROM forecasts
        GROUP BY spot_name
    """
    df = read_database(query)
    
    # Convert wind direction and swell directions to compass points
    df['morning_direction'] = df['morning_direction'].apply(convert_to_compass)
    df['afternoon_direction'] = df['afternoon_direction'].apply(convert_to_compass)
    df['morning_swells_0_direction'] = df['morning_swells_0_direction'].apply(convert_to_compass)
    df['afternoon_swells_0_direction'] = df['afternoon_swells_0_direction'].apply(convert_to_compass)
    df['morning_swells_1_direction'] = df['morning_swells_1_direction'].apply(convert_to_compass)
    df['afternoon_swells_1_direction'] = df['afternoon_swells_1_direction'].apply(convert_to_compass)
    df['morning_swells_2_direction'] = df['morning_swells_2_direction'].apply(convert_to_compass)
    df['afternoon_swells_2_direction'] = df['afternoon_swells_2_direction'].apply(convert_to_compass)
    
    return jsonify(df.to_dict(orient='records'))

def convert_to_compass(degrees):
    if pd.isnull(degrees):
        return "N/A"
    val = int((degrees / 22.5) + 0.5)
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return f"{int(degrees)}° {directions[val % 16]}"

@app.route('/beach/<spot_name>')
def beach(spot_name):
    query = f"SELECT * FROM forecasts WHERE spot_name='{spot_name}'"
    df = read_database(query)
    df['timestamp_dt'] = pd.to_datetime(df['timestamp_dt'])
    df['time'] = df['timestamp_dt'].dt.strftime('%H:%M')

    grouped_data = df.groupby('time').agg({
        'surf_raw_min': lambda x: round(x.iloc[0], 1),
        'surf_raw_max': lambda x: round(x.iloc[0], 1),
        'speed': lambda x: round(x.iloc[0], 1),
        'direction': lambda x: round(x.iloc[0]),
        'optimalScore': lambda x: round(x.iloc[0], 1),
        'power': lambda x: round(x.iloc[0], 1),
        'probability': lambda x: round(x.iloc[0], 1),
        'swells_0_height': 'first',
        'swells_0_period': lambda x: round(x.iloc[0]),
        'swells_1_height': 'first',
        'swells_1_period': lambda x: round(x.iloc[0]),
        'swells_2_height': 'first',
        'swells_2_period': lambda x: round(x.iloc[0]),
        'swells_3_height': 'first',
        'swells_3_period': lambda x: round(x.iloc[0]),
        'swells_4_height': 'first',
        'swells_4_period': lambda x: round(x.iloc[0]),
        'swells_5_height': 'first',
        'swells_5_period': lambda x: round(x.iloc[0]),
    }).reset_index()

    return render_template('beach.html', spot_name=spot_name, beach_data=grouped_data.to_dict(orient='records'))

@app.route('/raw-data')
def raw_data():
    query = "SELECT * FROM forecasts"
    df = read_database(query)
    
    # Drop the 'timestamp_timestamp' column
    df = df.drop(columns=['timestamp_timestamp'])
    
    # Reorder the columns to move 'spot_name' to the second position
    columns = ['timestamp_dt', 'spot_name'] + [col for col in df.columns if col not in ['timestamp_dt', 'spot_name']]
    df = df[columns]
    
    # Convert the DataFrame to HTML
    data_html = df.to_html(classes='table table-striped table-dark', index=False)
    
    return render_template('raw_data.html', data=data_html)

@app.route('/beach/<spot_name>/surf-report')
def surf_report(spot_name):
    # Find the corresponding spot ID for the given spot_name
    spot_id = None
    for key, value in spots.items():
        if value.lower() == spot_name.lower():
            spot_id = key
            break
    
    if not spot_id:
        raise ValueError(f"Spot ID not found for {spot_name}")

    # Fetch the forecast data for the specific spot
    spot_forecasts = pysurfline.get_spot_forecasts(
        spotId=spot_id,
        days=1,
        intervalHours=2,
    )
    
    # Use the plot_surf_report function
    img = io.BytesIO()
    pysurfline.plot_surf_report(
        spot_forecasts,
        barLabels=True,
        wind=True,
        savepath=img
    )
    img.seek(0)

    return send_file(img, mimetype='image/png')

@app.route('/beach/<spot_name>/plot')
def beach_plot(spot_name):
    query = f"SELECT * FROM forecasts WHERE spot_name='{spot_name}'"
    df = read_database(query)
    df['timestamp_dt'] = pd.to_datetime(df['timestamp_dt'])
    tomorrow_date = pd.Timestamp('2024-08-28')
    beach_tomorrow = df[df['timestamp_dt'].dt.date == tomorrow_date.date()]

    beach_tomorrow = beach_tomorrow.copy()
    beach_tomorrow.loc[:, 'time'] = beach_tomorrow['timestamp_dt'].dt.strftime('%H:%M')

    # Create subplots with spacing between them
    fig, axs = plt.subplots(2, 2, figsize=(13, 9), facecolor='black')
    fig.suptitle(f'{spot_name} - Surf Forecast for {tomorrow_date.date()}', fontsize=20, color='white')

    # Adjust subplot spacing to create visible black lines between plots
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.5, hspace=0.5)

    # Average Surf Height Over Time
    axs[0, 0].plot(beach_tomorrow['time'], (beach_tomorrow['surf_raw_min'] + beach_tomorrow['surf_raw_max']) / 2, label='Avg Surf Height', color='blue')
    axs[0, 0].set_title('Average Surf Height Over Time', color='white')
    axs[0, 0].set_xlabel('Time', color='white')
    axs[0, 0].set_ylabel('Surf Height (ft)', color='white')
    axs[0, 0].legend()
    axs[0, 0].grid(True)
    axs[0, 0].tick_params(axis='x', colors='white', rotation=45)
    axs[0, 0].tick_params(axis='y', colors='white')
    axs[0, 0].spines['bottom'].set_color('white')
    axs[0, 0].spines['top'].set_color('white')
    axs[0, 0].spines['left'].set_color('white')
    axs[0, 0].spines['right'].set_color('white')

    # Wind Speed and Direction Over Time
    axs[0, 1].plot(beach_tomorrow['time'], beach_tomorrow['speed'], label='Wind Speed', color='orange')
    axs[0, 1].set_title('Wind Speed and Direction Over Time', color='white')
    axs[0, 1].set_xlabel('Time', color='white')
    axs[0, 1].set_ylabel('Wind Speed (mph)', color='white')
    axs[0, 1].legend(loc='upper left')
    axs[0, 1].grid(True)
    axs[0, 1].tick_params(axis='x', colors='white', rotation=45)
    axs[0, 1].tick_params(axis='y', colors='white')
    axs[0, 1].spines['bottom'].set_color('white')
    axs[0, 1].spines['top'].set_color('white')
    axs[0, 1].spines['left'].set_color('white')
    axs[0, 1].spines['right'].set_color('white')

    ax2b = axs[0, 1].twinx()
    ax2b.plot(beach_tomorrow['time'], beach_tomorrow['direction'], label='Wind Direction', color='green')
    ax2b.set_ylabel('Wind Direction (degrees)', color='white')
    ax2b.legend(loc='upper right')
    ax2b.tick_params(axis='y', colors='white')
    ax2b.spines['bottom'].set_color('white')
    ax2b.spines['top'].set_color('white')
    ax2b.spines['left'].set_color('white')
    ax2b.spines['right'].set_color('white')

    # Swells (0-5) Height Over Time
    swell_colors = ['purple', 'blue', 'green', 'red', 'cyan', 'magenta']
    for i in range(6):
        axs[1, 0].plot(beach_tomorrow['time'], beach_tomorrow[f'swells_{i}_height'], label=f'Swell {i} Height', color=swell_colors[i])
    axs[1, 0].set_title('Swells (0-5) Height Over Time', color='white')
    axs[1, 0].set_xlabel('Time', color='white')
    axs[1, 0].set_ylabel('Swell Height (ft)', color='white')
    axs[1, 0].legend()
    axs[1, 0].grid(True)
    axs[1, 0].tick_params(axis='x', colors='white', rotation=45)
    axs[1, 0].tick_params(axis='y', colors='white')
    axs[1, 0].spines['bottom'].set_color('white')
    axs[1, 0].spines['top'].set_color('white')
    axs[1, 0].spines['left'].set_color('white')
    axs[1, 0].spines['right'].set_color('white')

    # Power Over Time
    axs[1, 1].plot(beach_tomorrow['time'], beach_tomorrow['power'], label='Power', color='red')
    axs[1, 1].set_title('Power Over Time', color='white')
    axs[1, 1].set_xlabel('Time', color='white')
    axs[1, 1].set_ylabel('Power', color='white')
    axs[1, 1].legend()
    axs[1, 1].grid(True)
    axs[1, 1].tick_params(axis='x', colors='white', rotation=45)
    axs[1, 1].tick_params(axis='y', colors='white')
    axs[1, 1].spines['bottom'].set_color('white')
    axs[1, 1].spines['top'].set_color('white')
    axs[1, 1].spines['left'].set_color('white')
    axs[1, 1].spines['right'].set_color('white')

    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])

    img = io.BytesIO()
    plt.savefig(img, format='png', facecolor=fig.get_facecolor())
    img.seek(0)
    plt.close(fig)  # Close the figure to free memory

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
