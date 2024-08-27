# Surf_Cast
### Overview
Surf_Cast is a web application designed to provide surfers and beachgoers with real-time surf and tide forecasts for various beaches in San Diego, California. By leveraging data from NOAA and Surfline, the app delivers accurate and up-to-date information on surf height, wind speed, swell data, and tide predictions. The project is built using Python, Flask, SQLite, and Matplotlib for data visualization.

### Features
1. Surf Forecasts: Displays detailed surf conditions, including surf height, wind speed, and swell data for selected beaches.
2. Tide Predictions: Provides hourly tide height predictions for multiple locations in San Diego.
3. Interactive Graphs: Visualizes surf and tide data over time with clear, easy-to-read line graphs.
4. Database Integration: Stores surf and tide data in a SQLite database for quick retrieval and analysis.
5. User-Friendly Interface: Clean and responsive web pages for viewing forecasts, raw data, and graphical reports.
6. Customizable Views: Users can view detailed forecasts for individual beaches, including specific surf and tide conditions.
   
### Project Structure
- app.py: The main Flask application file that routes the web requests and renders the pages.
- create_database.py: Script to create and populate the SQLite database with surf forecast data.
- tide_data.py: Script to fetch and store tide prediction data from NOAA.
- read_database.py: Utility script for reading data from the SQLite database.
- surf_forecast.db: SQLite database storing surf forecast data.
- tide_data.db: SQLite database storing tide prediction data.
- templates: Directory containing HTML templates (index.html, beach.html, raw_data.html) for rendering web pages.
- static: Directory containing static assets like JavaScript files and CSS for the web interface.
- venv: Python virtual environment directory containing installed dependencies.

### Installation Prerequisites
- Python 3.x
- Flask
- SQLite
- Matplotlib
- pysurfline

Surf Forecaster:
![image](https://github.com/user-attachments/assets/d59ea547-1a13-4d99-a90c-e6987c177b73)

![image](https://github.com/user-attachments/assets/57e667d6-14bd-498e-ab4d-13d44cfa7ad5)


