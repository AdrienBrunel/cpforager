# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import csv
import pandas as pd
from src import parameters, utils
from src.gps.gps import GPS
from src.gps_collection.gps_collection import GPS_Collection
from src.axy.axy import AXY


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = "%s/data" % root_dir
test_dir = "%s/test" % root_dir
src_dir  = "%s/src" % root_dir
plot_dir = "%s/plots" % root_dir
res_dir  = "%s/results" % root_dir


# ======================================================= #
# PARAMATERS
# ======================================================= #
plot_params = parameters.get_plot_params()


# ======================================================= #
# TEST GPS CLASS
# ======================================================= #

# parameters
fieldwork = "BRA_FDN_2016_09"
colony = "BRA_FDN_MEI"

# get structure of parameters
params = parameters.get_params(colony)

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

# test built-in methods
print(gps)
print(len(gps))
print(gps[1312])

# test display_data_summary method
gps.display_data_summary()

# test full_diag, maps_diag, folium_map, folium_map_colorgrad methods
_ = gps.full_diag(test_dir, "%s_diag" % file_id, plot_params)
_ = gps.maps_diag(test_dir, "%s_map" % file_id, plot_params)
_ = gps.folium_map(test_dir, "%s_fmap" % file_id)
_ = gps.folium_map_wtrips(test_dir, "%s_fmap_wtrips" % file_id, plot_params)
_ = gps.folium_map_colorgrad(test_dir, "%s_fmap_speed" % file_id, plot_params)


# ======================================================= #
# TEST GPS INTERPOLATION
# ======================================================= #
# build a regular interpolation datetime
interp_freq_secs = 5
interp_datetime = pd.date_range(start=gps.df["datetime"].iloc[0], end=gps.df["datetime"].iloc[-1], freq=pd.Timedelta(seconds=interp_freq_secs), periods=None)

# compute interpolated positions from GPS method
df_interp = gps.interpolate_lat_lon(interp_datetime, add_proxy=True)

# build another GPS object with interpolated dataframe
gps_interp = GPS(df_interp, gps.group, "%s_%s" % (gps.id, "interp"), gps.params)

# display size change and produce diag
print("%d/%d = %.2f%%" % (len(gps_interp), len(gps), 100*len(gps_interp)/len(gps)))
_ = gps_interp.full_diag(test_dir, "%s_diag" % gps_interp.id, plot_params)


# ======================================================= #
# TEST GPS_COLLECTION CLASS
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
        
    # test built-in methods
    print(gps_collection)
    print(len(gps_collection))
    print(gps_collection[2])
    
    # test display_data_summary method
    gps_collection.display_data_summary()
    
    # test plot_stats_summary, folium_map, maps_diag methods
    _ = gps_collection.plot_stats_summary(test_dir, "trip_statistics_%s" % fieldwork, plot_params)
    _ = gps_collection.folium_map(test_dir, "folium_%s" % fieldwork)
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
_ = gps_collection_all.folium_map(test_dir, "folium_all")
gps_collection_all.trip_statistics_all.to_csv("%s/trip_statistics_all.csv" % (test_dir), index=False, quoting=csv.QUOTE_NONNUMERIC)


# ======================================================= #
# TEST AXY CLASS
# ======================================================= #

# parameters
fieldwork = "BRA_FDN_2022_04"
colony = "BRA_FDN_MEI"

# get structure of parameters
params = parameters.get_params(colony)

# set file infos
file_name = "BRA_FDN_MEI_2022-04-26_SDAC_01_U61556_F_GPS_AXY_RT10_UTC.csv"
file_id = file_name.replace(".csv", "")
file_path = "%s/%s/%s" % (data_dir, fieldwork, file_name)
    
# load raw data
df = pd.read_csv(file_path, sep=",")

# produce "datetime" column of type datetime64
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="%Y-%m-%d %H:%M:%S.%f", dayfirst=False)

# if time is at UTC, convert it to local datetime
if "_UTC" in file_name: df = utils.convert_utc_to_loc(df, params.get("local_tz"))

# build AXY object
axy = AXY(df=df, group=fieldwork, id=file_id, params=params)


# test built-in methods
print(axy)
print(len(axy))
print(axy[1312])

# test display_data_summary method
axy.display_data_summary()

# test full_diag, maps_diag, folium_map, folium_map_colorgrad methods
_ = axy.full_diag(test_dir, "%s_diag" % file_id, plot_params)
_ = axy.maps_diag(test_dir, "%s_map" % file_id, plot_params)
_ = axy.folium_map(test_dir, "%s_fmap" % file_id)
_ = axy.folium_map_wtrips(test_dir, "%s_fmap_wtrips" % file_id, plot_params)
_ = axy.folium_map_colorgrad(test_dir, "%s_fmap_speed" % file_id, plot_params)