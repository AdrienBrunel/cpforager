# seabird-movement-cpf
Python code to handle GPS data gathered from biologgers attached to central-place foraging seabirds. The idea is to make movement ecology data a bit easier to process.

# GPS
## constructor
GPS(df, group, id, params) : 
* *df* is a pandas DataFrame containing "datetime", "longitude" and "latitude" columns. Type of "datetime" column must be converted to datetime64.
* *group* is a string representing the group to which the data belongs (year, fieldwork, specie, etc.) which can be relevant for future statistics.
* *id* is a string representing the unique identifier of the central-place foraging seabird.
* *params* is the list of parameters that should at least include the fields present in parameters.py.

The resulting GPS object add columns to the DataFrame for step metrics of the GPS data but also the central-place foraging trip statistics. See the documentation for more details.

## methods
* *display_data_summary* : display a summary of the GPS data.
* *full_diag* : produce a full png diagnostic showing the GPS data.
* *maps_diag* : produce the png maps showing the GPS data.
* *folium_map* : produce the html map showing the GPS data.
* *folium_map_colorgrad* : produce the html map showing the GPS data with a speed color gradient.


# GPS_Collection
## constructor
GPS_Collection(gps_collection)
* *gps_collection* is a list of GPS object.

## methods
* *display_data_summary* : display a summary of the GPS collection.
* *plot_stats_summary* : produce the png showing the trip statistics of the GPS collection.
* *maps_diag* : produce the png map showing all the trips in the GPS collection.
* *folium_map* : produce the html map showing all the trips in the GPS collection.


# Infos
Python version used is 3.11.5
OS used is Ubuntu 18.04
