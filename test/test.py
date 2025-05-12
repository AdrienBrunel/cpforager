# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import csv
import pandas as pd
from src import parameters, utils
from src.gps.gps import GPS
from src.gps_collection.gps_collection import GPS_Collection


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = "%s/data" % root_dir
test_dir = "%s/test" % root_dir
src_dir = "%s/src" % root_dir
plot_dir = "%s/plots" % root_dir
res_dir = "%s/results" % root_dir


# ======================================================= #
# TEST GPS
# ======================================================= #

# parameters
fieldwork = "BRA_FDN_2016_09"
colony = "BRA_FDN_MEI"

# get structure of parameters
params = parameters.get_params(colony)
plot_params = parameters.get_plot_params()

# set file infos
file_name = "BRA_FDN_MEI_2016-09-15_SSUL_01_T32840_NA_GPS_IGU120_BR023_LOC.csv"
file_id = file_name.replace(".csv", "")
file_path = "%s/%s/%s" % (data_dir, fieldwork, file_name)
    
# load raw data
df = pd.read_csv(file_path, sep=",")

# produce "datetime" column of type datetime64
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="mixed", dayfirst=False)

# build GPS object
gps = GPS(df=df, group=fieldwork, id=file_id, params=params)

# display summary
gps.display_data_summary()

# produce individual plots
_ = gps.full_diag(test_dir, "%s_diag" % file_id, plot_params)
_ = gps.maps_diag(test_dir, "%s_map" % file_id, plot_params)
_ = gps.folium_map(test_dir, "%s_fmap" % file_id)
_ = gps.folium_map_colorgrad(test_dir, "%s_fmap_speed" % file_id, plot_params)

# produce the csv file of processed gps data
gps.df.drop(["datetime", "step_heading"], axis=1).to_csv("%s/%s" % (test_dir, file_name), index=False, quoting=csv.QUOTE_NONNUMERIC)


# ======================================================= #
# TEST GPS COLLECTION
# ======================================================= #

# parameters
fieldworks = ["PER_PSC_2012_11", "PER_PSC_2013_11", "BRA_FDN_2016_09", "BRA_FDN_2018_09", "BRA_SAN_2022_03"]
colonies = ["PER_PSC_PSC", "PER_PSC_PSC", "BRA_FDN_MEI", "BRA_FDN_MEI", "BRA_SAN_FRA"]

# loop over fieldworks
gps_collection_all = []
for (fieldwork, colony) in zip(fieldworks, colonies):

    # list of files to process
    files = os.listdir("%s/%s" % (data_dir, fieldwork))
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
        file_path = "%s/%s" % ("%s/%s" % (data_dir, fieldwork), file_name)
        
        # load raw data
        df = pd.read_csv(file_path, sep=",")
        
        # produce "datetime" column of type datetime64
        df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="mixed", dayfirst=False)
        
        # if time is at UTC, convert it to local datetime
        if "_UTC" in file_name: df = utils.convert_utc_to_loc(df, params.get("local_tz"))
        
        # build GPS object
        gps = GPS(df=df, group=fieldwork, id=file_id, params=params)
        
        # append gps to the overall collections
        gps_collection.append(gps)
        gps_collection_all.append(gps)
        
    # plot data summary
    gps_collection = GPS_Collection(gps_collection)
    gps_collection.display_data_summary()
    _ = gps_collection.plot_stats_summary(test_dir, "trip_statistics_%s" % fieldwork, plot_params)
    _ = gps_collection.folium_map(test_dir, "folium_%s" % fieldwork)
    _ = gps_collection.maps_diag(test_dir, "maps_%s" % fieldwork, plot_params)

# analysis of all data
gps_collection_all = GPS_Collection(gps_collection_all)
gps_collection_all.display_data_summary()
_ = gps_collection_all.plot_stats_summary(test_dir, "trip_statistics_all", plot_params)
_ = gps_collection_all.folium_map(test_dir, "folium_all")
gps_collection_all.trip_statistics_all.to_csv("%s/trip_statistics_all.csv" % (test_dir), index=False, quoting=csv.QUOTE_NONNUMERIC)