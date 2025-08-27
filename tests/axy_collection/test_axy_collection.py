# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import csv
import pandas as pd
from cpforager import parameters, utils, misc, AXY, AXY_Collection


# ======================================================= #
# DIRECTORIES
# ======================================================= #
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "data")
test_dir = os.path.join(root_dir, "tests", "axy_collection")


# ======================================================= #
# PARAMETERS
# ======================================================= #

# set metadata
fieldwork = "BRA_FDN_2022_04"
colony = "BRA_FDN_MEI"

# set parameters dictionaries
plot_params = parameters.get_plot_params()
params = parameters.get_params(colony)


# ======================================================= #
# TEST AXY_COLLECTION CLASS
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

    # append axy to the overall collections
    axy_collection.append(axy)

# plot data summary
axy_collection = AXY_Collection(axy_collection)

# test built-in methods
print(axy_collection)
print(len(axy_collection))
print(axy_collection[2])

# test display_data_summary method
axy_collection.display_data_summary()

# test plot_stats_summary, folium_map, maps_diag methods
_ = axy_collection.plot_trip_stats_summary(test_dir, "trip_statistics_%s" % fieldwork, plot_params)
_ = axy_collection.plot_dive_stats_summary(test_dir, "dive_statistics_%s" % fieldwork, plot_params)
_ = axy_collection.indiv_map_all(test_dir, "indiv_map_all_%s" % fieldwork, plot_params)
_ = axy_collection.indiv_depth_all(test_dir, "indiv_depth_all_%s" % fieldwork, plot_params)
_ = axy_collection.folium_map(test_dir, "fmaps_%s" % fieldwork, plot_params)
_ = axy_collection.maps_diag(test_dir, "maps_%s" % fieldwork, plot_params)
axy_collection.trip_statistics_all.to_csv("%s/trip_statistics_%s.csv" % (test_dir, fieldwork), index=False, quoting=csv.QUOTE_NONNUMERIC)


# import pandas as pd
# import numpy as np
# # Create the first DataFrame
# df1 = pd.DataFrame({
#     'float_col': [1.1, 2.2, np.nan],
#     'str_col': ["lol1", "lol2", "lol3"],
#     'int_col': [1, 2, np.nan]
# })
# # Create the second DataFrame
# df2 = pd.DataFrame({
#     'float_col': [3.3, np.nan, 5.5],
#     'str_col': ["lol1", "lol2", np.nan],
#     'int_col': [3, 4, 5]
# })
# # Concatenate the DataFrames
# result = pd.concat([df1, df2], ignore_index=True)
# print(result)

# result["int_col"].astype(int)
# result["int_col"] = result["int_col"].astype("Int64")
# result["int_col"] = result["float_col"].astype("Float64")
# print(result)


# def get_column_dtype(column_names):
    
#     # define the dictionary of types by columns
#     {"group":"str", "id":"str", "datetime":"object", "longitude":"float", "latitude":"float", "pressure":"float", "temperature":"float", "ax":"float", "ay":"float", "az":"float",
#      "step_time":"float", "step_length":"float", "step_speed":"float", "step_heading":"float","step_turning_angle":"float", 
#                "step_heading_to_colony":"float", "is_night":"int", "is_suspicious":"Int64", "dist_to_nest":"float", "trip":"Int64",
#                     "depth":"float", "dive":"Int64",
#                     "ax_f":"float", "ay_f":"float", "az_f":"float","odba":"float", "odba_f":"float"}
#     dtypes_columns_dict = {"group":"str", "id":"str", "datetime":"object", "longitude":"float"}

#     # extract types
#     dtypes = [dtypes_columns_dict[key] for key in column_names]
    
#     return dtypes