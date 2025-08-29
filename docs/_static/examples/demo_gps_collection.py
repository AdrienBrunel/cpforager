# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
from cpforager import parameters, utils, misc, GPS, GPS_Collection


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "gps_collection")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldworks = ["PER_PSC_2012_11", "PER_PSC_2013_11", "BRA_FDN_2016_09", "BRA_FDN_2018_09", "BRA_SAN_2022_03"]
colonies = ["PER_PSC_PSC", "PER_PSC_PSC", "BRA_FDN_MEI", "BRA_FDN_MEI", "BRA_SAN_FRA"]

# get parameters dictionaries
plot_params = parameters.get_plot_params()


# ======================================================= #
# BUILD GPS_COLLECTION OBJECT
# ======================================================= #

# loop over fieldworks
gps_collection = []
for (fieldwork, colony) in zip(fieldworks, colonies):

    # determine list of gps files
    files = misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_GPS_IGU")
    n_files = len(files)

    # get structure of parameters according to colony code
    params = parameters.get_params(colony)

    # loop over gps files
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

        # build GPS object
        gps = GPS(df=df, group=fieldwork, id=file_id, params=params)

        # append gps to the overall collection
        gps_collection.append(gps)

# build GPS_Collection object
gps_collection = GPS_Collection(gps_collection)
