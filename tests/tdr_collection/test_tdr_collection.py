# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import csv
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
# TEST TDR_COLLECTION CLASS
# ======================================================= #

# loop over fieldworks
tdr_collection_all = []
for (fieldwork, colony) in zip(fieldworks, colonies):

    # list of files to process
    files = misc.grep_pattern(os.listdir(os.path.join(data_dir, fieldwork)), "_TDR_")
    n_files = len(files)

    # get structure of parameters
    params = parameters.get_params(colony)
    plot_params = parameters.get_plot_params()

    # loop over files in directory
    tdr_collection = []
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

        # append tdr to the overall collections
        tdr_collection.append(tdr)
        tdr_collection_all.append(tdr)

    # plot data summary
    tdr_collection = TDR_Collection(tdr_collection)

    # test built-in methods
    print(tdr_collection)
    print(len(tdr_collection))
    print(tdr_collection[0])

    # test display_data_summary method
    tdr_collection.display_data_summary()

    # test plot_stats_summary, folium_map, maps_diag methods
    _ = tdr_collection.plot_stats_summary(test_dir, "dive_statistics_%s" % fieldwork, plot_params)

# build TDR_Collection object
tdr_collection_all = TDR_Collection(tdr_collection_all)

# test built-in methods
print(tdr_collection_all)
print(len(tdr_collection_all))
print(tdr_collection_all[5])

# test display_data_summary method
tdr_collection_all.display_data_summary()

# test plot_stats_summary, folium_map, maps_diag methods
_ = tdr_collection_all.plot_stats_summary(test_dir, "dive_statistics_all", plot_params)
tdr_collection_all.dive_statistics_all.to_csv("%s/dive_statistics_all.csv" % (test_dir), index=False, quoting=csv.QUOTE_NONNUMERIC)
_ = tdr_collection_all.indiv_depth_all(test_dir, "indiv_depth_all", plot_params)