# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import numpy as np
import pandas as pd
from cpforager import utils, constants, check, parameters
from suntime import Sun
import pytz
from scipy.signal import butter, filtfilt


# ================================================================================================ #
# ESTIMATION OF THE NEST POSITION
# ================================================================================================ #
def estimate_nest_position(df, params, verbose=False):
     
    """   
    Estimate the nest position from longitude and latitude data.
        
    :param df: dataframe with ``longitude`` and ``latitude`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :param verbose: display information if True.
    :type verbose: bool
    :return: the estimated nest position.
    :rtype: [float, float] 
    
    If not known beforehand, the nest position is estimated as the median position among positions inside the 
    colony rectangle with a small enough speed. If not possible, the nest position is estimated at the center of 
    the colony. 
    
    .. note::
        The required fields in the parameters dictionary are ``colony``, ``nesting_speed`` and ``nest_position``.
    """
    
    # get parameters
    colony = params.get("colony")
    nesting_speed = params.get("nesting_speed")
    nest_position = params.get("nest_position")
    
    # consider only the positions inside the colony rectangle
    at_colony = ((df["longitude"] >= colony["box_longitude"][0]) &
                 (df["longitude"] <= colony["box_longitude"][1]) & 
                 (df["latitude"] >= colony["box_latitude"][0]) & 
                 (df["latitude"] <= colony["box_latitude"][1]))
    
    # consider only the positions with a small enough speed
    low_speed = (df["step_speed"] < nesting_speed)

    # nest position is estimated as the median of the positions left (low speed and inside colony)
    if(nest_position is None):
        if((at_colony & low_speed).sum() > 0):
            nest_lon = df["longitude"][at_colony & low_speed].median()
            nest_lat = df["latitude"][at_colony & low_speed].median()
        else:
            if(at_colony.sum() > 0):
                nest_lon = df["longitude"][at_colony].median()
                nest_lat = df["latitude"][at_colony].median()
            else:
                nest_lon = colony["center"][0]
                nest_lat = colony["center"][1]
                if verbose: print("WARNING : cannot estimate a nest position, took the colony position (%.5f, %.5f) instead" % (nest_lon, nest_lat))
        nest_position = [nest_lon, nest_lat]
        
    return(nest_position)


# ================================================================================================ #
# IS NIGHT
# ================================================================================================ #
def add_is_night(df, params):
    
    """
    Add to the dataframe an additional ``is_night`` boolean column worth 1 if it is night, 0 otherwise.
    
    :param df: dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe with an additional ``is_night`` boolean column worth 1 if it is night, 0 otherwise.
    :rtype: pandas.DataFrame
    
    The boolean value is computed using suntime and pytz Python package. Night is defined using the sunrise and sunset 
    times at the colony center.
    
    .. note::
        The required fields in the parameters dictionary are ``colony`` and ``local_tz``.
        
    .. warning::
        Dataframe ``datetime`` column must be at local time. The accuracy of ``is_night`` column depends on it.
    """

    # get parameters
    colony = params.get("colony")
    local_timezone = params.get("local_tz")
    
    # lon/lat of colony
    colony_lon = colony["center"][0]
    colony_lat = colony["center"][1]
    
    # first row of datetime
    datetime_0 = df.loc[0, "datetime"]
    
    # derive sunrise and sunset    
    sunrise = Sun(colony_lat, colony_lon).get_sunrise_time(datetime_0).astimezone(pytz.timezone(local_timezone))
    sunset = Sun(colony_lat, colony_lon).get_sunset_time(datetime_0).astimezone(pytz.timezone(local_timezone))
    
    # add column to dataframe
    df["is_night"] = (df["datetime"].dt.time < sunrise.time()) | (df["datetime"].dt.time > sunset.time())

    # reformat column
    df["is_night"] = df["is_night"].astype(int)

    return(df)


# ================================================================================================ #
# STEP TIME
# ================================================================================================ #
def add_step_time(df):
    
    """   
    Add to the dataframe an additional ``step_time`` column that gives the step time in seconds.
     
    :param df: dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :return: the dataframe with an additional ``step_time`` column that gives the step time in seconds.
    :rtype: pandas.DataFrame
    
    Step time is computed as the duration in seconds between consecutive measures of position.
    
    .. warning::
        First step time value is NaN.
    """
    
    # compute step time in seconds
    df["step_time"] = (df["datetime"] - df["datetime"].shift(1)).dt.total_seconds()

    # reformat column
    df["step_time"] = df["step_time"]

    return(df)


# ================================================================================================ #
# STEP LENGTH
# ================================================================================================ #
def add_step_length(df):
    
    """    
    Add to the dataframe an additional ``step_length`` column that gives the step length in kilometers.
    
    :param df: dataframe with ``longitude`` and ``latitude`` columns.
    :type df: pandas.DataFrame
    :return: the dataframe with an additional ``step_length`` column that gives the step length in kilometers.
    :rtype: pandas.DataFrame
    
    Step length is computed as the length in kilometers between consecutive measures of position.
    
    .. warning::
        First step length value is NaN.
    """
    
    # compute step distance in km
    df["step_length"]  = utils.ortho_distance(df["longitude"].shift(1), df["latitude"].shift(1), df["longitude"], df["latitude"])

    # reformat column
    df["step_length"] = df["step_length"].round(3)

    return(df)


