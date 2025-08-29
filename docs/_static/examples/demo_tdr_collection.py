# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import pandas as pd
from cpforager import parameters, utils, misc, TDR, TDR_Collection


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "tdr_collection")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldworks = ["PER_PSC_2008_11", "BRA_FDN_2017_04", "BRA_FDN_2022_04"]
colonies = ["PER_PSC_PSC", "BRA_FDN_MEI", "BRA_FDN_MEI"]

# set parameters dictionaries
plot_params = parameters.get_plot_params()


# ======================================================= #
# BUILD TDR_COLLECTION OBJECT
# ======================================================= #

# loop over fieldworks
tdr_collection = []
for (fieldwork, colony) in zip(fieldworks, colonies):

    # list of files to process
    files = misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_TDR_")
    n_files = len(files)

    # get structure of parameters
    params = parameters.get_params(colony)

    # loop over files in directory
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

        # if sensor model is G5, convert dbar to hPa
        if "_TDR_G5_" in file_name: df["pressure"] = 100*df["pressure"]
         
        # build TDR object
        tdr = TDR(df=df, group=fieldwork, id=file_id, params=params)

        # append tdr to the overall collection
        tdr_collection.append(tdr)

# build TDR_Collection object
tdr_collection = TDR_Collection(tdr_collection)