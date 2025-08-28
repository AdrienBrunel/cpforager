# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
from cpforager.axy_collection import diagnostic, display
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
        :vartype n_trips: int
        :ivar trip_statistics_all: the trip statistics dataframe merged over every AXY included in the list.
        :vartype trip_statistics_all: pandas.DataFrame
        :ivar n_dives: the number of dives summed over every AXY included in the list.
        :vartype n_dives: int
        :ivar dive_statistics_all: the dive statistics dataframe merged over every AXY included in the list.
        :vartype dive_statistics_all: pandas.DataFrame
        
        .. note ::
            To avoid memory overload, we do not build an overall dataframe that would result from all AXY data concatenation.
        """
        
        # loop over axy collection to build gps and tdr collections
        gps_collection = []
        tdr_collection = []
        for axy in axy_collection:
            gps_collection.append(axy.gps)
            tdr_collection.append(axy.tdr)
        
        # build GPS_Collection and TDR_Collection objects
        gps_collection = GPS_Collection(gps_collection)
        tdr_collection = TDR_Collection(tdr_collection)

        # set attributes
        self.axy_collection = axy_collection
        self.n_axy = len(axy_collection)
        self.gps_collection = gps_collection
        self.tdr_collection = tdr_collection
        self.n_trips = gps_collection.n_trips
        self.trip_statistics_all = gps_collection.trip_statistics_all
        self.n_dives = tdr_collection.n_dives
        self.dive_statistics_all = tdr_collection.dive_statistics_all

    # [METHODS] length of the class
    def __len__(self):
        return self.n_axy

    # [METHODS] getter of the class
    def __getitem__(self, idx):
        return self.axy_collection[idx]

    # [METHODS] string representation of the class
    def __repr__(self):
        return "%s(%d AXY, %d trips, %d dives)" % (type(self).__name__, self.n_axy, self.n_trips, self.n_dives)

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    plot_trip_stats_summary = diagnostic.plot_trip_stats_summary
    plot_dive_stats_summary = diagnostic.plot_dive_stats_summary
    maps_diag = diagnostic.maps_diagnostic
    indiv_map_all = diagnostic.indiv_map_all
    indiv_depth_all = diagnostic.indiv_depth_all
    folium_map = diagnostic.folium_map