# ================================================================================================ #
# STEP SPEED
# ================================================================================================ #
def add_step_speed(df):
    
    """    
    Add to the dataframe an additional ``step_speed`` column that gives the step ground speed in kilometers per hour.
    
    :param df: dataframe with ``step_time`` and ``step_length`` columns.
    :type df: pandas.DataFrame
    :return: the dataframe with an additional ``step_speed`` column that gives the step ground speed in kilometers per hour.
    :rtype: pandas.DataFrame
    
    Step speed is computed as the average ground speed in kilometers per hour between consecutive measures of position.
    
    .. warning::
        First step speed value is NaN.
    """

    # compute step distance in km
    dist_in_km = df["step_length"]
    
    # compute step time in hour
    dt_in_hours = df["step_time"]/3600

    # compute step speed in km/h
    df["step_speed"]  = dist_in_km/dt_in_hours

    # reformat column
    df["step_speed"] = df["step_speed"].round(3)

    return(df)


# ================================================================================================ #
# STEP HEADING
# ================================================================================================ #
def add_step_heading(df):
    
    """    
    Add to the dataframe an additional ``step_heading`` column that gives step heading in degrees.
    
    :param df: dataframe with ``longitude`` and ``latitude`` columns.
    :type df: pandas.DataFrame
    :return: the dataframe with an additional ``step_heading`` column that gives step heading in degrees. 
    :rtype: pandas.DataFrame
    
    Step heading is computed as the angle in degrees between the North and the direction formed by 
    two consecutive measures of position (N=0°, E=90°, S=180°, W=270°).
    
    .. warning::
        First step heading value is NaN.
    """
    
    # compute step heading
    df["step_heading"] = utils.spherical_heading(df["longitude"].shift(1), df["latitude"].shift(1), df["longitude"], df["latitude"])

    # reformat column
    df["step_heading"] = df["step_heading"].round(1)

    return(df)


# ================================================================================================ #
# STEP TURNING ANGLE
# ================================================================================================ #
def add_step_turning_angle(df):
    
    """    
    Add to the dataframe an additional ``step_turning_angle`` column that gives the step turning angle in degrees (between -180° and +180°). 
    
    :param df: dataframe with a ``step_heading`` column.
    :type df: pandas.DataFrame
    :return: the dataframe with an additional ``step_turning_angle`` column that gives the step turning angle in degrees (between -180° and +180°). 
    :rtype: pandas.DataFrame
    
    Step turning angle is computed as the difference of step heading between consecutive measures of position.
    
    .. warning::
        First two step turning angle values are NaN.
    """
    
    # compute step turning angle
    dheading = np.diff(df["step_heading"])
    cond = (dheading % 360) > 180
    dheading[cond] = (dheading[cond] % 360) - 360
    dheading[~cond] = (dheading[~cond] % 360)

    # add step turning angle to dataframe
    df["step_turning_angle"] = np.concatenate([[np.nan], dheading])

    # reformat column
    df["step_turning_angle"] = df["step_turning_angle"].round(1)

    return(df)


# ================================================================================================ #
# STEP HEADING TO COLONY
# ================================================================================================ #
def add_step_heading_to_colony(df, params):
    
    """    
    Add to the dataframe an additional ``step_heading_to_colony`` column that gives heading to the colony in degrees. 
    
    :param df: dataframe with ``longitude`` and ``latitude`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary.
    :type params: dict
    :return: the dataframe with an additional ``step_heading_to_colony`` column that gives heading to the colony in degrees. 
    :rtype: pandas.DataFrame
    
    .. note::
        The required fields in the parameters dictionary are ``colony``.
    """
    
    # get parameters
    colony = params.get("colony")
    colony_lon = colony["center"][0]
    colony_lat = colony["center"][1]
    
    # compute step heading
    df["step_heading_to_colony"] = utils.spherical_heading(colony_lon, colony_lat, df["longitude"], df["latitude"])

    # reformat column
    df["step_heading_to_colony"] = df["step_heading_to_colony"].round(1)

    return(df)


# ================================================================================================ #
# DISTANCE TO THE NEST
# ================================================================================================ #
def add_dist_to_nest(df, params):
    
    """    
    Add to the dataframe an additional ``dist_to_nest`` column that gives the orthodromic distance to the estimated nest position in kilometers.
    
    :param df: dataframe with ``longitude`` and ``latitude`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary.
    :type params: dict
    :return: the dataframe with an additional ``dist_to_nest`` column that gives the orthodromic distance to the estimated nest position in kilometers.
    :rtype: pandas.DataFrame
    
    .. note::
        The required fields in the parameters dictionary are ``colony``, ``nesting_speed`` and ``nest_position``.  
    """
    
    # estimate the nest position
    [nest_lon, nest_lat] = estimate_nest_position(df, params)

    # compute distance to nest
    df["dist_to_nest"] = utils.ortho_distance(df["longitude"], df["latitude"], nest_lon, nest_lat)

    # reformat column
    df["dist_to_nest"] = df["dist_to_nest"].round(3)
    
    return(df)


