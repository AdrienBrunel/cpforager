# seabird-movement-cpf
Python code to manipulate data collected from biologgers attached to central-place foraging seabirds. The idea is to make movement ecology data a bit easier to process.

<br />

# User guide 
* In the `parameters.py` script, the `get_params(colony)` function produces a dictionary of parameters. This dictionary is required as an argument in the `GPS`, `GPS_Collection` and `AXY` classes. Users can modify the following parameters :

name                        | description
--------------------------- | ----------------------
`colony`                    | longitude/latitude bounding box inside which the searbird's nest is to be found. 
`local_tz`                  | local timezone of the seabird's nest.
`max_possible_speed`        | speed threshold in km/h above which a longitude/latitude measure can be considered as an error and will be deleted.
`dist_threshold`            | distance from the nest threshold in km above which the seabird is considered in a foraging trip.
`speed_threshold`           | speed threshold in km/h above which the seabird is still considered in a foraging trip despite being below the distance threshold.
`nesting_speed`             | speed threshold in km/h below which the seabird is considered at nest.
`trip_min_duration`         | duration in seconds above which a trip is valid.
`trip_max_duration`         | duration in seconds below which a trip is valid.
`trip_min_length`           | length in km above which a trip is valid.
`trip_max_length`           | length in km below which a trip is valid.
`trip_min_steps`            | number of steps above which a trip is valid.
`diving_depth_threshold`    | set the depth threshold above which a seabird is considered to be diving.

* In the `test` folder, the `test.py` script illustrates how the `GPS`, `GPS_Collection` and `AXY` classes should be used to fully benefit the users. Results of this script is also found in the `test` folder.

<br />

# GPS
Constructor `GPS(df, group, id, params)` : 
* `df` is a pandas DataFrame containing ***datetime***, ***longitude*** and ***latitude*** columns. The user must input the ***datetime*** at the local timezone and converted to `datetime64` type (see `test.py`).
* `group` is a string representing the group to which the data belongs (year, fieldwork, specie, etc.) which can be relevant for future statistics.
* `id` is a string representing the unique identifier of the central-place foraging seabird.
* `params` is the list of parameters that should at least include the fields present in parameters.py.

The resulting GPS object adds step metrics to the initial DataFrame but also provides the central-place foraging trip statistics. See the documentation for more details.

methods                | description
---------------------- | ----------------------
`display_data_summary` | display a summary of the GPS data.
`full_diag`            | produce a full png diagnostic showing the GPS data.
`maps_diag`            | produce the png maps showing the GPS data.
`folium_map`           | produce the html map showing the GPS data.
`folium_map_wtrips`    | produce the html map showing the GPS data with trip colors.
`folium_map_colorgrad` | produce the html map showing the GPS data with a speed color gradient.
`interpolate_lat_lon`  | produce the interpolated dataframe along a desired datetime numpy array.

# GPS_Collection
Constructor `GPS_Collection(gps_collection)`
* `gps_collection` is an array of GPS object.

The resulting GPS_Collection object allows to handle several GPS biologgers at once to produce overall central-place foraging trip statistics and relevant plots. See the documentation for more details.

methods                | description
---------------------- | ----------------------
`display_data_summary` | display a summary of the GPS collection.
`plot_stats_summary`   | produce the png showing the trip statistics of the GPS collection.
`maps_diag`            | produce the png map showing all the trips in the GPS collection.
`folium_map`           | produce the html map showing all the trips in the GPS collection.

# TDR
Constructor `TDR(df, group, id, params)` : 
* `df` is a pandas DataFrame containing ***datetime***, ***pressure*** and ***temperature*** columns. The user must input the ***datetime*** at the local timezone and converted to `datetime64` type (see `test.py`).
* `group` is a string representing the group to which the data belongs (year, fieldwork, specie, etc.) which can be relevant for future statistics.
* `id` is a string representing the unique identifier of the central-place foraging seabird.
* `params` is the list of parameters that should at least include the fields present in parameters.py.

The resulting TDR object adds segmented dives to the initial DataFrame. See the documentation for more details.

methods                | description
---------------------- | ----------------------
`display_data_summary` | display a summary of the TDR data.
`full_diag`            | produce a full png diagnostic showing the TDR data.

# AXY
Constructor `AXY(df, group, id, params)` : 
* `df` is a pandas DataFrame containing ***datetime***, ***longitude***, ***latitude***, ***ax***, ***ay*** and ***az*** columns. The user must input the ***datetime*** at the local timezone and converted to `datetime64` type (see `test.py`).
* `group` is a string representing the group to which the data belongs (year, fieldwork, specie, etc.) which can be relevant for future statistics.
* `id` is a string representing the unique identifier of the central-place foraging seabird.
* `params` is the list of parameters that should at least include the fields present in parameters.py.

The resulting AXY object adds step metrics to the initial DataFrame and accelerations metrics (*e.g.* ODBA), but also provides the central-place foraging trip statistics. See the documentation for more details.

methods                | description
---------------------- | ----------------------
`display_data_summary` | display a summary of the AXY data.
`full_diag`            | produce a full png diagnostic showing the AXY data.
`maps_diag`            | produce the png maps showing the GPS data.
`folium_map`           | produce the html map showing the GPS data.
`folium_map_wtrips`    | produce the html map showing the GPS data with trip colors.
`folium_map_colorgrad` | produce the html map showing the GPS data with a speed color gradient.

<br />

# Infos
* Python version used is 3.13.3
* OS used is Ubuntu 20.04

<br />

# Future developments
- [ ] document code and produce automatically documentation using sphinx
- [ ] create a `TDR` class for biologgers recording ***pressure*** (and ***temperature***).
- [ ] improve number of dives calculation in `add_is_diving` function to account for biologger time resolution.
- [ ] create a function `merge_gps_tdr(GPS, TDR)` that will merge TDR data within GPS data and produce the resulting dataframe.
- [ ] create a `GPS_TDR` class for biologgers with both GPS and TDR data.