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
    
    """
    A class to represent the GPS data of a central-place foraging seabird.

    ...

    Attributes
    ----------
    df : pandas.DataFrame
        The dataframe containing the raw and processed GPS data.
    group : str
        The string representing the group to which the GPS data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
    id : str
        The string representing the unique identifier of the central-place foraging seabird.
    params : dict
        The dictionary containing the parameters used for the GPS data processing.
    n_df : int
        The number of measures in the GPS recording.
    start_datetime : datetime.datetime
        The starting datetime of the GPS recording.
    end_datetime : datetime.datetime
        The ending datetime of the GPS recording.
    resolution : float
        The time resolution of the GPS data in seconds estimated as the median value of the step times.
    total_duration : float
        The total duration of the GPS recording in days.
    total_length : float
        The total length of the GPS recording in kilometers.
    dmax : float
        The maximum distance to the nest reached by the central place-foraging seabird.
    n_trip : int
        The number of foraging trips realised by the seabird.
    nest_position : [float, float]
        The longitude and latitude of the estimated nest position.
    trip_statistics : pandas.DataFrame
        The dataframe containing the trip statistics where one row corresponds to one foraging trip.
        
    Methods
    -------
    display_data_summary()
        Prints the GPS data summary.
    full_diag()
        Produces the full diagnostic of the GPS data.
    maps_diag()
        Produces the maps of the GPS data.
    folium_map()
        Produces the html map of the GPS data.
    folium_map_colorgrad()
        Produces the html map of the GPS data with a speed color gradient.
    """
    
    # [CONSTRUCTOR] GPS
    def __init__(self, df=pd.DataFrame, group=str, id=str, params=dict):
        """
        Parameters
        ----------
        df : pandas.DataFrame
            The dataframe containing "datetime", "longitude" and "latitude" columns. Type of "datetime" column must be converted to datetime64.
        group : str
            The string representing the group to which the GPS data belongs (*e.g.* species, year, fieldwork, *etc*.) useful for statistics and filtering.
        id : str
            The string representing the unique identifier of the central-place foraging seabird.
        params : dict
            The dictionary of parameters.
        """           
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
        
    # [BUILT-IN METHODS] length of the class 
    def __len__(self):
        return self.n_df
    
    # [BUILT-IN METHODS] getter of the class 
    def __getitem__(self, idx):
        return self.df.iloc[idx]
        
    # [BUILT-IN METHODS] string representation of the class 
    def __repr__(self):
        return "%s(group=%s, id=%s, trips=%d, n=%d)" % (type(self).__name__, self.group, self.id, self.n_trip, self.n_df)
        
    # [METHODS] display the summary of the data
    display_data_summary = display.display_data_summary
    
    # [METHODS] plot data
    full_diag = diagnostic.full_diagnostic
    maps_diag = diagnostic.maps_diagnostic
    folium_map = diagnostic.folium_map
    folium_map_wtrips = diagnostic.folium_map_wtrips
    folium_map_colorgrad = diagnostic.folium_map_colorgrad