# ================================================================================================ #
# TRIP SEGMENTATION
# ================================================================================================ #
def add_trip(df, params):
    
    """    
    Add to the dataframe an additional ``trip`` column that gives the trip identifier number.
    
    :param df: dataframe with ``datetime``, ``dist_to_nest``, ``step_speed`` and ``step_length`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe with an additional ``trip`` column that gives the trip id number.
    :rtype: pandas.DataFrame
       
    The idea is to segment the full recording of positions in foraging trips by labelling every positions with a trip id. 
    
    .. note::
        The required fields in the parameters dictionary are ``dist_threshold``, ``speed_threshold``, ``trip_min_duration``,
        ``trip_min_length`` and ``trip_min_steps``.    
    """
    
    # get parameters
    dist_threshold = params.get("dist_threshold")
    speed_threshold = params.get("speed_threshold")
    trip_min_duration = params.get("trip_min_duration")
    trip_max_duration = params.get("trip_max_duration")
    trip_min_length = params.get("trip_min_length")
    trip_max_length = params.get("trip_max_length")
    trip_min_steps = params.get("trip_min_steps")
    
    # number of steps
    n_df = len(df)
    
    # init trip id array
    trip_id = np.zeros(n_df, dtype=int)

    # determine when bird is close to nest
    is_nesting = np.where(df["dist_to_nest"] <= dist_threshold, 1, 0)
    
    # determine when nesting state is changing
    changing_state = np.insert(np.diff(is_nesting), 0, 0)

    # compute start indexes of the candidate trips
    candidates_start_idx = np.where(changing_state == -1)[0]
    if is_nesting[0] == 0:
        candidates_start_idx = np.insert(candidates_start_idx, 0, 0)
    
    # total number of candidate trips
    n_candidates = len(candidates_start_idx)
    
    # compute end indexes of the candidate trips
    candidates_end_idx = np.where(changing_state == 1)[0]
    if is_nesting[n_df-1] == 0:
        candidates_end_idx = np.insert(candidates_end_idx, n_candidates-1, n_df-1)

    # determine start and end indexes of valid trips among candidate trips
    if n_candidates > 0:
        
        # init
        valids_start_idx = []
        valids_end_idx = []
        t_end_previous_trip = 0
        k = 0        
        
        # loop over candidate trips
        while k < n_candidates:
                
            # start and end index of the k-th candidate trip
            t_start = max(candidates_start_idx[k], t_end_previous_trip)
            t_end = candidates_end_idx[k]

            # include steps before trip start while speed is high enough 
            # (limited by the end index of the previous trip)
            speed = df.loc[t_start,"step_speed"]
            while speed > speed_threshold:
                if t_start > t_end_previous_trip:
                    t_start = t_start - 1
                    speed = df.loc[t_start,"step_speed"]
                else:
                    speed = -1

            # include steps after trip end while speed is high enough (no limit)
            speed = df.loc[t_end,"step_speed"]
            while speed > speed_threshold:
                if t_end < (n_df-1):
                    t_end = t_end + 1
                    if k+1 < n_candidates:
                        if (t_end > candidates_start_idx[k+1]):
                            t_end = candidates_end_idx[k+1]
                            k = k+1
                    speed = df.loc[t_end, "step_speed"]
                else:
                    speed = -1
            t_end_previous_trip = t_end
            
            # trip is valid iff duration, length and steps are high enough
            trip_duration = (df.loc[t_end, "datetime"] - df.loc[t_start, "datetime"]).total_seconds()
            trip_length = (df.loc[t_start:(t_end+1), "step_length"].sum())
            trip_steps = len(df.loc[t_start:(t_end+1)])
            if (trip_duration > trip_min_duration) and (trip_duration < trip_max_duration) and (trip_length > trip_min_length) and (trip_length < trip_max_length) and (trip_steps > trip_min_steps):
                valids_start_idx.append(t_start)
                valids_end_idx.append(t_end)
                
            # increment candidate trip
            k = k+1
       
        # set trip ids of the valid trips
        n_valids = len(valids_start_idx)
        if n_valids > 0:
            for k in range(1, n_valids+1):
                t_start = valids_start_idx[k-1]
                t_end = valids_end_idx[k-1]
                trip_id[t_start:(t_end+1)] = k
    
    # add trip id to the dataframe        
    df["trip"] = trip_id

    return df


# ================================================================================================ #
# DEPTH
# ================================================================================================ #
def add_depth(df):
    
    """    
    Add to the dataframe an additional ``depth`` column that gives the estimated underwater depth in negative meters.   
    
    :param df: dataframe with a ``pressure`` column in hPa.
    :type df: pandas.DataFrame
    :return: the dataframe with an additional ``depth`` column that gives the estimated underwater depth in negative meters.
    :rtype: pandas.DataFrame
    """
    
    # physical constants
    salt_water_density = constants.salt_water_density
    earth_acceleration = constants.earth_acceleration
    
    # zero offset correction

    # compute depth
    p_atm = df["pressure"].median()
    df["depth"] = 100*(p_atm-df["pressure"])/(salt_water_density*earth_acceleration)
    
    # reformat column
    df["depth"] = df["depth"].round(2)
    
    return(df)


