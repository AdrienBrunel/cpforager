# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
from cpforager import parameters, utils, GPS


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "gps")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2016_09"
colony    = "BRA_FDN_MEI"
file_name = "BRA_FDN_MEI_2016-09-15_SSUL_01_T32840_NA_GPS_IGU120_BR023_LOC.csv"
file_id   = file_name.replace(".csv", "")
file_path = os.path.join(data_dir, fieldwork, file_name)

# get parameters dictionaries
plot_params = parameters.get_plot_params()
params      = parameters.get_params(colony)


# ======================================================= #
# BUILD GPS OBJECT
# ======================================================= #

# load raw data 
df = pd.read_csv(file_path, sep=",")

# add a "datetime" column of type datetime64
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="mixed", dayfirst=False)

# if time is at UTC, convert it to local datetime
if "_UTC" in file_name: df = utils.convert_utc_to_loc(df, params.get("local_tz"))

# build GPS object (df must have "datetime", "longitude" and "latitude" columns)
gps = GPS(df=df, group=fieldwork, id=file_id, params=params)