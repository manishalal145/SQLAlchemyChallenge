# SQLAlchemy Homework - Surfs Up!

![surfs-up.png](Images/surfs-up.png)

## Background <br/>
This repository is designed to make a climate analysis on Honolulu, Hawaii, to help clients trip planning, and outline when they can plan their vacation.


## Step 1 - Climate Analysis and Exploration

To begin, used Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database. All of the following analysis completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Python SQL toolkit and Object Relational Mapper<br/>
 -- import sqlalchemy<br/>
 -- from sqlalchemy.ext.automap import automap_base<br/>
 -- from sqlalchemy.orm import Session<br/>
 -- from sqlalchemy import create_engine, func<br/>

* SQLAlchemy engine created create_engine to connect to the sqlite database.<br/>
  engine = create_engine("sqlite:///hawaii.sqlite")

* To reflect the tables into classes, and save a reference to those classes called Station and Measurement.<br/>
  Base = automap_base()<br/>
  Measurement = Base.classes.measurement<br/>
  Station = Base.classes.station<br/>

* Create our session (link) from Python to the DB<br/>
  session = Session(engine)<br/>

### Precipitation Analysis

* Designed a query to retrieve the last 12 months of precipitation data.Selected only the `date` and `prcp` values.<br/>
![surfs-up.png](Images/image1.png)

* Loaded the query results into a Pandas DataFrame and set the index to the date column.<br/>
![surfs-up.png](Images/image2.png)

* Sort the DataFrame values by `date`.<br/>
![surfs-up.png](Images/image3.png)

* Plot the results using the DataFrame `plot` method.</br>
![precipitation](Images/PrecipitationAnalysis.png)

* Used Pandas to print the summary statistics for the precipitation data.</br>
![precipitation](Images/image4.png)


### Station Analysis

* Designed a query to calculate the total number of stations.<br/>
![precipitation](Images/image5.png)

* Designed a query to find the most active stations.<br/>
![precipitation](Images/image6.png)


* Designed a query to retrieve the last 12 months of temperature observation data (TOBS) of the most active station and plotted the results as a histogram with `bins=12`.<br/>
![station-histogram](Images/Temperature_vs_Frequency.png)

- - -

## Step 2 - Climate App

* Used Flask to create routes which are as follow:

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of the dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.
  

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculated `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculated the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
