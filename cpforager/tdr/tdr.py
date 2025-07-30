# ======================================================= #
# LIBRARIES
# ======================================================= #
import pandas as pd
from cpforager import processing
from cpforager.tdr import diagnostic, display


# ======================================================= #
# BIOLOGGER SUPER-CLASS
# ======================================================= #
class TDR:

    # [CONSTRUCTOR] TDR
    def __init__(self, df=pd.DataFrame, group=str, id=str, params=dict):
        """
        Parameters
        ----------
        df : pandas.DataFrame
            The dataframe containing "datetime", "pressure" and "temperature" columns. Type of "datetime" column must be converted to datetime64.
        group : str
            The string representing the group to which the TDR data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        id : str
            The string representing the unique identifier of the central-place foraging seabird.
        params : dict
            The dictionary of parameters.
        """
        # process data
        df = processing.add_tdr_data(df, params)

        # compute additional information
        basic_infos = processing.compute_basic_infos(df)
        tdr_infos = processing.compute_tdr_infos(df, params)

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
        self.nb_dives = tdr_infos["nb_dives"]
        self.median_pressure = tdr_infos["median_pressure"]
        self.median_depth = tdr_infos["median_depth"]
        self.mean_temperature = tdr_infos["mean_temperature"]
        
    # [BUILT-IN METHODS] length of the class
    def __len__(self):
        return self.n_df

    # [BUILT-IN METHODS] getter of the class
    def __getitem__(self, idx):
        return self.df.iloc[idx]

    # [BUILT-IN METHODS] string representation of the class
    def __repr__(self):
        return "%s(group=%s, id=%s, dives=%d, n=%d)" % (type(self).__name__, self.group, self.id, self.nb_dives, self.n_df)

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # [METHODS] plot data
    full_diag = diagnostic.full_diagnostic
