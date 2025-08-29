# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import pandas as pd
import numpy as np
from cpforager.gps_tdr_collection import diagnostic, display
from cpforager.gps_collection.gps_collection import GPS_Collection
from cpforager.tdr_collection.tdr_collection import TDR_Collection


# ================================================================================================ #
# GPS_TDR_COLLECTION CLASS
# ================================================================================================ #
class GPS_TDR_Collection:
    
    """
    A class to represent a list of GPS_TDR data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] GPS_TDR_COLLECTION
    def __init__(self, gps_tdr_collection):
        
        """
        Constructor of a GPS_TDR_Collection object.
        
        :param gps_tdr_collection: the list of GPS_TDR.
        :type gps_tdr_collection: list[cpforager.GPS_TDR]
        
        :ivar gps_tdr_collection: the list of GPS_TDR.
        :vartype gps_tdr_collection: list[cpforager.GPS_TDR]
        :ivar n_gps_tdr: the total number of GPS_TDR included in the list.
        :vartype n_gps_tdr: int
        :ivar n_trips: the number of trips summed over every GPS_TDR included in the list.
        :vartype n_trips: int
        :ivar trip_statistics_all: the trip statistics dataframe merged over every GPS_TDR included in the list.
        :vartype trip_statistics_all: pandas.DataFrame
        :ivar n_dives: the number of dives summed over every GPS_TDR included in the list.
        :vartype n_dives: int
        :ivar dive_statistics_all: the dive statistics dataframe merged over every GPS_TDR included in the list.
        :vartype dive_statistics_all: pandas.DataFrame
        :ivar df_all: the enhanced GPS_TDR dataframe merged over every GPS_TDR included in the list.
        :vartype df_all: pandas.DataFrame
        """

        # loop over gps_tdr collection to build gps and tdr collections
        gps_collection = []
        tdr_collection = []
        for gps_tdr in gps_tdr_collection:
            gps_collection.append(gps_tdr.gps)
            tdr_collection.append(gps_tdr.tdr)
        
        # build GPS_Collection and TDR_Collection objects
        gps_collection = GPS_Collection(gps_collection)
        tdr_collection = TDR_Collection(tdr_collection)

        # set attributes
        self.gps_tdr_collection = gps_tdr_collection
        self.n_gps_tdr = len(gps_tdr_collection)
        self.gps_collection = gps_collection
        self.tdr_collection = tdr_collection
        self.n_trips = gps_collection.n_trips
        self.trip_statistics_all = gps_collection.trip_statistics_all
        self.n_dives = tdr_collection.n_dives
        self.dive_statistics_all = tdr_collection.dive_statistics_all

    # [METHODS] length of the class
    def __len__(self):
        return self.n_gps_tdr

    # [METHODS] getter of the class
    def __getitem__(self, idx):
        return self.gps_tdr_collection[idx]

    # [METHODS] string representation of the class
    def __repr__(self):
        return "%s(%d GPS_TDR, %d trips, %d dives)" % (type(self).__name__, self.n_gps_tdr, self.n_trips, self.n_dives)

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    plot_trip_stats_summary = diagnostic.plot_trip_stats_summary
    plot_dive_stats_summary = diagnostic.plot_dive_stats_summary
    maps_diag = diagnostic.maps_diagnostic
    indiv_map_all = diagnostic.indiv_map_all
    indiv_depth_all = diagnostic.indiv_depth_all
    folium_map = diagnostic.folium_map