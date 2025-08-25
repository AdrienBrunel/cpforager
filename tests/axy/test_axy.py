# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
import time
from cpforager import parameters, utils, AXY


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "axy")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2022_04"
colony = "BRA_FDN_MEI"
file_name = "BRA_FDN_MEI_2022-04-26_SDAC_01_U61556_F_GPS_AXY_RT10_UTC.csv"

# set parameters dictionaries
params = parameters.get_params(colony)
plot_params = parameters.get_plot_params()


# ======================================================= #
# TEST AXY CLASS
# ======================================================= #

# set file infos
file_id = file_name.replace(".csv", "")
file_path = os.path.join(data_dir, fieldwork, file_name)

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
print(axy.df_gps.iloc[1312])

# test display_data_summary method
axy.display_data_summary()

# test full_diag, maps_diag, folium_map, folium_map_colorgrad methods
_ = axy.full_diag(test_dir, "%s_diag" % file_id, plot_params)
_ = axy.maps_diag(test_dir, "%s_map" % file_id, plot_params)
_ = axy.folium_map(test_dir, "%s_fmap" % file_id, plot_params)


# ======================================================= #
# TEST FAST FULL DIAGNOSTIC
# ======================================================= #

# compare plotting speed of full diagnostic
for fast in [False, True]:
    start = time.time()
    _ = axy.full_diag(test_dir, "%s_diag_fast=%r" % (file_id, fast), plot_params, fast=fast)
    end = time.time()
    print("Full diagnostic [fast=%r] : %.1f minutes" % (fast, (end-start)/60))


# ======================================================= #
# TEST AXY INTERPOLATION
# ======================================================= #

# build a regular interpolation datetime
interp_freq_secs = 10
interp_datetime = pd.date_range(start=axy.df_gps["datetime"].iloc[0], end=axy.df_gps["datetime"].iloc[-1], freq=pd.Timedelta(seconds=interp_freq_secs), periods=None)

# compute interpolated positions from AXY method
df_gps_interp = axy.interpolate_lat_lon(interp_datetime, add_proxy=True)

# merge dataframes on datetime column
df_wo_positions = axy.df[["date", "time", "ax", "ay", "az", "pressure", "temperature", "datetime"]]
df_interp = pd.merge(df_wo_positions, df_gps_interp, on="datetime", how="left")

# build another AXY object with interpolated dataframe
axy_interp = AXY(df=df_interp, group=fieldwork, id="%s_%s" % (axy.id, "interp"), params=params)

# display size change and produce diag
print("df     : %d/%d = %.2f%%" % (len(axy_interp), len(axy), 100*len(axy_interp)/len(axy)))
print("df_gps : %d/%d = %.2f%%" % (len(axy_interp.df_gps), len(axy.df_gps), 100*len(axy_interp.df_gps)/len(axy.df_gps)))
_ = axy_interp.full_diag(test_dir, "%s_diag" % axy_interp.id, plot_params, fast=True)
_ = axy_interp.maps_diag(test_dir, "%s_map" % axy_interp.id, plot_params)
