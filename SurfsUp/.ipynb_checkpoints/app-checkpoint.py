from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

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
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

@app.route('/')
def home():
    return (
        "Welcome to the Flask API! Available routes:\n"
        "/api/v1.0/precipitation\n"
        "/api/v1.0/stations\n"
        "/api/v1.0/tobs\n"
        "/api/v1.0/<start>\n"
        "/api/v1.0/<start>/<end>"
    )


@app.route('/api/v1.0/precipitation')
def get_precipitation():
    # Query to retrieve the last 12 months of precipitation data
    last_year_date = "2016-08-23"  # Replace with your actual start date
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
    # Replace the following example data with your actual data
    stations = ["USC00519397", "USC00513117", "USC00519281", ...]
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def get_tobs():
    # Perform a query to get temperature observations and return as JSON
    # Replace the following example data with your actual data
    temperature_data = [
        {"date": "2016-01-01", "tobs": 72.0},
        {"date": "2016-01-02", "tobs": 70.0},
        # ...
    ]
    return jsonify(temperature_data)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def get_temperature_range(start, end=None):
    # Perform a query to calculate temperature statistics based on start and end dates
    # Return the calculated statistics as JSON
    # Replace the following example data with your actual data
    temperature_stats = {
        "TMIN": 65.0,
        "TAVG": 72.5,
        "TMAX": 80.0,
    }
    return jsonify(temperature_stats)

if __name__ == '__main__':
    app.run(debug=True)


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
