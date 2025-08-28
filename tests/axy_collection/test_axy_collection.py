# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import csv
import pandas as pd
from cpforager import parameters, utils, misc, AXY, AXY_Collection


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "axy_collection")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2022_04"
colony = "BRA_FDN_MEI"

# set parameters dictionaries
plot_params = parameters.get_plot_params()
params = parameters.get_params(colony)


# ======================================================= #
# TEST AXY_COLLECTION CLASS
# ======================================================= #

# list of files to process
files = misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_GPS_AXY_")
n_files = len(files)

# loop over files in directory
axy_collection = []
for k in range(n_files):

    # set file infos
    file_name = files[k]
    file_id = file_name.replace(".csv", "")
    file_path = os.path.join(data_dir, fieldwork, file_name)

    # load raw data
    df = pd.read_csv(file_path, sep=",")

    # produce "datetime" column of type datetime64
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="mixed", dayfirst=False)

    # if time is at UTC, convert it to local datetime
    if "_UTC" in file_name: df = utils.convert_utc_to_loc(df, params.get("local_tz"))

    # build AXY object
    axy = AXY(df=df, group=fieldwork, id=file_id, params=params)

    # append axy to the overall collection
    axy_collection.append(axy)

# build AXY_Collection object
axy_collection = AXY_Collection(axy_collection)

# test built-in methods
print(axy_collection)
print(len(axy_collection))
print(axy_collection[2])

# test display_data_summary method
axy_collection.display_data_summary()

# test plot_stats_summary, folium_map, maps_diag methods
_ = axy_collection.plot_trip_stats_summary(test_dir, "trip_statistics_%s" % fieldwork, plot_params)
_ = axy_collection.plot_dive_stats_summary(test_dir, "dive_statistics_%s" % fieldwork, plot_params)
_ = axy_collection.indiv_map_all(test_dir, "indiv_map_all_%s" % fieldwork, plot_params)
_ = axy_collection.indiv_depth_all(test_dir, "indiv_depth_all_%s" % fieldwork, plot_params)
_ = axy_collection.folium_map(test_dir, "fmaps_%s" % fieldwork, plot_params)
_ = axy_collection.maps_diag(test_dir, "maps_%s" % fieldwork, plot_params)
axy_collection.trip_statistics_all.to_csv("%s/trip_statistics_%s.csv" % (test_dir, fieldwork), index=False, quoting=csv.QUOTE_NONNUMERIC)