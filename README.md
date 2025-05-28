# seabird-movement-cpf
Python code to handle data gathered from biologgers attached to central-place foraging seabirds. The idea is to make movement ecology data a bit easier to process.


# GPS
Constructor `GPS(df, group, id, params)` : 
* `df` is a pandas DataFrame containing ***datetime***, ***longitude*** and ***latitude***, columns. The user must input the ***datetime*** at local timezone and converted to `datetime64` type (see `test.py`).
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


# AXY
Constructor  `AXY(df, group, id, params)` : 
* `df` is a pandas DataFrame containing ***datetime***, ***longitude***, ***latitude***, ***ax***, ***ay*** and ***az*** columns. The user must input the ***datetime*** at local timezone and converted to `datetime64` type (see `test.py`).
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
`folium_map_colorgrad` | produce the html map showing the GPS data with a speed color gradient.


# Infos
* Python version used is 3.11.5
* OS used is Ubuntu 18.04