# ================================================================================================ #
# DIVE SEGMENTATION
# ================================================================================================ #
def add_dive(df, params):
    
    """   
    Add to the dataframe an additional ``dive`` column that gives the dive id number.
     
    :param df: dataframe with ``datetime`` and ``depth`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe with an additional ``dive`` column that gives the dive id number.
    :rtype: pandas.DataFrame
       
    The idea is to segment the full recording of pressure in foraging dives by labelling every measure with a dive id.
    
    .. note::
        The required fields in the parameters dictionary are ``diving_depth_threshold`` and ``dive_min_duration``.
    """
    
    # get parameters
    diving_depth_threshold = params.get("diving_depth_threshold")
    dive_min_duration = params.get("dive_min_duration")
    
    # number of steps
    n_df = len(df)
    
    # init dive id array
    dive_id = np.zeros(n_df, dtype=int)

    # determine when bird is flying
    is_flying = np.where(df["depth"] >= diving_depth_threshold, 1, 0)
    
    # determine when diving state is changing
    changing_state = np.insert(np.diff(is_flying), 0, 0)

    # compute start indexes of the candidate dives
    candidates_start_idx = np.where(changing_state == -1)[0]
    if is_flying[0] == 0:
        candidates_start_idx = np.insert(candidates_start_idx, 0, 0)
    
    # total number of candidate dives
    n_candidates = len(candidates_start_idx)
    
    # compute end indexes of the candidate dives
    candidates_end_idx = np.where(changing_state == 1)[0]
    if is_flying[n_df-1] == 0:
        candidates_end_idx = np.insert(candidates_end_idx, n_candidates-1, n_df-1)

    # determine start and end indexes of valid dives among candidate dives
    if n_candidates > 0:
        
        # init
        valids_start_idx = []
        valids_end_idx = []
        t_end_previous_dive = 0
        k = 0        
        
        # loop over candidate dives
        while k < n_candidates:
                
            # start and end index of the k-th candidate dive
            t_start = max(candidates_start_idx[k], t_end_previous_dive)
            t_end = candidates_end_idx[k]
            t_end_previous_dive = t_end
            
            # dive is valid iff duration is high enough
            dive_duration = (df.loc[t_end, "datetime"] - df.loc[t_start, "datetime"]).total_seconds()
            if (dive_duration > dive_min_duration):
                valids_start_idx.append(t_start)
                valids_end_idx.append(t_end)
                
            # increment candidate dive
            k = k+1
       
        # set dive ids of the valid dives
        n_valids = len(valids_start_idx)
        if n_valids > 0:
            for k in range(1, n_valids+1):
                t_start = valids_start_idx[k-1]
                t_end = valids_end_idx[k-1]
                dive_id[t_start:(t_end+1)] = k
    
    # add dive id to the dataframe        
    df["dive"] = dive_id

    return df


# ================================================================================================ #
# FILTER ACCELERATIONS
# ================================================================================================ #
def add_filtered_acc(df, params):
    
    """    
    Add to the dataframe the additional ``ax_f``, ``ay_f`` and ``az_f`` columns of the filtered triaxial accelerations. 
    
    :param df: dataframe with ``step_time``, ``ax``, ``ay`` and ``az`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe with the additional ``ax_f``, ``ay_f`` and ``az_f`` columns of the filtered triaxial accelerations.
    :rtype: pandas.DataFrame
    
    Accelerations can be filtered using :
        - a rolling average of the dynamical acceleration over a given time window. 
        - a Butterworth high-pass filter. 
    
    .. note::
        The required fields in the parameters dictionary are ``filter_type`` and according to this value, either ``acc_time_window`` for rolling average or ``cutoff_f`` and ``order`` for high-pass filtering. 
    """
    
    # get parameters
    filter_type = params.get("filter_type")
    if filter_type == "rolling_avg": 
        time_window = params.get("acc_time_window")
    elif filter_type == "high_pass":
        cutoff = params.get("cutoff_f")
        order = params.get("order")
        
    # estimate sensor resolution
    resolution = df["step_time"].median()
    
    # rolling average filtering 
    if filter_type == "rolling_avg": 
        
        # determine window size in number of steps
        window = int(time_window/resolution)
        
        # compute filtered acceleration as the rolling average over a time window in seconds
        df["ax_f"] = df["ax"] - df["ax"].rolling(window=window, center=True, min_periods=1).mean()
        df["ay_f"] = df["ay"] - df["ay"].rolling(window=window, center=True, min_periods=1).mean()
        df["az_f"] = df["az"] - df["az"].rolling(window=window, center=True, min_periods=1).mean()
        
    # Butterworth high-pass filtering 
    elif filter_type == "high_pass":
        
        # filter parameters 
        fs = 1/resolution
        nyquist = 0.5*fs
        normal_cutoff = cutoff/nyquist
        b, a = butter(order, normal_cutoff, btype="high", analog=False)

        # compute filtered acceleration by applying the filter
        df["ax_f"] = filtfilt(b, a, df["ax"].values)
        df["ay_f"] = filtfilt(b, a, df["ay"].values)
        df["az_f"] = filtfilt(b, a, df["az"].values)
    
    # raise error    
    else:
        raise NotImplementedError("Filter type %s is not implemented." % (filter_type))
        
    # reformat colum
    df["ax_f"] = df["ax_f"].round(3)
    df["ay_f"] = df["ay_f"].round(3)
    df["az_f"] = df["az_f"].round(3) 
    
    return(df)


# ================================================================================================ #
# ODBA
# ================================================================================================ #
def add_odba(df, params): 
        
    """    
    Add to the dataframe the additional ``odba`` and ``odba_f`` columns of the raw and filtered overall dynamical body acceleration.
    
    :param df: dataframe with ``ax``, ``ay``, ``az``, ``ax_f``, ``ay_f`` and ``az_f`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe with the additional ``odba`` and ``odba_f`` columns of the raw and filtered overall dynamical body acceleration.
    :rtype: pandas.DataFrame
    
    .. note::
        The required fields in the parameters dictionary are ``odba_p_norm``.
    """
    
    # get parameters
    p = params.get("odba_p_norm")
    
    # compute odba as the euclidean p-norm of the acceleration vector
    df["odba"] = (abs(df["ax"])**p + abs(df["ay"])**p + abs(df["az"])**p)**(1/p)
    df["odba_f"] = (abs(df["ax_f"])**p + abs(df["ay_f"])**p + abs(df["az_f"])**p)**(1/p)
    
    # reformat colum
    df["odba"] = df["odba"].round(3)
    df["odba_f"] = df["odba_f"].round(3)

    return(df)


