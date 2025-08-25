# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import pandas as pd
import numpy as np
from cpforager.axy_collection import diagnostic, display, stdb
from cpforager.gps_collection.gps_collection import GPS_Collection
from cpforager.tdr_collection.tdr_collection import TDR_Collection


# ================================================================================================ #
# AXY_COLLECTION CLASS
# ================================================================================================ #
class AXY_Collection:
    
    """
    A class to represent a list of AXY data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] AXY_COLLECTION
    def __init__(self, axy_collection):
        
        """
        Constructor of an AXY_Collection object.
        
        :param axy_collection: the list of AXY.
        :type axy_collection: list[cpforager.AXY]
        
        :ivar axy_collection: the list of AXY.
        :vartype axy_collection: list[cpforager.AXY]
        :ivar n_axy: the total number of AXY included in the list.
        :vartype n_axy: int
        :ivar n_trips: the number of trips summed over every AXY included in the list.
        :vartype n_trips: str
        :ivar trip_statistics_all: the trip statistics dataframe merged over every AXY included in the list.
        :vartype trip_statistics_all: pandas.DataFrame
        :ivar n_dives: the number of dives summed over every AXY included in the list.
        :vartype n_dives: str
        :ivar dive_statistics_all: the dive statistics dataframe merged over every AXY included in the list.
        :vartype dive_statistics_all: pandas.DataFrame
        :ivar df_all: the enhanced AXY dataframe merged over every AXY included in the list.
        :vartype df_all: pandas.DataFrame
        """

        # init dataframes
        dtypes_1 = {"group":"str", "id":"str", "trip_id":"str", "length":"float", "duration":"float", "max_hole":"float", "dmax":"float", "n_step":"int"}
        trip_statistics_all = pd.DataFrame(columns=dtypes_1.keys())
        trip_statistics_all = trip_statistics_all.astype(dtype=dtypes_1)
        
        dtypes_2 = {"group":"str", "id":"str", "dive_id":"str", "duration":"float", "max_depth":"float"}
        dive_statistics_all = pd.DataFrame(columns=dtypes_2.keys())
        dive_statistics_all = dive_statistics_all.astype(dtype=dtypes_2)

        dtypes_3 = {"group":"str", "id":"str", "datetime":"object", "longitude":"float", "latitude":"float", "pressure":"float", "temperature":"float", "ax":"float", "ay":"float", "az":"float",
                    "step_time":"float", "step_length":"float", "step_speed":"float", "step_heading":"float","step_turning_angle":"float", 
                    "step_heading_to_colony":"float", "is_night":"int", "is_suspicious":"int", "dist_to_nest":"float", "trip":"int",
                    "depth":"float", "dive":"int",
                    "ax_f":"float", "ay_f":"float", "az_f":"float","odba":"float", "odba_f":"float"}
        df_all = pd.DataFrame(columns=dtypes_3.keys())
        df_all = df_all.astype(dtype=dtypes_3)

        # compute statistics
        group = []
        id = []
        trip_id = []
        dive_id = []
        gps_collection = []
        tdr_collection = []
        for axy in axy_collection:

            # display infos
            print(" # =========  [Group %s] - [Id %s] ========= #" % (axy.group, axy.id))

            # build the trip statisics dataframe of the entire collection
            group = np.concatenate((group, [axy.group for k in axy.df.loc[axy.df["trip"]>0, "trip"].unique()]))
            id = np.concatenate((id, [axy.id for k in axy.df.loc[axy.df["trip"]>0, "trip"].unique()]))
            trip_id = np.concatenate((trip_id, [f"{axy.group}_{axy.id}_T{k:04}" for k in axy.df.loc[axy.df["trip"]>0, "trip"].unique()]))
            trip_statistics_all = pd.concat([trip_statistics_all, axy.trip_statistics], ignore_index=True)
            
            # build the dive statisics dataframe of the entire collection
            group = np.concatenate((group, [axy.group for k in axy.df.loc[axy.df["dive"]>0, "dive"].unique()]))
            id = np.concatenate((id, [axy.id for k in axy.df.loc[axy.df["dive"]>0, "dive"].unique()]))
            dive_id = np.concatenate((dive_id, [f"{axy.group}_{axy.id}_D{k:04}" for k in axy.df.loc[axy.df["dive"]>0, "dive"].unique()]))
            dive_statistics_all = pd.concat([dive_statistics_all, axy.dive_statistics], ignore_index=True)

            # build the full data dataframe of the entire collection
            df_tmp = pd.DataFrame(columns=df_all.columns)
            df_tmp[["datetime", "longitude", "latitude", "pressure", "temperature", "ax", "ay", "az", "step_time", "step_length", 
                    "step_speed","step_heading", "step_turning_angle","step_heading_to_colony", "is_night", "is_suspicious", "dist_to_nest", "trip",
                    "depth", "dive", "ax_f", "ay_f", "az_f", "odba", "odba_f"]] = axy.df[["datetime", "longitude", "latitude", "pressure", "temperature", "ax", "ay", "az", "step_time", 
                                                                                          "step_length", "step_speed","step_heading", "step_turning_angle","step_heading_to_colony", "is_night", 
                                                                                          "is_suspicious", "dist_to_nest", "trip", "depth", "dive", "ax_f", "ay_f", "az_f", "odba", "odba_f"]]
            df_tmp = df_tmp.astype(dtype=dtypes_3)

            # add metadata in df for each trip
            df_tmp["id"] = axy.id
            df_tmp["group"] = axy.group
            df_all = pd.concat([df_all, df_tmp], ignore_index=True)
            
            # build gps and tdr collections
            gps_collection.append(axy.gps)
            tdr_collection.append(axy.tdr)

        # replace id column with full trip ids
        trip_statistics_all["group"] = group
        trip_statistics_all["id"] = id
        trip_statistics_all["trip_id"] = trip_id

        # set attributes
        self.axy_collection = axy_collection
        self.n_axy = len(axy_collection)
        self.gps_collection = GPS_Collection(gps_collection)
        self.tdr_collection = TDR_Collection(tdr_collection)
        self.n_trips = len(trip_statistics_all)
        self.trip_statistics_all = trip_statistics_all
        self.n_dives = len(dive_statistics_all)
        self.dive_statistics_all = dive_statistics_all
        self.df_all = df_all

    # [METHODS] length of the class
    def __len__(self):
        return self.n_axy

    # [METHODS] getter of the class
    def __getitem__(self, idx):
        return self.axy_collection[idx]

    # [METHODS] string representation of the class
    def __repr__(self):
        return "%s(%d AXY, %d trips)" % (type(self).__name__, self.n_axy, self.n_trips)

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    plot_trip_stats_summary = diagnostic.plot_trip_stats_summary
    plot_dive_stats_summary = diagnostic.plot_dive_stats_summary
    maps_diag = diagnostic.maps_diagnostic
    indiv_map_all = diagnostic.indiv_map_all
    indiv_depth_all = diagnostic.indiv_depth_all
    folium_map = diagnostic.folium_map