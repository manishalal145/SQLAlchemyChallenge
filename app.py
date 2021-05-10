# import dependencies
from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt
from datetime import date, timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# SQLAlchemy
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)
Base.classes.keys()

# Reference the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask
app = Flask(__name__)

# dates
session = Session(engine)
latest_date = session.query(Measurement.date) \
                     .order_by(Measurement.date.desc()).first()
one_year = dt.datetime.strptime(*latest_date,"%Y-%m-%d") - timedelta(days=365)
session.close()

# Flask routes
# Home route
@app.route("/")
def welcome():
    return """
        <style>
            h1 {text-align : center}
            h2 {text-align : center}
            ul {list-style-position : inside}
            li {list-style-position : inside}
            .div {text-align : center}
            .inline {display : inline-block; text-align : left;}
        </style>
        <h1>Welcome to the Hawaii!</h1><br/>
        <h2><bold>Available routes:</bold></h2><br/>
        <div class="div">
            <div class="inline">
                <ul>
                    <li><a href="/api/v1.0/precipitation" target="_blank">/api/v1.0/precipitation</a></li>
                    <li><a href="/api/v1.0/stations" target="_blank">/api/v1.0/stations</a></li>
                    <li><a href="/api/v1.0/tobs" target="_blank">/api/v1.0/tobs</a></li>
                    <li><a href="/api/v1.0/yyyymmdd" target="_blank">/api/v1.0/start </a></li>
                    <li><a href="/api/v1.0/yyyymmdd/yyyymmdd" target="_blank">/api/v1.0/start/end </a></li>
                </ul>
            </div>
        </div>
    """

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Return a JSON List of Stations From the Dataset
        session = Session(engine)
        stations_all = session.query(Station.station, Station.name).all()
        session.close()
        # Convert List of Tuples Into Normal List
        station_list = list(np.ravel(stations_all))
        # Return a JSON List of Stations from the Dataset
        return jsonify(station_list)

# Station route
@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()
    # Convert List of Tuples Into Normal List
    station_list = list(np.ravel(results))
    # Return JSON List of Temperature Observations (tobs) for the Previous Year
    return jsonify(station_list)

# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # most_active_stations
    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).first()
    # Query for the Dates and Temperature Observations from a Year from the Last Data Point
    results = session.query(Measurement.date, Measurement.tobs) \
               .filter(Measurement.station == most_active_stations.station) \
               .filter(Measurement.date >= dt.datetime.strftime(one_year,"%Y-%m-%d")) \
               .order_by(Measurement.date) \
               .all()

    session.close()
    # Convert List of Tuples Into Normal List
    tobs_list = list(np.ravel(results))
    # Return JSON List of Temperature Observations (tobs) for the Previous Year
    return jsonify(tobs_list)

# Start Date route
@app.route("/api/v1.0/<start>")
def start_day(start):
   session = Session(engine)
   start_day = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
   session.close()
   # Convert List of Tuples Into Normal List
   start_day_list = list(np.ravel(start_day))
   # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
   return jsonify(start_day_list)

# Start Date and End Date route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    start_end_day = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    session.close()
    # Convert List of Tuples Into Normal List
    start_end_day_list = list(np.ravel(start_end_day))
    # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
    return jsonify(start_end_day_list)

# Main
if __name__ == "__main__":
    app.run(debug=True)