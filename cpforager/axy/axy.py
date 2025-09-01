# ======================================================= #
# LIBRARIES
# ======================================================= #
from cpforager.gps.gps import GPS
from cpforager.tdr.tdr import TDR
from cpforager import processing
from cpforager.axy import display, diagnostic, interpolation


# ======================================================= #
# AXY CLASS
# ======================================================= #
class AXY:
    
    """
    A class to represent the AXY data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] AXY
    def __init__(self, df, group, id, params):
        
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
        :vartype df: pandas.DataFrame
        :ivar group: The string representing the group to which the AXY data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :vartype group: str
        :ivar id: The string representing the unique identifier of the central-place foraging seabird.
        :vartype id: str
        :ivar params: The dictionary containing the parameters used for the AXY data processing.
        :vartype params: dict
        :ivar n_df: the number of measures in the AXY recording.
        :vartype n_df: int
        :ivar gps: the GPS data of AXY at GPS resolution.
        :vartype gps: cpforager.GPS
        :ivar df_gps: the dataframe containing AXY data at GPS resolution.
        :vartype df_gps: pandas.DataFrame
        :ivar tdr: the TDR data of AXY at TDR resolution.
        :vartype tdr: cpforager.TDR
        :ivar df_tdr: the dataframe containing AXY data at TDR resolution.
        :vartype df_tdr: pandas.DataFrame
        :ivar start_datetime:  the starting datetime of the AXY recording.
        :vartype start_datetime: datetime.datetime
        :ivar end_datetime: the ending datetime of the AXY recording.
        :vartype end_datetime: datetime.datetime
        :ivar frequency: the frequency of the AXY data in Hz.
        :vartype frequency: float
        :ivar total_duration: the total duration of the AXY recording in days.
        :vartype total_duration: float
        :ivar max_odba: the maximum overall dynamical body acceleration.
        :vartype max_odba: float
        :ivar median_odba: the median overall dynamical body acceleration.
        :vartype median_odba: float
        :ivar max_odba_f: the maximum filtered overall dynamical body acceleration.
        :vartype max_odba_f: float
        :ivar median_odba_f: the median filtered overall dynamical body acceleration.
        :vartype median_odba_f: float        
        """

        # process data
        df, df_gps, df_tdr = processing.add_axy_data(df, params)

        # build GPS object
        gps = GPS(df_gps, group, id, params)
        
        # build TDR object
        tdr = TDR(df_tdr, group, id, params)

        # compute additional information
        basic_infos = processing.compute_basic_infos(df)
        axy_infos = processing.compute_axy_infos(df)

        # set attributes
        self.df = df
        self.group = group
        self.id = id
        self.params = params
        self.n_df = basic_infos["n_df"]
        self.start_datetime = basic_infos["start_datetime"]
        self.end_datetime = basic_infos["end_datetime"]
        self.frequency = 1/basic_infos["resolution"]
        self.total_duration = basic_infos["total_duration"]
        self.max_odba = axy_infos["max_odba"]
        self.median_odba = axy_infos["median_odba"]
        self.max_odba_f = axy_infos["max_odba_f"]
        self.median_odba_f = axy_infos["median_odba_f"]
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