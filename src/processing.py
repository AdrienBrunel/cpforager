import numpy as np
import pandas as pd
from src import utils
from suntime import Sun
import pytz
    

# ================================================================================================ #
# GOAL   : estimate the nest position inside the colony from longitude and latitude data.
#
# INPUT  : - df            : dataframe with "longitude" and "latitude" columns.
#          - params        : structure of parameters with "colony" giving the bounding box of the 
#                            colony, "nesting_speed" giving the speed below which we consider the 
#                            bird at nest. 
#          - nest_position : nest position if known beforehand. 
#          - verbose       : if True print all information to the terminal. 
#
# OUTPUT : - nest : estimated longitude and latitude of the nest.
# ================================================================================================ #
def estimate_nest_position(df, params, nest_position=None, verbose=False):
    
    # get parameters
    colony = params.get("colony")
    nesting_speed = params.get("nesting_speed")
    
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
# GOAL   : compute the duration in seconds between every measure of position.
#
# INPUT  : - df : dataframe with a "datetime" column.
#
# OUTPUT : - df : dataframe with an additional column "step_time" that gives the step time in
#                 seconds.
# ================================================================================================ #
def add_step_time(df):
    
    # compute step time in seconds
    df["step_time"] = (df["datetime"] - df["datetime"].shift(1)).dt.total_seconds()

    # reformat column
    df["step_time"] = df["step_time"].round(1)

    return(df)


# ================================================================================================ #
# GOAL   : compute the length in kilometers between every measure of position.
#
# INPUT  : - df : dataframe with "longitude" and "latitude" columns.
#
# OUTPUT : - df : dataframe with an additional column "step_length" that gives the step length in 
#                 kilometers.
# ================================================================================================ #
def add_step_length(df):
    
    # compute step distance in km
    df["step_length"]  = utils.ortho_distance(df["longitude"].shift(1), df["latitude"].shift(1), df["longitude"], df["latitude"])

    # reformat column
    df["step_length"] = df["step_length"].round(3)

    return(df)


# ================================================================================================ #
# GOAL   : compute the length in kilometers between every measure of position.
#
# INPUT  : - df : dataframe with "longitude" and "latitude" columns.
#
# OUTPUT : - df : dataframe with an additional column "step_length" that gives the step length in 
#                 kilometers.
# ================================================================================================ #
def add_step_speed(df):

    # compute step distance in km
    dist_in_km = df["step_length"]
    
    # compute step time in hour
    dt_in_hours = df["step_time"]/3600

    # compute step speed in km/h
    df["step_speed"]  = dist_in_km / dt_in_hours

    # reformat column
    df["step_speed"] = df["step_speed"].round(3)

    return(df)


# ================================================================================================ #
# GOAL   : compute the heading in degrees between the north and the direction formed by two
#          successive positions. (N=0°, E=90°, S=180°, W=270°).
# 
# INPUT  : - df : dataframe with "longitude" and "latitude" columns.
#
# OUTPUT : - df : dataframe with an additional column "step_heading" that gives heading in degrees. 
# ================================================================================================ #
def add_step_heading(df):
    
    # compute step heading
    df["step_heading"] = utils.spherical_heading(df["longitude"].shift(1), df["latitude"].shift(1), df["longitude"], df["latitude"])

    # reformat column
    df["step_heading"] = df["step_heading"].round(1)

    return(df)


# ================================================================================================ #
# GOAL   : compute the turning angle in degrees between every measure of position.
# 
# INPUT  : - df : dataframe with "longitude" and "latitude" columns.
#
# OUTPUT : - df : dataframe with an additional column "step_turning_angle" that gives the step
#                 turning angle in degrees (between -180 and +180). 
# ================================================================================================ #
def add_step_turning_angle(df):
    
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
# GOAL   : compute the heading in degrees between the colony and the position of the animal.
# 
# INPUT  : - df : dataframe with "longitude" and "latitude" columns.
#          - params : structure of parameters with "colony" giving the bounding box of the colony, 
#                     "nesting_speed" giving the speed below which we consider the bird at nest. 
#
# OUTPUT : - df : dataframe with an additional column "step_heading_to_colony" that gives heading 
#                 of bird related to the colony in degrees. 
# ================================================================================================ #
def add_step_heading_to_colony(df, params):
    
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
# GOAL   : compute the distance to the estimated nest position from longitude and latitude data.
#
# INPUT  : - df     : dataframe with "longitude" and "latitude" columns.
#          - params : structure of parameters with "colony" giving the bounding box of the colony, 
#                     "nesting_speed" giving the speed below which we consider the bird at nest.
#
# OUTPUT : - df : dataframe with an additional "dist_to_nest" column that gives the distance to the
#                 estimated nest position.
# ================================================================================================ #
def add_dist_to_nest(df, params):
    
    # estimate the nest position
    [nest_lon, nest_lat] = estimate_nest_position(df, params)

    # compute distance to nest
    df["dist_to_nest"] = utils.ortho_distance(df["longitude"], df["latitude"], nest_lon, nest_lat)

    # reformat column
    df["dist_to_nest"] = df["dist_to_nest"].round(3)
    
    return(df)


