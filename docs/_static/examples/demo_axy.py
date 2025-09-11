# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
from cpforager import parameters, utils, AXY


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir   = os.getcwd()
data_dir   = os.path.join(root_dir, "data")
config_dir = os.path.join(root_dir, "configs")
test_dir   = os.path.join(root_dir, "tests", "axy")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2022_04"
colony    = "BRA_FDN_MEI"
file_name = "BRA_FDN_MEI_2022-04-26_SDAC_01_U61556_F_GPS_AXY_RT10_UTC.csv"
file_id   = file_name.replace(".csv", "")
file_path = os.path.join(data_dir, fieldwork, file_name)

# set configuration paths
config_colony_path   = os.path.join(config_dir, "colony_%s.yml" % (colony))
config_trips_path    = os.path.join(config_dir, "trips.yml")
config_dives_path    = os.path.join(config_dir, "dives_SULA.yml")
config_accelero_path = os.path.join(config_dir, "accelero_rollavg.yml")

# set parameters dictionaries
params      = parameters.get_params([config_colony_path, config_trips_path, config_dives_path, config_accelero_path])
plot_params = parameters.get_plot_params()


# ======================================================= #
# BUILD AXY OBJECT
# ======================================================= #

# load raw data
df = pd.read_csv(file_path, sep=",")

# add a "datetime" column of type datetime64
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="%Y-%m-%d %H:%M:%S.%f", dayfirst=False)

# if time is at UTC, convert it to local datetime
if "_UTC" in file_name: df = utils.convert_utc_to_loc(df, params.get("local_tz"))

# build AXY object (df must have "datetime", "ax", "ay", "az", "longitude", "latitude", "pressure" and "temperature" columns)
axy = AXY(df=df, group=fieldwork, id=file_id, params=params)