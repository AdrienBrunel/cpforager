# ======================================================= #
# LIBRARIES
# ======================================================= #
import pandas as pd
from cpforager import processing
from cpforager.gps import diagnostic, display, interpolation


# ======================================================= #
# GPS CLASS
# ======================================================= #
class GPS:

    """
    A class to represent the GPS data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] GPS
    def __init__(self, df=pd.DataFrame, group=str, id=str, params=dict):
        
        """
        Constructor of a GPS object.
        
        :param df: the dataframe containing ``datetime``, ``longitude`` and ``latitude`` columns. Type of ``datetime`` column must be datetime64.
        :type df: pandas.DataFrame
        :param group: the string representing the group to which the GPS data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :type group: str
        :param id: the string representing the unique identifier of the central-place foraging seabird.
        :type id: str
        :param params: the parameters dictionary.
        :type params: dict
        
        :ivar df: the dataframe containing the raw and processed GPS data.
        :type df: pandas.DataFrame
        :ivar group: The string representing the group to which the GPS data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :type group: str
        :ivar id: The string representing the unique identifier of the central-place foraging seabird.
        :type id: str
        :ivar params: The dictionary containing the parameters used for the GPS data processing.
        :type params: dict
        :ivar n_df: the number of measures in the GPS recording.
        :type n_df: int
        :ivar start_datetime:  the starting datetime of the GPS recording.
        :type start_datetime: datetime.datetime
        :ivar end_datetime: the ending datetime of the GPS recording.
        :type end_datetime: datetime.datetime
        :ivar resolution: the time resolution of the GPS data in seconds estimated as the median value of the step times.
        :type resolution: float
        :ivar total_duration: the total duration of the GPS recording in days.
        :type total_duration: float
        :ivar total_length: the total length of the GPS recording in kilometers.
        :type total_length: float
        :ivar dmax: the maximum distance to the nest reached by the central place-foraging seabird.
        :type dmax: float
        :ivar n_trips: the number of foraging trips realised by the seabird.
        :type n_trips: int
        :ivar nest_position: the longitude and latitude of the estimated nest position.
        :type nest_position: [float, float]
        :ivar trip_statistics: the dataframe containing the trip statistics where one row corresponds to one foraging trip.
        :type trip_statistics: pandas.DataFrame        
        """
        
        # process data
        df = processing.add_gps_data(df, params)

        # compute additional information
        basic_infos = processing.compute_basic_infos(df)
        gps_infos = processing.compute_gps_infos(df, params)

        # set attributes
        self.df = df
        self.group = group
        self.id = id
        self.params = params
        self.n_df = basic_infos["n_df"]
        self.start_datetime = basic_infos["start_datetime"]
        self.end_datetime = basic_infos["end_datetime"]
        self.resolution = basic_infos["resolution"]
        self.total_duration = basic_infos["total_duration"]
        self.total_length = gps_infos["total_length"]
        self.dmax = gps_infos["dmax"]
        self.n_trips = gps_infos["n_trips"]
        self.nest_position = gps_infos["nest_position"]
        self.trip_statistics = gps_infos["trip_statistics"]

    # [BUILT-IN METHODS] length of the class
    def __len__(self):
        return self.n_df

    # [BUILT-IN METHODS] getter of the class
    def __getitem__(self, idx):
        return self.df.iloc[idx]

    # [BUILT-IN METHODS] string representation of the class
    def __repr__(self):
        return "%s(group=%s, id=%s, trips=%d, n=%d)" % (type(self).__name__, self.group, self.id, self.n_trips, self.n_df)

    # [METHODS] interpolate data
    interpolate_lat_lon = interpolation.interpolate_lat_lon

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    full_diag = diagnostic.full_diagnostic
    maps_diag = diagnostic.maps_diagnostic
    folium_map = diagnostic.folium_map
    folium_map_wtrips = diagnostic.folium_map_wtrips
    folium_map_colorgrad = diagnostic.folium_map_colorgrad