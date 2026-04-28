# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
from cpforager import parameters, utils, GPS_TDR


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
config_dir = os.path.join(root_dir, "configs")
test_dir = os.path.join(root_dir, "tests", "gps_tdr")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "PER_PSC_2008_11"
colony = "PER_PSC_PSC"
gps_file_name = "PER_PSC_PSC_2008-11-25_SVAR_06_5006_F_GPS_GIP_36_UTC.csv"
tdr_file_name = "PER_PSC_PSC_2008-11-25_SVAR_06_5006_F_TDR_G5_3075_UTC.csv"
file_id = "PER_PSC_PSC_2008-11-25_SVAR_06_5006_F_GPSxTDR"

# set configuration paths
config_colony_path = os.path.join(config_dir, "colony_%s.yml" % (colony))
config_trips_path = os.path.join(config_dir, "trips.yml")
config_dives_path = os.path.join(config_dir, "dives_SULA.yml")

# set parameters dictionaries
params = parameters.get_params([config_colony_path, config_trips_path, config_dives_path])
plot_params = parameters.get_plot_params()


# ======================================================= #
# TEST GPS_TDR CLASS
# ======================================================= #

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
gps_tdr = GPS_TDR(df=df, group=fieldwork, id=file_id, params=params)

# test built-in methods
print(gps_tdr)
print(len(gps_tdr))
print(gps_tdr[1312])

# test display_data_summary method
gps_tdr.display_data_summary()

# test full_diag, maps_diag, folium_map
_ = gps_tdr.full_diag(test_dir, "%s_diag" % file_id, plot_params)
_ = gps_tdr.maps_diag(test_dir, "%s_map" % file_id, plot_params)
_ = gps_tdr.folium_map(test_dir, "%s_fmap" % file_id, plot_params)


# ======================================================= #
# TEST GPS_TDR INTERPOLATION
# ======================================================= #
# build a regular interpolation datetime
interp_freq_secs = 5
interp_datetime = pd.date_range(start=gps_tdr.df["datetime"].iloc[0], end=gps_tdr.df["datetime"].iloc[-1], freq=pd.Timedelta(seconds=interp_freq_secs), periods=None)

# compute interpolated positions from GPS_TDR method
df_gps_interp = gps_tdr.interpolate_lat_lon(interp_datetime, add_proxy=True)

# merge dataframes on datetime column
df_wo_positions = gps_tdr.df[["date", "time", "pressure", "temperature", "datetime"]]
df_interp = pd.merge(df_wo_positions, df_gps_interp, on="datetime", how="left")

# build another GPS_TDR object with interpolated dataframe
gps_tdr_interp = GPS_TDR(df=df_interp, group=gps_tdr.group, id="%s_%s" % (gps_tdr.id, "interp"), params=gps_tdr.params)

# display size change and produce diag
print("df     : %d/%d = %.2f%%" % (len(gps_tdr_interp), len(gps_tdr), 100*len(gps_tdr_interp)/len(gps_tdr)))
print("df_gps : %d/%d = %.2f%%" % (len(gps_tdr_interp.df_gps), len(gps_tdr.df_gps), 100*len(gps_tdr_interp.df_gps)/len(gps_tdr.df_gps)))
_ = gps_tdr_interp.full_diag(test_dir, "%s_diag" % gps_tdr_interp.id, plot_params)
