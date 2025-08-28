# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import csv
import pandas as pd
from cpforager import parameters, utils, misc, GPS, GPS_Collection
from cpforager.gps_collection import stdb


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "gps_collection")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldworks = ["PER_PSC_2012_11", "PER_PSC_2013_11", "BRA_FDN_2016_09", "BRA_FDN_2018_09", "BRA_SAN_2022_03"]
colonies = ["PER_PSC_PSC", "PER_PSC_PSC", "BRA_FDN_MEI", "BRA_FDN_MEI", "BRA_SAN_FRA"]

# set parameters dictionaries
plot_params = parameters.get_plot_params()


# ======================================================= #
# TEST GPS_COLLECTION CLASS
# ======================================================= #

# loop over fieldworks
gps_collection_all = []
for (fieldwork, colony) in zip(fieldworks, colonies):

    # list of files to process
    files = misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_GPS_")
    n_files = len(files)

    # get structure of parameters
    params = parameters.get_params(colony)
    plot_params = parameters.get_plot_params()

    # loop over files in directory
    gps_collection = []
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

        # build GPS object
        gps = GPS(df=df, group=fieldwork, id=file_id, params=params)

        # append gps to the overall collection
        gps_collection.append(gps)
        gps_collection_all.append(gps)

    # plot data summary
    gps_collection = GPS_Collection(gps_collection)

    # test built-in methods
    print(gps_collection)
    print(len(gps_collection))
    print(gps_collection[2])

    # test display_data_summary method
    gps_collection.display_data_summary()

    # test plot_stats_summary, folium_map, maps_diag methods
    _ = gps_collection.plot_stats_summary(test_dir, "trip_statistics_%s" % fieldwork, plot_params)
    _ = gps_collection.folium_map(test_dir, "fmaps_%s" % fieldwork, plot_params)
    _ = gps_collection.maps_diag(test_dir, "maps_%s" % fieldwork, plot_params)

# analysis of all data
gps_collection_all = GPS_Collection(gps_collection_all)

# test built-in methods
print(gps_collection_all)
print(len(gps_collection_all))
print(gps_collection_all[5])

# test display_data_summary method
gps_collection_all.display_data_summary()

# test plot_stats_summary, folium_map, maps_diag methods
_ = gps_collection_all.plot_stats_summary(test_dir, "trip_statistics_all", plot_params)
_ = gps_collection_all.folium_map(test_dir, "fmaps_all", plot_params, rand=True)
_ = gps_collection_all.indiv_map_all(test_dir, "indiv_map_all", plot_params)
gps_collection_all.trip_statistics_all.to_csv("%s/trip_statistics_all.csv" % (test_dir), index=False, quoting=csv.QUOTE_NONNUMERIC)


# ======================================================= #
# TEST SEABIRD TRACKING DATABASE
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2016_09"
colony = "BRA_FDN_MEI"

# load metadata
metadata_file_path = os.path.join(data_dir, fieldwork, "metadata_%s.csv" % (fieldwork))
metadata = pd.read_csv(metadata_file_path, sep=",")

# list of files to process
files = misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_GPS_IGU")
n_files = len(files)

# get structure of parameters
params = parameters.get_params(colony)
plot_params = parameters.get_plot_params()

# loop over files in directory
gps_collection = []
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

    # build GPS object
    gps = GPS(df, fieldwork, file_id, params)

    # append gps to the overall collections
    gps_collection.append(gps)
    
# build GPS_Collection object
gps_collection = GPS_Collection(gps_collection)

# produce dataframe at the Seabird Tracking format
df_stdb = gps_collection.to_SeabirdTracking(metadata)
df_stdb.to_csv("%s/%s_stdb_format.csv" % (test_dir, fieldwork), index=False, quoting=csv.QUOTE_NONNUMERIC)

# produce gps collection from the Seabird Tracking format
df_stdb = pd.read_csv("%s/%s_stdb_format.csv" % (test_dir, fieldwork), sep=",")
new_gps_collection, new_metadata = stdb.convert_to_gps_collection(df_stdb, fieldwork, params)
new_gps_collection = GPS_Collection(gps_collection)
new_gps_collection.display_data_summary()