# ================================================================================================ #
# TAG SUSPICIOUS ROWS
# ================================================================================================ #
def add_is_suspicious(df, params):
    
    """    
    Add to the dataframe the additional ``is_suspicious`` boolean column tagging suspicious position recordings.
    
    :param df: dataframe with a ``step_speed`` column.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe with the additional ``is_suspicious`` boolean column tagging suspicious position recordings.
    :rtype: pandas.DataFrame
    
    The idea is to make it possible to clean the data of its position recording bugs.
    
    .. note::
        The required fields in the parameters dictionary are ``max_possible_speed``.
            
    .. important::
        Bugs in the position recordings may suggest a dive.
    """
    
    # get parameters
    max_possible_speed = params.get("max_possible_speed")
    
    # tag suspicious rows
    df["is_suspicious"] = (df["step_speed"] > max_possible_speed).astype(int)
    
    return(df)


# # ================================================================================================ #
# # REMOVE SUSPICIOUS ROWS
# # ================================================================================================ #
# def remove_suspicious(df, params):
    
#     """    
#     Remove from the dataframe rows with a step speed above the max possible speed threshold.
    
#     :param df: dataframe with a ``step_speed`` column.
#     :type df: pandas.DataFrame
#     :param params: parameters dictionary. 
#     :type params: dict
#     :return: the dataframe without the rows with a step speed above the max possible speed threshold.
#     :rtype: pandas.DataFrame
    
#     The idea is to clean the data of its recording bugs.
    
#     .. note::
#         The required fields in the parameters dictionary are ``max_possible_speed``.
            
#     .. important::
#         Bugs in the position recordings may suggest a dive.
#     """
    
#     # get parameters
#     max_possible_speed = params.get("max_possible_speed")
    
#     # remove suspicious rows
#     is_suspicious = (df["step_speed"] > max_possible_speed)
#     df = df.loc[~(is_suspicious)].reset_index(drop=True)
    
#     return(df)


# ================================================================================================ #
# POSITION INTERPOLATION
# ================================================================================================ #
def interpolate_lat_lon(df, interp_datetime, add_proxy=False):
            
    """
    Interpolate longitude and latitude at a given datetime.
        
    :param df: dataframe with ``datetime``, ``longitude``and ``latitude`` columns.
    :type df: pandas.DataFrame
    :param interp_datetime: desired datetime for interpolation.
    :type interp_datetime: pandas.DatetimeIndex
    :param add_proxy: add an ``interp_proxy`` column to the resulting dataframe if True.
    :type add_proxy: bool
    :return: a dataframe with ``datetime``, ``longitude`` and ``latitude`` interpolated at the desired datetime.
    :rtype: pandas.DataFrame
    
    Inerpolation is performed using NumPy. The interpolation proxy is computed as the duration in seconds between 
    the desired datetime and the closest mesured position. 
    
    .. warning::
        Computing the interpolation proxy significantly slows down the computation.
    """

    # number of interpolation step
    n_step = len(interp_datetime)

    # init interpolated dataframe
    df_interp = pd.DataFrame({"datetime": interp_datetime, "latitude": [df.loc[0, "latitude"]]*n_step, "longitude": [df.loc[0, "longitude"]]*n_step})

    # interpolate longitude and latitude
    df_interp["latitude"] = np.interp(interp_datetime.values.astype(float), df["datetime"].values.astype(float), df["latitude"].values)
    df_interp["longitude"] = np.interp(interp_datetime.values.astype(float), df["datetime"].values.astype(float), df["longitude"].values)
    
    # reformat column
    df_interp["latitude"] = df_interp["latitude"].round(6)
    df_interp["longitude"] = df_interp["longitude"].round(6)
    
    # compute interpolation proxy
    if add_proxy:
        
        # compute duration between interp and measure
        df_interp["interp_proxy"] = [0.0]*n_step
        for k in range(n_step):
            t = df_interp.loc[k, "datetime"]
            idx = np.searchsorted(df["datetime"], t)
            if (idx == 0):
                t2 = df.loc[idx, "datetime"]
                df_interp.loc[k,"interp_proxy"] = (t2-t).total_seconds()
            elif (idx == len(df)):
                t1 = df.loc[idx-1, "datetime"]
                df_interp.loc[k,"interp_proxy"] = (t-t1).total_seconds()
            else:
                t1 = df.loc[idx-1,"datetime"]
                t2 = df.loc[idx,"datetime"]
                df_interp.loc[k, "interp_proxy"] = min((t-t1).total_seconds(), (t2-t).total_seconds())
    
        # reformat column
        df_interp["interp_proxy"] = df_interp["interp_proxy"].round(1)

    return(df_interp)


# ================================================================================================ #
# BASIC DATA
# ================================================================================================ #
def add_basic_data(df, params):
    
    """
    Enhance the dataframe with the additional basic data.
        
    :param df: dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe enhanced with the additional basic data.
    :rtype: pandas.DataFrame
    """
    
    # check if datetime is ok
    _ = check.check_datetime(df, verbose=True)
    
    # compute basic data
    df = add_step_time(df)
    df = add_is_night(df, params)
    
    return(df)
    
    
