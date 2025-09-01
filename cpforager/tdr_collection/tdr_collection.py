# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import pandas as pd
import numpy as np
from cpforager import parameters
from cpforager.tdr_collection import diagnostic, display


# ================================================================================================ #
# TDR_COLLECTION CLASS
# ================================================================================================ #
class TDR_Collection:
    
    """
    A class to represent a list of TDR data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] TDR_COLLECTION
    def __init__(self, tdr_collection):
        
        """
        Constructor of a TDR_Collection object.
        
        :param tdr_collection: the list of TDR.
        :type tdr_collection: list[cpforager.TDR]
        
        :ivar tdr_collection: the list of TDR.
        :vartype tdr_collection: list[cpforager.TDR]
        :ivar n_tdr: the total number of TDR included in the list.
        :vartype n_tdr: int
        :ivar n_dives: the number of dives summed over every TDR included in the list.
        :vartype n_dives: int
        :ivar dive_statistics_all: the dive statistics dataframe merged over every TDR included in the list.
        :vartype dive_statistics_all: pandas.DataFrame
        :ivar df_all: the enhanced TDR dataframe merged over every TDR included in the list.
        :vartype df_all: pandas.DataFrame
        """
        
        # init dataframes
        column_names_1 = ["group", "id", "dive_id", "duration", "max_depth"]
        dtypes_1 = parameters.get_columns_dtypes(column_names_1)
        dive_statistics_all = pd.DataFrame(columns=column_names_1).astype(dtype=dtypes_1)
        
        column_names_2 = ["group", "id", "datetime", "pressure", "temperature", "step_time", "depth", "is_night", "dive"]
        dtypes_2 = parameters.get_columns_dtypes(column_names_2)
        df_all = pd.DataFrame(columns=column_names_2).astype(dtype=dtypes_2)

        # compute statistics
        group = []
        id = []
        dive_id = []
        for tdr in tdr_collection:

            # display infos
            print(" # =========  [Group %s] - [Id %s] ========= #" % (tdr.group, tdr.id))

            # build the dive statisics dataframe of the entire collection
            group = np.concatenate((group, [tdr.group for k in tdr.df.loc[tdr.df["dive"]>0, "dive"].unique()]))
            id = np.concatenate((id, [tdr.id for k in tdr.df.loc[tdr.df["dive"]>0, "dive"].unique()]))
            dive_id = np.concatenate((dive_id, [f"{tdr.group}_{tdr.id}_D{k:04}" for k in tdr.df.loc[tdr.df["dive"]>0, "dive"].unique()]))
            dive_statistics_all = pd.concat([dive_statistics_all, tdr.dive_statistics], ignore_index=True)

            # build the full data dataframe of the entire collection
            df_tmp = pd.DataFrame(columns=df_all.columns)
            df_tmp[["datetime", "pressure", "temperature", "step_time", "is_night", "depth", "dive"]] = tdr.df[["datetime", "pressure", "temperature", "step_time", "is_night", "depth", "dive"]]
            df_tmp = df_tmp.astype(dtype=dtypes_2)

            # add metadata in df for each dive
            df_tmp["id"] = tdr.id
            df_tmp["group"] = tdr.group
            df_all = pd.concat([df_all, df_tmp], ignore_index=True)

        # replace id column with full dive ids
        dive_statistics_all["group"] = group
        dive_statistics_all["id"] = id
        dive_statistics_all["dive_id"] = dive_id

        # set attributes
        self.tdr_collection = tdr_collection
        self.n_tdr = len(tdr_collection)
        self.n_dives = len(dive_statistics_all)
        self.dive_statistics_all = dive_statistics_all
        self.df_all = df_all

    # [METHODS] length of the class
    def __len__(self):
        return self.n_tdr

    # [METHODS] getter of the class
    def __getitem__(self, idx):
        return self.tdr_collection[idx]

    # [METHODS] string representation of the class
    def __repr__(self):
        return "%s(%d TDR, %d dives)" % (type(self).__name__, self.n_tdr, self.n_dives)

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    plot_stats_summary = diagnostic.plot_stats_summary
    indiv_depth_all = diagnostic.indiv_depth_all