# cpforager
Are you a scientist involved in movement ecology working with biologging data collected from central-place foraging seabirds? **cpforager** is a Python package designed to help you manipulate, process, analyse and visualise the biologging datasets with ease and flexibility.

The main objectives of **cpforager** package are :  
1. Efficiently handle large-scale biologging datasets, including high-resolution sensor data.
2. Provide a modular and extensible architecture, allowing users to tailor the code to specific research needs.
3. Facilitate a smooth transition to Python for movement ecology researchers familiar with other environments (*e.g.*, R).

**cpforager** package supports various biologging sensor types commonly used in the field and provides the following core classes:
* `GPS` : for handling position recordings. 
* `TDR` : for handling pressure recordings.
* `AXY` : for handling tri-axial acceleration recordings at high resolution combined with lower resolution position and pressure recordings.
* `GPS_Collection` : for working with datasets composed of multiple GPS loggers.
* ~~`TDR_Collection` : for working with datasets composed of multiple TDR loggers.~~
* ~~`AXY_Collection` : for working with datasets composed of multiple AXY loggers.~~

Each class automatically enhances raw data but also computes key features specific to each biologger (*e.g.* trip segmentation for GPS, dive segmentation for TDR, ODBA calculation for AXY). They are also accompanied with built-in methods for data processing and visualisation.

<br />

# Installation
TO BE DONE

First, clone this repository:
<!-- start:code block -->
git clone https://github.com/AdrienBrunel/seabird-movement-cpf
<!-- end:code block -->

<br />
# User guide 

1. Read you data (GPS/TDR/AXY) with pandas
2. Build a datetime column  at the local timezone
3. Create the appropriate fields in parameters (see [Parameters](#Parameters "Goto Parameters"))
4. Build you object GPS/TDR/AXY
5. 

* In the `test` folder, the [test.py](./test/test.py) script illustrates how the `GPS`, `TDR`, `AXY` and `GPS_Collection` classes should be used to fully benefit the users. Results of this script is also found in the `test` folder.

* Documentation can be produced using sphinx in the `doc` folder. (Work in progress)

<br />

# Parameters 
* In [parameters.py](./cpforager/parameters.py) script, the `get_params(colony)` function produces a dictionary of parameters. This dictionary is required as an argument in the `GPS`, `TDR`, `AXY` and `GPS_Collection` classes. Users can modify the following parameters :

name                        | description           | class
--------------------------- | ----------------------| ----------------------
`colony`                    | longitude/latitude bounding box inside which the searbird's nest is to be found. | GPS
`local_tz`                  | local timezone of the seabird's nest. | GPS, TDR, AXY
`max_possible_speed`        | speed threshold in km/h above which a longitude/latitude measure can be considered as an error and will be deleted. | GPS
`dist_threshold`            | distance from the nest threshold in km above which the seabird is considered in a foraging trip. | GPS
`speed_threshold`           | speed threshold in km/h above which the seabird is still considered in a foraging trip despite being below the distance threshold. | GPS
`nesting_speed`             | speed threshold in km/h below which the seabird is considered at nest. | GPS
`trip_min_duration`         | duration in seconds above which a trip is valid. | GPS
`trip_max_duration`         | duration in seconds below which a trip is valid. | GPS
`trip_min_length`           | length in km above which a trip is valid. | GPS
`trip_max_length`           | length in km below which a trip is valid. | GPS
`trip_min_steps`            | number of steps above which a trip is valid. | GPS
`diving_depth_threshold`    | set the depth threshold above which a seabird is considered to be diving. | TDR
`dive_min_duration`         | set the minimum duration in seconds of a dive for the considered seabird. | TDR

<br />

# GPS
Constructor `GPS(df, group, id, params)` : 
* `df` is a pandas DataFrame containing ***datetime***, ***longitude*** and ***latitude*** columns. The user must input the ***datetime*** at the local timezone and converted to `datetime64` type (see [test.py](./test/test.py)).
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

# TDR
Constructor `TDR(df, group, id, params)` : 
* `df` is a pandas DataFrame containing ***datetime***, ***pressure*** and ***temperature*** columns. The user must input the ***datetime*** at the local timezone and converted to `datetime64` type (see [test.py](./test/test.py)).
* `group` is a string representing the group to which the data belongs (year, fieldwork, specie, etc.) which can be relevant for future statistics.
* `id` is a string representing the unique identifier of the central-place foraging seabird.
* `params` is the list of parameters that should at least include the fields present in [parameters.py](./cpforager/parameters.py).

The resulting TDR object adds segmented dives to the initial DataFrame. See the documentation for more details.

methods                | description
---------------------- | ----------------------
`display_data_summary` | display a summary of the TDR data.
`full_diag`            | produce a full png diagnostic showing the TDR data.

# AXY
Constructor `AXY(df, group, id, params)` : 
* `df` is a pandas DataFrame containing ***datetime***, ***longitude***, ***latitude***, ***ax***, ***ay*** and ***az*** columns. The user must input the ***datetime*** at the local timezone and converted to `datetime64` type (see [test.py](./test/test.py)).
* `group` is a string representing the group to which the data belongs (year, fieldwork, specie, etc.) which can be relevant for future statistics.
* `id` is a string representing the unique identifier of the central-place foraging seabird.
* `params` is the list of parameters that should at least include the fields present in [parameters.py](./cpforager/parameters.py).

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


# TDR_Collection
Constructor `TDR_Collection(tdr_collection)`
* `tdr_collection` is an array of TDR object.

TO BE DONE.

# AXY_Collection
Constructor `AXY_Collection(axy_collection)`
* `axy_collection` is an array of AXY object.

TO BE DONE.

<br />

# Infos
* Python version used is 3.13.3
* OS used is Ubuntu 20.04
* Environment used is [environment.yml](environment.yml)

<br />

# Future developments
- [ ] document code and produce automatically documentation using sphinx
- [ ] create a function `merge_gps_tdr(GPS, TDR)` that will merge TDR data within GPS data and produce the resulting dataframe.
- [ ] create a `GPS_TDR` class for biologgers with both GPS and TDR data.
- [ ] create a `AXY_Collection` class.
- [ ] create a `TDR_Collection` class.