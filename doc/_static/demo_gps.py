# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
from cpforager import parameters, GPS


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "test")
plot_dir = os.path.join(root_dir, "plots")


# ======================================================= #
# PARAMETERS
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
file_path = os.path.join(data_dir, fieldwork, file_name)

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