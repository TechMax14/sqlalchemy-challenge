from flask import Flask, jsonify
from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

# Database Setup
# Replace 'sqlite:///your_database_file.db' with your actual database file path
database_path = "C:/Users/fishm/Documents/UT Bootcamp/HW8/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite"
# Create the engine with the adjusted path
engine = create_engine(f"sqlite:///{database_path}")

# Create a connection
connection = engine.connect()

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement  # DO THIS IN PART 1 TOO
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


@app.route('/')
def home():
    return (
        "Welcome to the Flask API! Available routes:<br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/<start><br>"
        "/api/v1.0/<start>/<end>"
    )


@app.route('/api/v1.0/precipitation')
def get_precipitation():
    date_query = text("SELECT MAX(date) FROM measurement")
    most_recent_date = session.execute(date_query).scalar()
    last_year_date = (pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')

    # Query to retrieve the last 12 months of precipitation data
    #last_year_date = "2016-08-23"  # Replace with your actual start date
    precipitation_data = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= last_year_date)
        .all()
    )

    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)


@app.route('/api/v1.0/stations')
def get_stations():
    # Perform a query to get a list of stations and return as JSON
    # Query the list of station names
    station_names = session.query(Station.station).all()

    # Convert the list of tuples to a flat list of strings
    stations = [station[0] for station in station_names]

    return jsonify(stations)


@app.route('/api/v1.0/tobs')
def get_tobs():
    # Perform a query to get temperature observations and return as JSON
    # Calculate the date one year ago from the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = datetime.strptime(most_recent_date, "%Y-%m-%d")
    one_year_ago = most_recent_date - timedelta(days=365)

    # Query the most-active station
    most_active_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.id).desc()).first()[0]

    # Query temperature observations for the most active station in the last 12 months
    temperature_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a list of dictionaries
    temperature_data_dict = [{"date": date, "tobs": tobs} for date, tobs in temperature_data]

    return jsonify(temperature_data_dict)


@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def get_temperature_range(start, end=None):
    # Perform a query to calculate temperature statistics based on start and end dates
    # Convert start and end dates to datetime objects
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d") if end else None
    
    # Query temperature statistics based on start and end dates
    query = session.query(
        func.min(Measurement.tobs).label("TMIN"),
        func.avg(Measurement.tobs).label("TAVG"),
        func.max(Measurement.tobs).label("TMAX")
    ).filter(Measurement.date >= start_date)
    
    if end_date:
        query = query.filter(Measurement.date <= end_date)
    
    temperature_stats = query.one()
    
    # Convert the query result to a dictionary
    temperature_stats_dict = {
        "TMIN": temperature_stats.TMIN,
        "TAVG": temperature_stats.TAVG,
        "TMAX": temperature_stats.TMAX
    }
    
    return jsonify(temperature_stats_dict)

if __name__ == '__main__':
    app.run(debug=True)
