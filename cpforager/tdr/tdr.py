# ======================================================= #
# LIBRARIES
# ======================================================= #
import pandas as pd
from cpforager import processing
from cpforager.tdr import diagnostic, display


# ======================================================= #
# TDR CLASS
# ======================================================= #
class TDR:
    """
    A class to represent the TDR data of a central-place foraging seabird.
    """

    # [CONSTRUCTOR] TDR
    def __init__(self, df=pd.DataFrame, group=str, id=str, params=dict):
        
        """
        Constructor of a TDR object.
        
        :param df: the dataframe containing ``datetime``, ``pressure`` and ``temperature`` columns. Type of ``datetime`` column must be datetime64.
        :type df: pandas.DataFrame
        :param group: the string representing the group to which the TDR data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :type group: str
        :param id: the string representing the unique identifier of the central-place foraging seabird.
        :type id: str
        :param params: the parameters dictionary.
        :type params: dict
        
        :ivar df: the dataframe containing the raw and processed TDR data.
        :type df: pandas.DataFrame
        :ivar group: The string representing the group to which the TDR data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        :type group: str
        :ivar id: The string representing the unique identifier of the central-place foraging seabird.
        :type id: str
        :ivar params: The dictionary containing the parameters used for the TDR data processing.
        :type params: dict
        :ivar n_df: the number of measures in the TDR recording.
        :type n_df: int
        :ivar start_datetime:  the starting datetime of the TDR recording.
        :type start_datetime: datetime.datetime
        :ivar end_datetime: the ending datetime of the TDR recording.
        :type end_datetime: datetime.datetime
        :ivar resolution: the time resolution of the TDR data in seconds estimated as the median value of the step times.
        :type resolution: float
        :ivar total_duration: the total duration of the TDR recording in days.
        :type total_duration: float
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
        """
        
        # process data
        df = processing.add_tdr_data(df, params)

        # compute additional information
        basic_infos = processing.compute_basic_infos(df)
        tdr_infos = processing.compute_tdr_infos(df)

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
        self.n_dives = tdr_infos["n_dives"]
        self.median_pressure = tdr_infos["median_pressure"]
        self.median_depth = tdr_infos["median_depth"]
        self.max_depth = tdr_infos["max_depth"]
        self.mean_temperature = tdr_infos["mean_temperature"]
        self.dive_statistics = tdr_infos["dive_statistics"]
        
    # [BUILT-IN METHODS] length of the class
    def __len__(self):
        return self.n_df

    # [BUILT-IN METHODS] getter of the class
    def __getitem__(self, idx):
        return self.df.iloc[idx]

    # [BUILT-IN METHODS] string representation of the class
    def __repr__(self):
        return "%s(group=%s, id=%s, dives=%d, n=%d)" % (type(self).__name__, self.group, self.id, self.n_dives, self.n_df)

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    full_diag = diagnostic.full_diagnostic