# ================================================================================================ #
# GPS DATA
# ================================================================================================ #
def add_gps_data(df, params, clean=True):
        
    """    
    Enhance the dataframe with the additional gps data.
    
    :param df: dataframe with ``datetime``, ``longitude`` and ``latitude`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :param clean: clean gps data if True. 
    :type clean: bool
    :return: the dataframe enhanced with the additional gps data.
    :rtype: pandas.DataFrame
    
    .. warning::
        If clean is True, size of the output dataframe may differ from the input dataframe.
    """
    
    # compute basic data
    df = add_basic_data(df, params)
    
    # step statistics of gps data
    df = add_step_length(df) 
    df = add_step_speed(df) 
    df = add_step_heading(df)
    df = add_step_turning_angle(df)
    df = add_step_heading_to_colony(df, params)
    
    # clean gps data
    df = add_is_suspicious(df, params)
    if clean:        
        df = df.loc[df["is_suspicious"]==0].reset_index(drop=True)
    
    # trip segmentation
    df = add_dist_to_nest(df, params)
    df = add_trip(df, params)
    
    # check if gps data is ok
    _ = check.check_gps(df, verbose=True)
    
    return(df)


# ================================================================================================ #
# TDR DATA
# ================================================================================================ #
def add_tdr_data(df, params):
    
    """    
    Enhance the dataframe with the additional tdr data.
    
    :param df: dataframe with ``datetime``, ``pressure`` and ``temperature`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe enhanced with the additional tdr data.
    :rtype: pandas.DataFrame
    """
    
    # compute basic data
    df = add_basic_data(df, params)
    
    # check if tdr data is ok
    _ = check.check_tdr(df, verbose=True)
    
    # process tdr data
    df = add_depth(df)
    df = add_dive(df, params)
    
    return(df)


# ================================================================================================ #
# AXY DATA
# ================================================================================================ #
def add_axy_data(df, params):
    
    """    
    Enhance the dataframe with the additional axy data.
    
    :param df: dataframe with a ``datetime``, ``ax``, ``ay``, ``az``, ``longitude``, ``latitude``, ``pressure`` and ``temperature`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe enhanced with the additional axy data.
    :rtype: pandas.DataFrame
    """
    
    # compute basic data
    df = add_basic_data(df, params)
    
    # check if acc data is ok
    _ = check.check_acc(df, verbose=True)
    
    # process acceleration data
    df = add_filtered_acc(df, params)
    df = add_odba(df, params)
        
    # extract data at gps resolution and add processed gps data
    gps_resolution = (df["longitude"].notna()) & (df["latitude"].notna())
    gps_indices = df.loc[gps_resolution].index
    df_gps_tmp = df.loc[gps_resolution, ["datetime", "longitude", "latitude"]].reset_index(drop=True)
    df_gps_tmp = add_gps_data(df_gps_tmp, params, clean=False)
    
    # extract data at tdr resolution and add processed tdr data
    tdr_resolution = (df["pressure"].notna()) & (df["temperature"].notna())
    tdr_indices = df.loc[tdr_resolution].index
    df_tdr_tmp = df.loc[tdr_resolution, ["datetime", "pressure", "temperature"]].reset_index(drop=True)
    df_tdr_tmp = add_tdr_data(df_tdr_tmp, params)
    
    # init dataframe full of NaNs and set data type according to dictionary
    gps_columns = ["step_length", "step_speed", "step_turning_angle", "step_heading", "step_heading_to_colony", "is_suspicious", "dist_to_nest", "trip"]
    tdr_columns = ["depth", "dive"]
    data_columns = gps_columns + tdr_columns
    columns_dtypes_dict = parameters.get_columns_dtypes(data_columns)
    for data_column in data_columns:
        df[data_column] = pd.Series([pd.NA]*len(df), dtype=columns_dtypes_dict[data_column])
        
    # # init dataframe full of NaNs and set data type according to dictionary
    # gps_columns = ["step_length", "step_speed", "step_turning_angle", "step_heading", "step_heading_to_colony", "is_suspicious", "dist_to_nest", "trip"]
    # tdr_columns = ["depth", "dive"]
    # data_columns = gps_columns + tdr_columns
    # columns_dtypes_dict = parameters.get_columns_dtypes(data_columns)
    # df_to_add = pd.DataFrame(index=range(len(df)), columns=data_columns).astype(columns_dtypes_dict)
    # df_to_add[:] = pd.NA
    # df = pd.concat([df, df_to_add], axis=1)
    
    # add gps data to the df at gps resolution
    df.loc[gps_indices, gps_columns] = df_gps_tmp[gps_columns].values
    
    # add tdr data to the df at tdr resolution
    df.loc[tdr_indices, tdr_columns] = df_tdr_tmp[tdr_columns].values
    
    # gps_columns = ["step_length", "step_speed", "step_turning_angle", "step_heading", "step_heading_to_colony", "is_suspicious", "dist_to_nest", "trip"]
    # columns_dtypes_dict = parameters.get_columns_dtypes(gps_columns)
    # # df[gps_columns] = np.nan
    # # # init to NaN
    # for gps_column in gps_columns:
    #     df[gps_column] = pd.Series([pd.NA]*len(df), dtype=columns_dtypes_dict[gps_column])
    # # for gps_column in gps_columns:
    # #     df.loc[gps_indices, gps_column] = df_gps_tmp[gps_column].values
    # #     df[gps_column] = df[gps_column].astype(columns_dtypes_dict[gps_column])
    # df.loc[gps_indices, gps_columns] = df_gps_tmp[gps_columns].values
    
    # # add tdr data to the initial df
    # tdr_columns = ["depth", "dive"]
    # # df[tdr_columns] = np.nan
    # columns_dtypes_dict = parameters.get_columns_dtypes(tdr_columns)
    # for tdr_column in tdr_columns:
    #     df[tdr_column] = pd.Series([pd.NA]*len(df), dtype=columns_dtypes_dict[tdr_column])
    # df.loc[tdr_indices, tdr_columns] = df_tdr_tmp[tdr_columns].values
    
    # produce df_gps by processing (sum, mean, max) data between two gps measures
    cols_funcs = {"odba":"sum", "odba_f":"sum", "step_time":"sum",
                  "pressure":"max", "depth":"max", "dive":"max",
                  "temperature":"mean",
                  "dive":"len_unique_pos"}
    df = utils.apply_functions_between_samples(df, gps_resolution, cols_funcs, verbose=True)
    
    # process gps data
    df_gps = df.loc[gps_resolution].reset_index(drop=True)
    df_gps = df_gps.drop(["odba", "odba_f", "step_time", "dive", "pressure", "depth", "temperature"], axis=1)
    df_gps = df_gps.rename(columns={"odba_sum":"odba", "odba_f_sum":"odba_f", "step_time_sum":"step_time", 
                                    "dive_max":"dive", "dive_len_unique_pos":"n_dives",
                                    "pressure_max":"pressure", "depth_max":"depth", "temperature_mean":"temperature"})
    df_gps["trip"] = df_gps["trip"].astype(int)
    df_gps["is_suspicious"] = df_gps["is_suspicious"].astype(int)
        
    # # process tdr data
    # df_tdr = df.loc[tdr_resolution].reset_index(drop=True)
    # df_tdr = df_tdr.drop(["odba", "odba_f", "step_time", "dive", "pressure", "depth", "temperature"], axis=1)
    # df_tdr = df_tdr.rename(columns={"odba_sum":"odba", "odba_f_sum":"odba_f", "step_time_sum":"step_time"}) # longitude latitude ?
    df_tdr = df_tdr_tmp     
    df_tdr["dive"] = df_tdr["dive"].astype(int)

    # rearrange full dataframe
    df = df[np.concatenate((["date", "time", "ax", "ay", "az", "longitude", "latitude", "pressure", "temperature",
                             "datetime", "step_time", "is_night", "ax_f", "ay_f", "az_f", "odba", "odba_f"], gps_columns, tdr_columns))]
        
    return(df, df_gps, df_tdr)


