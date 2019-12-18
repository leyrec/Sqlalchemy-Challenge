# Dependencies and Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Communicate with the DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing DB into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session to link DB with Python through the engine
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Create an app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# List all the available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        
    )

# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
 
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the query results to a dictionary using `date` as the Key and `prcp` as the Value
        # Calculate the date 1 year ago from the last data point in the database
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a query to retrieve the last 12 months of precipitation data using `date` as the Key and `prcp` as the Value
        precipitation_data= session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
        # Convert list of tuples into a dictionary
        precipitation_list = dict(precipitation_data)
        # Return JSON representation of dictionary
        return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
        # Query for the total of stations (id) and names 
        total_stations = session.query(Station.station, Station.name).all()
        # Convert the query results from list of tuples into normal list
        station_list = list(np.ravel(total_stations))
        # Return JSON list of stations from the dataset
        return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the dates and temperature observations from a year from the last data point.
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a query to retrieve the last 12 months of temperature data using `date` as the Key and `tobs` as the Value
        temperature_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert the query results from list of tuples into normal list
        temperature_list = list(np.ravel(temperature_data))
        # Return a JSON list of Temperature Observations (tobs) for the previous year
        return jsonify(temperature_list)


@app.route("/api/v1.0/<start>")
def start_day(start):
        # Query the minimum temperature, the average temperature, and the max temperature for a given start range.
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert the query results from list of tuples into normal list
        startday_list = list(np.ravel(start_day))
        # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range.
        return jsonify(startday_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        # Query the minimum temperature, the average temperature, and the max temperature for a given start-end range.
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert the query results from list of tuples into normal list
        start_end_day_list = list(np.ravel(start_end_day))
        # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
        return jsonify(start_end_day_list)




if __name__ == '__main__':
    app.run(debug=True)