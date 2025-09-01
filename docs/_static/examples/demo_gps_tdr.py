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


# set parameters dictionaries
params = parameters.get_params(colony)
plot_params = parameters.get_plot_params()


# ======================================================= #
# BUILD GPS_TDR OBJECT
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

# build GPS_TDR object (df must have "datetime", "longitude", "latitude", "pressure" and "temperature" columns)
gps_tdr = GPS_TDR(df=df, group=fieldwork, id=file_id, params=params)