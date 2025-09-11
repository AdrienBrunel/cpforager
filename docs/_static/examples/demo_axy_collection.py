# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
from cpforager import parameters, utils, misc, AXY, AXY_Collection


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir   = os.getcwd()
data_dir   = os.path.join(root_dir, "data")
config_dir = os.path.join(root_dir, "configs")
test_dir   = os.path.join(root_dir, "tests", "axy_collection")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2022_04"
colony    = "BRA_FDN_MEI"

# set configuration paths
config_colony_path   = os.path.join(config_dir, "colony_%s.yml" % (colony))
config_trips_path    = os.path.join(config_dir, "trips.yml")
config_dives_path    = os.path.join(config_dir, "dives_SULA.yml")
config_accelero_path = os.path.join(config_dir, "accelero_rollavg.yml")

# set parameters dictionaries
params      = parameters.get_params([config_colony_path, config_trips_path, config_dives_path, config_accelero_path])
plot_params = parameters.get_plot_params()


# ======================================================= #
# BUILD AXY_COLLECTION OBJECT
# ======================================================= #

# list of files to process
files = misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_GPS_AXY_")
n_files = len(files)

# loop over files in directory
axy_collection = []
for k in range(n_files):

    # set file infos
    file_name = files[k]
    file_id = file_name.replace(".csv", "")
    file_path = os.path.join(data_dir, fieldwork, file_name)

    # load raw data
    df = pd.read_csv(file_path, sep=",")

    # produce "datetime" column of type datetime64
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="mixed", dayfirst=False)

    # if time is at UTC, convert it to local datetime
    if "_UTC" in file_name: df = utils.convert_utc_to_loc(df, params.get("local_tz"))

    # build AXY object
    axy = AXY(df=df, group=fieldwork, id=file_id, params=params)

    # append axy to the overall collection
    axy_collection.append(axy)

# build AXY_Collection object
axy_collection = AXY_Collection(axy_collection)