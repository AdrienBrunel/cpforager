# ======================================================= #
# LIBRARIES
# ======================================================= #
import pandas as pd
from src.gps.gps import GPS
from src import processing
from src.axy import diagnostic, display


# ======================================================= #
# BIOLOGGER SUPER-CLASS
# ======================================================= #
class AXY:

    # [CONSTRUCTOR] GPS
    def __init__(self, df=pd.DataFrame, group=str, id=str, params=dict):

        # process data
        df, df_gps, df_tdr = processing.add_axy_data(df, params)

        # build GPS object
        gps = GPS(df_gps, group, id, params)

        # compute additional information
        basic_infos = processing.compute_basic_infos(df)
        basic_gps_infos = processing.compute_basic_infos(df_gps)
        gps_infos = processing.compute_gps_infos(df_gps, params)
        tdr_infos = processing.compute_tdr_infos(df)
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
        self.n_trip = gps_infos["n_trip"]
        self.nest_position = gps_infos["nest_position"]
        self.trip_statistics = gps_infos["trip_statistics"]
        self.nb_dives = tdr_infos["nb_dives"]
        self.median_pressure = tdr_infos["median_pressure"]
        self.median_depth = tdr_infos["median_depth"]
        self.mean_temperature = tdr_infos["mean_temperature"]
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
        return "%s(group=%s, id=%s, trips=%d, n=%d, n_gps=%d, n_tdr=%d)" % (type(self).__name__, self.group, self.id, self.n_trip, self.n_df, self.n_df_gps, self.n_df_tdr)

    # # [METHODS] interpolate data
    # interpolate_lat_lon = interpolation.interpolate_lat_lon

    # # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary

    # # [METHODS] plot data
    full_diag = diagnostic.full_diagnostic
    maps_diag = diagnostic.maps_diagnostic
    folium_map = diagnostic.folium_map
    folium_map_wtrips = diagnostic.folium_map_wtrips
    folium_map_colorgrad = diagnostic.folium_map_colorgrad