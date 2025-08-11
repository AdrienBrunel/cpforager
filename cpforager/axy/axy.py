# ======================================================= #
# LIBRARIES
# ======================================================= #
import pandas as pd
from cpforager.gps.gps import GPS
from cpforager import processing
from cpforager.axy import diagnostic, display, interpolation


# ======================================================= #
# AXY CLASS
# ======================================================= #
class AXY:
    
    """
    A class to represent the AXY data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] AXY
    def __init__(self, df=pd.DataFrame, group=str, id=str, params=dict):
        
        """
        Constructor of an AXY object.
        
        :param df: the dataframe containing ``datetime``, ``ax``, ``ay``, ``az``, ``longitude``, ``latitude``, ``pressure`` and ``temperature`` columns. Type of ``datetime`` column must be datetime64.
        :type df: pandas.DataFrame
        :param group: the string representing the group to which the AXY data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :type group: str
        :param id: the string representing the unique identifier of the central-place foraging seabird.
        :type id: str
        :param params: the parameters dictionary.
        :type params: dict
        
        :ivar df: the dataframe containing the raw and processed AXY data.
        :type df: pandas.DataFrame
        :ivar group: The string representing the group to which the AXY data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :type group: str
        :ivar id: The string representing the unique identifier of the central-place foraging seabird.
        :type id: str
        :ivar params: The dictionary containing the parameters used for the AXY data processing.
        :type params: dict
        :ivar df_gps: the dataframe containing AXY data at GPS resolution.
        :type df_gps: pandas.DataFrame
        :ivar n_df_gps: the number of GPS measures.
        :type n_df_gps: int
        :ivar gps: the GPS object of AXY data at GPS resolution.
        :type gps: cpforager.GPS
        :ivar df_tdr: the dataframe containing AXY data at TDR resolution.
        :type df_tdr: pandas.DataFrame
        :ivar n_df_tdr: the number of TDR measures.
        :type n_df_tdr: int
        :ivar n_df: the number of measures in the AXY recording.
        :type n_df: int
        :ivar start_datetime:  the starting datetime of the AXY recording.
        :type start_datetime: datetime.datetime
        :ivar end_datetime: the ending datetime of the AXY recording.
        :type end_datetime: datetime.datetime
        :ivar frequency: the frequency of the AXY data in Hz.
        :type frequency: float
        :ivar total_duration: the total duration of the AXY recording in days.
        :type total_duration: float
        :ivar gps_resolution: the time resolution of the GPS data.
        :type gps_resolution: float
        :ivar total_length: the total length of the AXY recording in kilometers.
        :type total_length: float
        :ivar dmax: the maximum distance to the nest reached by the central place-foraging seabird.
        :type dmax: float
        :ivar n_trips: the number of foraging trips realised by the seabird.
        :type n_trips: int
        :ivar nest_position: the longitude and latitude of the estimated nest position.
        :type nest_position: [float, float]
        :ivar trip_statistics: the dataframe containing the trip statistics where one row corresponds to one foraging trip.
        :type trip_statistics: pandas.DataFrame  
        :ivar tdr_resolution: the time resolution of the TDR data.
        :type tdr_resolution: float      
        :ivar n_dives: the number of dives realised by the seabird.
        :type n_dives: int
        :ivar median_pressure: the median pressure in hPa.
        :type median_pressure: float
        :ivar median_depth: the median depth in meters.
        :type median_depth: float
        :ivar max_depth: the maximum depth in meters.
        :type max_depth: float
        :ivar mean_temperature: the mean temperature in °C.
        :type mean_temperature: float
        :ivar dive_statistics: the dataframe containing the dive statistics where one row corresponds to one dive.
        :type dive_statistics: pandas.DataFrame 
        :ivar max_odba: the maximum overall dynamical body acceleration.
        :type max_odba: float
        :ivar median_odba: the median overall dynamical body acceleration.
        :type median_odba: float
        :ivar max_odba_f: the maximum filtered overall dynamical body acceleration.
        :type max_odba_f: float
        :ivar median_odba_f: the median filtered overall dynamical body acceleration.
        :type median_odba_f: float
        
        .. todo::
            Better organise attributes and add TDR object as a field. Improve methods to benefit from the GPS and TDR methods (*e.g.* display)
        """

        # process data
        df, df_gps, df_tdr = processing.add_axy_data(df, params)

        # build GPS object
        gps = GPS(df_gps, group, id, params)

        # compute additional information
        basic_infos = processing.compute_basic_infos(df)
        basic_gps_infos = processing.compute_basic_infos(df_gps)
        basic_tdr_infos = processing.compute_basic_infos(df_tdr)
        gps_infos = processing.compute_gps_infos(df_gps, params)
        tdr_infos = processing.compute_tdr_infos(df_tdr)
        axy_infos = processing.compute_axy_infos(df)

        # set attributes
        self.df = df
        self.group = group
        self.id = id
        self.params = params
        self.df_gps = df_gps
        self.n_df_gps = len(df_gps)
        self.gps = gps
        self.df_tdr = df_tdr
        self.n_df_tdr = len(df_tdr)
        self.n_df = basic_infos["n_df"]
        self.start_datetime = basic_infos["start_datetime"]
        self.end_datetime = basic_infos["end_datetime"]
        self.frequency = 1/basic_infos["resolution"]
        self.total_duration = basic_infos["total_duration"]
        self.gps_resolution = basic_gps_infos["resolution"]
        self.total_length = gps_infos["total_length"]
        self.dmax = gps_infos["dmax"]
        self.n_trips = gps_infos["n_trips"]
        self.nest_position = gps_infos["nest_position"]
        self.trip_statistics = gps_infos["trip_statistics"]
        self.tdr_resolution = basic_tdr_infos["resolution"]
        self.n_dives = tdr_infos["n_dives"]
        self.median_pressure = tdr_infos["median_pressure"]
        self.median_depth = tdr_infos["median_depth"]
        self.max_depth = tdr_infos["max_depth"]
        self.mean_temperature = tdr_infos["mean_temperature"]
        self.dive_statistics = tdr_infos["dive_statistics"]
        self.max_odba = axy_infos["max_odba"]
        self.median_odba = axy_infos["median_odba"]
        self.max_odba_f = axy_infos["max_odba_f"]
        self.median_odba_f = axy_infos["median_odba_f"]

    # [BUILT-IN METHODS] length of the class
    def __len__(self):
        return self.n_df

    # [BUILT-IN METHODS] getter of the class
    def __getitem__(self, idx):
        return self.df.iloc[idx]

    # [BUILT-IN METHODS] string representation of the class
    def __repr__(self):
        return "%s(group=%s, id=%s, trips=%d, dives=%d, n=%d, n_gps=%d, n_tdr=%d)" % (type(self).__name__, self.group, self.id, self.n_trips, self.n_dives, self.n_df, self.n_df_gps, self.n_df_tdr)

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