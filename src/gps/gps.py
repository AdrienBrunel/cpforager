# ======================================================= #
# LIBRARIES
# ======================================================= #
import pandas as pd
from src import processing
from src.gps import diagnostic, display


# ======================================================= #
# BIOLOGGER SUPER-CLASS
# ======================================================= #
class GPS:
    
    # [CONSTRUCTOR] GPS
    def __init__(self, df=pd.DataFrame, group=str, id=str, params=dict):
                        
        # process data
        df = processing.add_gps_data(df, params)
        
        # compute additional information
        infos = processing.compute_gps_infos(df, params)
        
        # set attributes
        self.df = df
        self.group = group
        self.id = id
        self.params = params
        self.n_df = infos["n_df"]
        self.start_datetime = infos["start_datetime"]
        self.end_datetime = infos["end_datetime"]
        self.resolution = infos["resolution"]
        self.total_duration = infos["total_duration"]
        self.total_length = infos["total_length"]
        self.dmax = infos["dmax"]
        self.n_trip = infos["n_trip"]
        self.nest_position = infos["nest_position"]
        self.trip_statistics = infos["trip_statistics"]

        

    # [METHODS] string representation of the class 
    def __repr__(self):
        return "%s(group=%s, id=%s, trips=%d, n=%d)" % (type(self).__name__, self.group, self.id, self.n_trip, self.n_df)
        

    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary
    
    # [METHODS] plot data
    full_diag = diagnostic.full_diagnostic
    maps_diag = diagnostic.maps_diagnostic
    folium_map = diagnostic.folium_map
    folium_map_colorgrad = diagnostic.folium_map_colorgrad