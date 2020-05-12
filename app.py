from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
import numpy as np
import datetime as dt

from flask import Flask, jsonify

# sqlalchemy need a primary key
# database setup
conn_str  = 'sqlite:///Resources/hawaii.sqlite'
conn = create_engine(conn_str)

# create base class for reflection
Base = automap_base()

# reflect tables in database
Base.prepare(conn,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# create flask app
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def homepage():
    """List of all returnable API routes."""
    return(
        f"(Note: Dates range from 2010-01-01 to 2017-08-23). <br><br>"
        f"Available Routes: <br>"

        f"/api/v1.0/precipitation<br/>"
        f"Returns dates and temperature from the last year. <br><br>"

        f"/api/v1.0/stations<br/>"
        f"Returns a json list of stations. <br><br>"

        f"/api/v1.0/tobs<br/>"
        f"Returns list of Temperature Observations(tobs) for previous year. <br><br>"

        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given start date.<br><br>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given date range."
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(bind=conn)

    # Query for the dates and precipitation values
    results =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    prcp_date_list = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        prcp_date_list.append(new_dict)

    session.close()

    return jsonify(prcp_date_list)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(bind=conn)

    # Query for the dates and precipitation values
    results =  session.query(Station.station, Station.name).all()

    # Convert to list of dictionaries to jsonify
    station_list = []

    for station, name in results:
        new_dict = {}
        new_dict[station] = name
        station_list.append(new_dict)

    session.close()

    return jsonify(station_list)

# Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def date_temp_activestation():
    # Create our session (link) from Python to the DB
    session = Session(bind=conn)

    # Get the last date contained in the dataset and date from one year ago
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    # Query for the dates and temperature values
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= last_year_date).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    tobs_date_list = []

    for date, tobs in results:
        new_dict = {}
        new_dict[date] = tobs
        tobs_date_list.append(new_dict)

    session.close()

    return jsonify(tobs_date_list)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_stats(start=None, end=None):
    
    session = Session(bind=conn)

    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # end date 
    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
  
    return jsonify(results)



# start app
if __name__ == '__main__':
    app.run(debug=True)