# ================================================================================================ #
# GPS_TDR DATA
# ================================================================================================ #
def add_gps_tdr_data(df, params):
    
    """    
    Enhance the dataframe with the additional gps_tdr data.
    
    :param df: dataframe with a ``datetime``, ``longitude``, ``latitude``, ``pressure`` and ``temperature`` columns.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dataframe enhanced with the additional gps_tdr data.
    :rtype: pandas.DataFrame
    """
    
    # compute basic data
    df = add_basic_data(df, params)
        
    # extract data at gps resolution and add processed gps data
    gps_resolution = (df["longitude"].notna()) & (df["latitude"].notna())
    gps_indices = df.loc[gps_resolution].index
    df_gps_tmp = df.loc[gps_resolution, ["datetime", "longitude", "latitude"]].reset_index(drop=True)
    df_gps_tmp = add_gps_data(df_gps_tmp, params, clean=False)
    
    # extract data at tdr resolution and add processed tdr data
    tdr_resolution = (df["pressure"].notna()) & (df["temperature"].notna())
    tdr_indices = df.loc[tdr_resolution].index
    df_tdr = df.loc[tdr_resolution, ["datetime", "pressure", "temperature"]].reset_index(drop=True)
    df_tdr = add_tdr_data(df_tdr, params)
    
    # init dataframe full of NaNs and set data type according to dictionary
    gps_columns = ["step_length", "step_speed", "step_turning_angle", "step_heading", "step_heading_to_colony", "is_suspicious", "dist_to_nest", "trip"]
    tdr_columns = ["depth", "dive"]
    data_columns = gps_columns + tdr_columns
    columns_dtypes_dict = parameters.get_columns_dtypes(data_columns)
    for data_column in data_columns:
        df[data_column] = pd.Series([pd.NA]*len(df), dtype=columns_dtypes_dict[data_column])
            
    # add gps data to the df at gps resolution
    df.loc[gps_indices, gps_columns] = df_gps_tmp[gps_columns].values
    
    # add tdr data to the df at tdr resolution
    df.loc[tdr_indices, tdr_columns] = df_tdr[tdr_columns].values
        
    # produce df_gps by processing (sum, mean, max) data between two gps measures
    cols_funcs = {"step_time":"sum", "pressure":"max", "depth":"max", 
                  "dive":"max", "temperature":"mean", "dive":"len_unique_pos"}
    df = utils.apply_functions_between_samples(df, gps_resolution, cols_funcs, verbose=True)
    
    # process gps data
    df_gps = df.loc[gps_resolution].reset_index(drop=True)
    df_gps = df_gps.drop(["step_time", "dive", "pressure", "depth", "temperature"], axis=1)
    df_gps = df_gps.rename(columns={"step_time_sum":"step_time", 
                                    "dive_max":"dive", "dive_len_unique_pos":"n_dives",
                                    "pressure_max":"pressure", "depth_max":"depth", "temperature_mean":"temperature"})
    df_gps["trip"] = df_gps["trip"].astype(int)
    df_gps["is_suspicious"] = df_gps["is_suspicious"].astype(int)
        
    # process tdr data
    df_tdr["dive"] = df_tdr["dive"].astype(int)

    # rearrange full dataframe
    df = df[np.concatenate((["date", "time", "longitude", "latitude", "pressure", "temperature",
                             "datetime", "step_time", "is_night"], gps_columns, tdr_columns))]
        
    return(df, df_gps, df_tdr)


