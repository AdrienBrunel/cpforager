# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import csv
import pandas as pd
from cpforager import parameters, utils, misc, GPS_TDR, GPS_TDR_Collection


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "gps_tdr_collection")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "PER_PSC_2008_11"
colony = "PER_PSC_PSC"

# list of bird ids (both in gps and tdr files)
bird_ids = ["_LBOU_55_", "_LBOU_56_", "_SVAR_06_", "_SVAR_04_"]
n_bird_ids = len(bird_ids)


# set parameters dictionaries
params = parameters.get_params(colony)
plot_params = parameters.get_plot_params()


# ======================================================= #
# TEST GPS_TDR CLASS
# ======================================================= #

# loop over bird ids
gps_tdr_collection = []
for k in range(n_bird_ids):
    
    # get bird id
    bird_id = bird_ids[k]

    # get corresponding gps file name
    gps_file_name = misc.grep_pattern(misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_GPS_"), bird_id)[0]
    
    # get corresponding tdr file
    tdr_file_name = misc.grep_pattern(misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_TDR_"), bird_id)[0]

    # set file infos
    gps_file_id = gps_file_name.replace(".csv", "")
    gps_file_path = os.path.join(data_dir, fieldwork, gps_file_name)
    tdr_file_id = tdr_file_name.replace(".csv", "")
    tdr_file_path = os.path.join(data_dir, fieldwork, tdr_file_name)

    # load raw data
    df_gps = pd.read_csv(gps_file_path, sep=",")
    df_tdr = pd.read_csv(tdr_file_path, sep=",")

    # produce "datetime" column of type datetime64
    df_gps["datetime"] = pd.to_datetime(df_gps["date"] + " " + df_gps["time"], format="mixed", dayfirst=False)
    df_tdr["datetime"] = pd.to_datetime(df_tdr["date"] + " " + df_tdr["time"], format="mixed", dayfirst=False)

    # if sensor model is G5, convert dbar to hPa
    if "_TDR_G5_" in tdr_file_name: df_tdr["pressure"] = 100*df_tdr["pressure"]

    # if time is at UTC, convert it to local datetime
    if "_UTC" in gps_file_name: df_gps = utils.convert_utc_to_loc(df_gps, params.get("local_tz"))
    if "_UTC" in tdr_file_name: df_tdr = utils.convert_utc_to_loc(df_tdr, params.get("local_tz"))

    # merge TDR and GPS data on datetime colum
    df = pd.merge_ordered(df_gps, df_tdr, on="datetime", how="outer")
    df[["date", "time"]] = df[["date_y", "time_y"]]
    df = df[["date", "time", "datetime", "longitude", "latitude", "pressure", "temperature"]]

    # build GPS_TDR object
    gps_tdr = GPS_TDR(df=df, group=fieldwork, id=bird_id, params=params)
    
    # append tdr to the overall collections
    gps_tdr_collection.append(gps_tdr)

# build GPS_TDR_Collection object
gps_tdr_collection = GPS_TDR_Collection(gps_tdr_collection)

# test built-in methods
print(gps_tdr_collection)
print(len(gps_tdr_collection))
print(gps_tdr_collection[2])

# test display_data_summary method
gps_tdr_collection.display_data_summary()

# test plot_dive_stats_summary, indiv_depth_all, plot_trip_stats_summary, maps_diag, indiv_map_all, folium_map methods
_ = gps_tdr_collection.plot_dive_stats_summary(test_dir, "dive_statistics_%s" % fieldwork, plot_params)
gps_tdr_collection.dive_statistics_all.to_csv("%s/dive_statistics_%s.csv" % (test_dir, fieldwork), index=False, quoting=csv.QUOTE_NONNUMERIC)
_ = gps_tdr_collection.indiv_depth_all(test_dir, "indiv_depth_%s" % fieldwork, plot_params)
_ = gps_tdr_collection.plot_trip_stats_summary(test_dir, "trip_statistics_%s" % fieldwork, plot_params)
_ = gps_tdr_collection.maps_diag(test_dir, "maps_diag_%s" % fieldwork, plot_params, rand=True)
_ = gps_tdr_collection.indiv_map_all(test_dir, "indiv_map_%s" % fieldwork, plot_params)
_ = gps_tdr_collection.folium_map(test_dir, "fmaps_%s" % fieldwork, plot_params)
gps_tdr_collection.trip_statistics_all.to_csv("%s/trip_statistics_%s.csv" % (test_dir, fieldwork), index=False, quoting=csv.QUOTE_NONNUMERIC)
