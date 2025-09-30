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
config_dir = os.path.join(root_dir, "configs")
test_dir = os.path.join(root_dir, "tests", "tdr")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2022_04"
colony = "BRA_FDN_MEI"
file_name = "BRA_FDN_MEI_2022-04-26_SDAC_01_U61556_F_TDR_AXY_RT10_UTC.csv"

# set configuration paths
config_colony_path = os.path.join(config_dir, "colony_%s.yml" % (colony))
config_dives_path = os.path.join(config_dir, "dives_SULA.yml")

# set parameters dictionaries
params = parameters.get_params([config_colony_path, config_dives_path])
plot_params = parameters.get_plot_params()


# ======================================================= #
# TEST TDR CLASS
# ======================================================= #

# set file infos
file_id = file_name.replace(".csv", "")
file_path = os.path.join(data_dir, fieldwork, file_name)

# load raw data
df = pd.read_csv(file_path, sep=",")

# produce "datetime" column of type datetime64
df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="mixed", dayfirst=False)

# if time is at UTC, convert it to local datetime
if "_UTC" in file_name: df = utils.convert_utc_to_loc(df, params.get("local_tz"))

# build TDR object
tdr = TDR(df=df, group=fieldwork, id=file_id, params=params)

# test built-in methods
print(tdr)
print(len(tdr))
print(tdr[1312])

# test display_data_summary method
tdr.display_data_summary()

# test full_diag
_ = tdr.full_diag(test_dir, "%s_diag" % file_id, plot_params)