# ======================================================= #
# LIBRARIES
# ======================================================= #
from cpforager.gps.gps import GPS
from cpforager.tdr.tdr import TDR
from cpforager import processing
from cpforager.gps_tdr import display, diagnostic, interpolation


# ======================================================= #
# GPS_TDR CLASS
# ======================================================= #
class GPS_TDR:

    """
    A class to represent the GPS and TDR data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] GPS_TDR
    def __init__(self, df, group, id, params):
        
        """
        Constructor of a GPS_TDR object.
        
        :param df: the dataframe containing ``datetime``, ``longitude``, ``latitude``, ``pressure`` and ``temperature`` columns. Type of ``datetime`` column must be datetime64.
        :type df: pandas.DataFrame
        :param group: the string representing the group to which the GPS data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :type group: str
        :param id: the string representing the unique identifier of the central-place foraging seabird.
        :type id: str
        :param params: the parameters dictionary.
        :type params: dict
        
        :ivar df: the dataframe containing the merged GPS and TDR data.
        :vartype df: pandas.DataFrame
        :ivar group: The string representing the group to which the AXY data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :vartype group: str
        :ivar id: The string representing the unique identifier of the central-place foraging seabird.
        :vartype id: str
        :ivar params: The dictionary containing the parameters used for the AXY data processing.
        :vartype params: dict
        :ivar n_df: the number of measures in the merged GPS and TDR recording.
        :vartype n_df: int
        :ivar gps: the GPS data of GPS_TDR at GPS resolution.
        :vartype gps: cpforager.GPS
        :ivar df_gps: the dataframe containing the GPS data.
        :vartype df_gps: pandas.DataFrame
        :ivar tdr: the TDR data of GPS_TDR at TDR resolution.
        :vartype tdr: cpforager.TDR
        :ivar df_tdr: the dataframe containing the TDR data.
        :vartype df_tdr: pandas.DataFrame
        :ivar start_datetime:  the starting datetime of the merged GPS and TDR recording.
        :vartype start_datetime: datetime.datetime
        :ivar end_datetime: the ending datetime of the merged GPS and TDR recording.
        :vartype end_datetime: datetime.datetime
        :ivar resolution: the time resolution of the GPS_TDR data in seconds estimated as the median value of the step times.
        :vartype resolution: float
        :ivar total_duration: the total duration of the merged GPS and TDR recording in days.
        :vartype total_duration: float   
        """
        
        # process data
        df, df_gps, df_tdr = processing.add_gps_tdr_data(df, params)
        
        # build GPS object
        gps = GPS(df_gps, group, id, params)
        
        # build TDR object
        tdr = TDR(df_tdr, group, id, params)

        # compute additional information
        basic_infos = processing.compute_basic_infos(df)
        
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
        self.gps = gps
        self.df_gps = df_gps
        self.tdr = tdr
        self.df_tdr = df_tdr

    # [BUILT-IN METHODS] length of the class
    def __len__(self):
        return self.n_df

    # [BUILT-IN METHODS] getter of the class
    def __getitem__(self, idx):
        return self.df.iloc[idx]

    # [BUILT-IN METHODS] string representation of the class
    def __repr__(self):
        return "%s(group=%s, id=%s, trips=%d, dives=%d, n=%d, n_gps=%d, n_tdr=%d)" % (type(self).__name__, self.group, self.id, self.gps.n_trips, self.tdr.n_dives, self.n_df, self.gps.n_df, self.tdr.n_df)

    # [METHODS] interpolate data
    interpolate_lat_lon = interpolation.interpolate_lat_lon

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    full_diag = diagnostic.full_diagnostic
    maps_diag = diagnostic.maps_diagnostic
    folium_map = diagnostic.folium_map