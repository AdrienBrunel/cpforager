# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import pandas as pd
import numpy as np
from cpforager.gps_collection import diagnostic, display, stdb
from cpforager.gps.gps import GPS


# ================================================================================================ #
# GPS_COLLECTION CLASS
# ================================================================================================ #
class GPS_Collection:
    
    """
    A class to represent a list of GPS data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] GPS_COLLECTION
    def __init__(self, gps_collection=list[GPS]):
        
        """
        Constructor of a GPS_Collection object.
        
        :param gps_collection: the list of GPS.
        :type gps_collection: list[cpforager.GPS]
        
        :ivar gps_collection: the list of GPS.
        :vartype gps_collection: list[cpforager.GPS]
        :ivar n_gps: the total number of GPS included in the list.
        :vartype n_gps: int
        :ivar n_trips: the number of trips summed over every GPS included in the list.
        :vartype n_trips: str
        :ivar trip_statistics_all: the trip statistics dataframe merged over every GPS included in the list.
        :vartype trip_statistics_all: pandas.DataFrame
        :ivar df_all: the enhanced GPS dataframe merged over every GPS included in the list.
        :vartype df_all: pandas.DataFrame
        """

        # init dataframes
        dtypes_1 = {"group":"str", "id":"str", "trip_id":"str", "length":"float", "duration":"float", "max_hole":"float", "dmax":"float", "n_step":"int"}
        trip_statistics_all = pd.DataFrame(columns=dtypes_1.keys())
        trip_statistics_all = trip_statistics_all.astype(dtype=dtypes_1)

        dtypes_2 = {"group":"str", "id":"str", "datetime":"object", "longitude":"float", "latitude":"float",
                    "step_time":"float", "step_length":"float", "step_speed":"float", "step_heading":"float",
                    "step_turning_angle":"float", "step_heading_to_colony":"float", "is_night":"int", "is_suspicious":"int", 
                    "dist_to_nest":"float", "trip":"int"}
        df_all = pd.DataFrame(columns=dtypes_2.keys())
        df_all = df_all.astype(dtype=dtypes_2)

        # compute statistics
        group = []
        id = []
        trip_id = []
        for gps in gps_collection:

            # display infos
            print(" # =========  [Group %s] - [Id %s] ========= #" % (gps.group, gps.id))

            # build the trip statisics dataframe of the entire collection
            group = np.concatenate((group, [gps.group for k in gps.df.loc[gps.df["trip"]>0, "trip"].unique()]))
            id = np.concatenate((id, [gps.id for k in gps.df.loc[gps.df["trip"]>0, "trip"].unique()]))
            trip_id = np.concatenate((trip_id, [f"{gps.group}_{gps.id}_T{k:04}" for k in gps.df.loc[gps.df["trip"]>0, "trip"].unique()]))
            trip_statistics_all = pd.concat([trip_statistics_all, gps.trip_statistics], ignore_index=True)

            # build the full data dataframe of the entire collection
            df_tmp = pd.DataFrame(columns=df_all.columns)
            df_tmp[["datetime", "longitude", "latitude", "step_time", "step_length", "step_speed","step_heading", 
                    "step_turning_angle","step_heading_to_colony", "is_night", "is_suspicious", "dist_to_nest", "trip"]] = gps.df[["datetime", "longitude", "latitude", "step_time", "step_length", "step_speed", "step_heading",
                                                                                                                                   "step_turning_angle", "step_heading_to_colony", "is_night", "is_suspicious", "dist_to_nest", "trip"]]
            df_tmp = df_tmp.astype(dtype=dtypes_2)

            # add metadata in df for each trip
            df_tmp["id"] = gps.id
            df_tmp["group"] = gps.group
            df_all = pd.concat([df_all, df_tmp], ignore_index=True)

        # replace id column with full trip ids
        trip_statistics_all["group"] = group
        trip_statistics_all["id"] = id
        trip_statistics_all["trip_id"] = trip_id

        # set attributes
        self.gps_collection = gps_collection
        self.n_gps = len(gps_collection)
        self.n_trips = len(trip_statistics_all)
        self.trip_statistics_all = trip_statistics_all
        self.df_all = df_all

    # [METHODS] length of the class
    def __len__(self):
        return self.n_gps

    # [METHODS] getter of the class
    def __getitem__(self, idx):
        return self.gps_collection[idx]

    # [METHODS] string representation of the class
    def __repr__(self):
        return "%s(%d GPS, %d trips)" % (type(self).__name__, self.n_gps, self.n_trips)

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    plot_stats_summary = diagnostic.plot_stats_summary
    maps_diag = diagnostic.maps_diagnostic
    folium_map = diagnostic.folium_map
    
    # [METHODS] Seabird Tracking Database formatting
    to_SeabirdTracking = stdb.convert_to_stdb_format