# ================================================================================================ #
# BASIC INFOS
# ================================================================================================ #
def compute_basic_infos(df):
     
    """    
    Produce the dictionary of basic infos.
    
    :param df: dataframe enhanced with the additional basic data.
    :type df: pandas.DataFrame
    :return: the dictionary of basic infos.
    :rtype: dict
    """
    
    # compute basic information
    start_datetime = df["datetime"].min()
    end_datetime = df["datetime"].max()
    resolution = df["step_time"].median()
    total_duration = (df["datetime"].max() - df["datetime"].min()).total_seconds()/86400
    n_df = len(df)
    
    # store basic information
    infos = {"start_datetime" : start_datetime,
             "end_datetime" : end_datetime,
             "resolution" : resolution,
             "total_duration" : total_duration,
             "n_df" : n_df}
    
    return(infos)

    
# ================================================================================================ #
# GPS INFOS
# ================================================================================================ #
def compute_gps_infos(df, params):
    
    """    
    Produce the dictionary of gps infos.
    
    :param df: dataframe enhanced with the additional gps data.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dictionary of gps infos.
    :rtype: dict
    """
    
    # compute gps infos
    total_length = df["step_length"].sum()
    dmax = df["dist_to_nest"].max()
    n_trips = df["trip"].max()
    trip_statistics = pd.DataFrame(columns=["id", "length", "duration", "max_hole", "dmax"])
    for k in range(n_trips):
        trip_id = k+1
        df_trip = df.loc[df["trip"] == trip_id].reset_index(drop=True)  
        n_df_trip = len(df_trip)
        trip_statistics.loc[k, "id"] = trip_id
        trip_statistics.loc[k, "length"] = df_trip["step_length"].sum()
        trip_statistics.loc[k, "duration"] = (df_trip.loc[n_df_trip-1, "datetime"] - df_trip.loc[0, "datetime"]).total_seconds()/3600
        trip_statistics.loc[k, "max_hole"] = df_trip["step_time"].max()
        trip_statistics.loc[k, "dmax"] = df_trip["dist_to_nest"].max()
        trip_statistics.loc[k, "n_step"] = n_df_trip
    nest_position = estimate_nest_position(df, params)
    
    # store gps infos
    infos = {"total_length" : total_length,
             "dmax" : dmax,
             "n_trips" : n_trips,
             "nest_position" : nest_position,
             "trip_statistics" : trip_statistics}
    
    return(infos)


# ================================================================================================ #
# TDR INFOS
# ================================================================================================ #
def compute_tdr_infos(df):
    
    """    
    Produce the dictionary of tdr infos.
    
    :param df: dataframe enhanced with the additional tdr data.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dictionary of tdr infos.
    :rtype: dict
    """
    
    # compute tdr infos
    n_dives = df["dive"].max()
    median_pressure = df["pressure"].median()
    median_depth = df["depth"].median()
    max_depth = df["depth"].max()
    mean_temperature = df["temperature"].mean()
    dive_statistics = pd.DataFrame(columns=["id", "duration", "max_depth"])
    for k in range(n_dives):
        dive_id = k+1
        df_dive = df.loc[df["dive"] == dive_id].reset_index(drop=True)
        n_df_dive = len(df_dive)
        dive_statistics.loc[k, "id"] = dive_id
        dive_statistics.loc[k, "duration"] = (df_dive.loc[n_df_dive-1, "datetime"] - df_dive.loc[0, "datetime"]).total_seconds()
        dive_statistics.loc[k, "max_depth"] = df_dive["depth"].max()
            
    # store tdr infos
    infos = {"n_dives" : n_dives,
             "median_pressure" : median_pressure, 
             "median_depth" : median_depth, 
             "max_depth" : max_depth, 
             "mean_temperature" : mean_temperature,
             "dive_statistics" : dive_statistics}
    
    return(infos)
    
    
# ================================================================================================ #
# AXY INFOS
# ================================================================================================ #
def compute_axy_infos(df):
        
    """    
    Produce the dictionary of axy infos.
    
    :param df: dataframe enhanced with the additional axy data.
    :type df: pandas.DataFrame
    :param params: parameters dictionary. 
    :type params: dict
    :return: the dictionary of axy infos.
    :rtype: dict
    """
    
    # compute axy infos
    max_odba = df["odba"].max()
    median_odba = df["odba"].median()
    max_odba_f = df["odba_f"].max()
    median_odba_f = df["odba_f"].median()
            
    # store axy infos
    infos = {"max_odba" : max_odba,
             "median_odba" : median_odba, 
             "max_odba_f" : max_odba_f, 
             "median_odba_f" : median_odba_f}
    
    return(infos)