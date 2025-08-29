# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
from cpforager import parameters, utils, TDR


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "tdr")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2022_04"
colony    = "BRA_FDN_MEI"
file_name = "BRA_FDN_MEI_2022-04-26_SDAC_01_U61556_F_TDR_G5_RT10_UTC.csv"
file_id   = file_name.replace(".csv", "")
file_path = os.path.join(data_dir, fieldwork, file_name)

# get parameters dictionaries
plot_params = parameters.get_plot_params()
params      = parameters.get_params(colony)


# ======================================================= #
# BUILD TDR OBJECT
# ======================================================= #

# load raw data
df = pd.read_csv(file_path, sep=",")

# add a "datetime" column of type datetime64
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="mixed", dayfirst=False)

# if time is at UTC, convert it to local datetime
if "_UTC" in file_name: df = utils.convert_utc_to_loc(df, params.get("local_tz"))

# build TDR object (df must have "datetime", "pressure" and "temperature" columns)
tdr = TDR(df=df, group=fieldwork, id=file_id, params=params)