# ================================================================================================ #
# GOAL   : segment the full recording of positions in foraging trips by labelling every positions 
# 	   with a trip id.
#
# INPUT  : - df     : dataframe with "dist_to_nest", "step_speed", "datetime" and "step_length" 
# 		              columns.
#          - params : structure of parameters with "dist_threshold" giving the distance to the nest 
#                     from which we consider a trip may start, "speed_threshold" giving the speed
#                     above which the trip is still ongoing, "trip_min_duration" giving the trip 
#                     duration below which we do not consider it to be a trip, "trip_min_length" 
#                     giving the trip length below which we do not consider it to be a trip,  
#                     "trip_min_steps" giving the trip number of position below which we do not 
#                     consider it to be a trip.
# 
# OUTPUT : - df : dataframe with an additional column "trip" that gives the trip number. 
# ================================================================================================ #
def add_trip(df, params):
    
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
# GOAL   : compute the boolean value informing if it is night at a given position and time.
#
# INPUT  : - df     : dataframe with a "datetime" column.
#          - params : structure of parameters with "colony".
#
# OUTPUT : - df : dataframe with an additional "is_night" column that is 1 if it is night, 
#                 0 otherwise.
# ================================================================================================ #
def add_is_night(df, params):

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
# GOAL   : clean gps data.
#
# INPUT  : - df     : dataframe with a "step_speed" column.
#          - params : structure of parameters.
#
# OUTPUT : - df : dataframe with a "is_suspicious" additional column.
# ================================================================================================ #
def remove_suspicious(df, params):
    
    # get parameters
    max_possible_speed = params.get("max_possible_speed")
    
    # remove suspicious rows
    is_suspicious = (df["step_speed"] > max_possible_speed)
    df = df.loc[~(is_suspicious)].reset_index(drop=True)
    
    return(df)


# ================================================================================================ #
# GOAL   : interpolate longitude and latitude at a desired datetime.
#
# INPUT  : - df              : dataframe with "datetime", "longitude" and "latitude" columns.
#          - interp_datetime : array of the desired datetime for interpolation. 
#          - add_proxy       : boolean True if we want to compute the interpolation proxy computed 
#                              as the duration in seconds between the interp_datetime and the closest
#                              GPS measure.
#
# OUTPUT : - df_interp : dataframe with longitude and latitude interpolated at interp_datetime.
# ================================================================================================ #
def interpolate_lat_lon(df, interp_datetime, add_proxy=False):

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
# GOAL   : add the gps data.
#
# INPUT  : - df     : dataframe with "datetime", "longitude" and "latitude" columns.
#          - params : structure of parameters.
#
# OUTPUT : - df : dataframe with many additional columns.
# ================================================================================================ #
def add_gps_data(df, params):
    
    
    # step statistics of gps data
    df = add_step_time(df)
    df = add_step_length(df) 
    df = add_step_speed(df) 
    df = add_step_heading(df)
    df = add_step_turning_angle(df)
    df = add_step_heading_to_colony(df, params)
    
    # clean data
    df = remove_suspicious(df, params)
        
    # trip segmenation
    df = add_is_night(df, params)
    df = add_dist_to_nest(df, params)
    df = add_trip(df, params)
    
    return(df)


# ================================================================================================ #
# GOAL   : build the infos structure of the gps data.
#
# INPUT  : - df     : dataframe with all the processed columns.
#          - params : structure of parameters.
#
# OUTPUT : - infos : data structure with information about the gps data.
# ================================================================================================ #
def compute_gps_infos(df, params):
    
    # compute basic information
    start_datetime = df["datetime"].min()
    end_datetime = df["datetime"].max()
    resolution = df["step_time"].median()
    total_duration = (df["datetime"].max() - df["datetime"].min()).total_seconds()/86400
    n_df = len(df)
    
    # store basic information
    basic_infos = {"start_datetime" : start_datetime,
                   "end_datetime" : end_datetime,
                   "resolution" : resolution,
                   "total_duration" : total_duration,
                   "n_df" : n_df}
        
    # compute gps infos
    total_length = df["step_length"].sum()
    dmax = df["dist_to_nest"].max()
    n_trip = len(df["trip"].unique())-1
    trip_statistics = pd.DataFrame(columns=["id", "length", "duration", "max_hole", "dmax"])
    for k in range(n_trip):
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
    gps_infos = {"total_length" : total_length,
                 "dmax" : dmax,
                 "n_trip" : n_trip,
                 "nest_position" : nest_position,
                 "trip_statistics" : trip_statistics}
    
    # append dictionaries
    infos = {}
    infos.update(basic_infos)
    infos.update(gps_infos)
    
    return(infos)

