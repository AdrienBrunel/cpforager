# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import math
import numpy as np
import pandas as pd

# ================================================================================================ #
# INPUT  : - lon_1 : longitude in degree of the first position.
#          - lat_1 : latitude in degree of the first position.
#          - lon_2 : longitude in degree of the second position.
#          - lat_2 : latitude in degree of the second position.
#
# OUTPUT : - hav_dist : distance in kilometers following the trigonometric haversine formula.
# ================================================================================================ #
def ortho_distance(lon_1, lat_1, lon_2, lat_2):

    # convert degree to radians
    lat_1 = math.pi/180*lat_1
    lat_2 = math.pi/180*lat_2
    lon_1 = math.pi/180*lon_1
    lon_2 = math.pi/180*lon_2

    # compute earth radius at mean latitude
    r_earth_equ = 6378.137
    r_earth_pol = 6356.752
    lat_mean = (lat_1 + lat_2)/2
    r_earth = np.sqrt(((r_earth_equ**2 * np.cos(lat_mean))**2 + (r_earth_pol**2 * np.sin(lat_mean))**2) / ((r_earth_equ * np.cos(lat_mean))**2 + (r_earth_pol * np.sin(lat_mean))**2))

    # longitude and latitude differences
    dlat = lat_2 - lat_1
    dlon = lon_2 - lon_1

    # compute great-circle distance using haversine formula
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(lat_1) * np.cos(lat_2) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    hav_dist = r_earth * c

    return(hav_dist)


# ================================================================================================ #
# INPUT  : - lon_1 : longitude in degree of the first position.
#          - lat_1 : latitude in degree of the first position.
#          - lon_2 : longitude in degree of the second position.
#          - lat_2 : latitude in degree of the second position.
#
# OUTPUT : - heading_deg : spherical heading in degrees between the north and the direction formed 
#                          by the two positions.
# ================================================================================================ #
def spherical_heading(lon_1, lat_1, lon_2, lat_2):

    # convert degree to radians
    lat_1 = math.pi/180*lat_1
    lat_2 = math.pi/180*lat_2
    lon_1 = math.pi/180*lon_1
    lon_2 = math.pi/180*lon_2

    # difference of longitude
    dlon = lon_2 - lon_1

    # compute heading
    a = np.cos(lat_1) * np.sin(lat_2) - np.sin(lat_1) * np.cos(lat_2) * np.cos(dlon)
    b = np.sin(dlon) * np.cos(lat_2)
    heading_rad = np.arctan2(b, a) % (2 * math.pi)

    # convert back to degrees
    heading_deg = 180/math.pi*heading_rad

    return(heading_deg)


# ================================================================================================ #
# INPUT  : - df : dataframe with a "datetime" column at utc timezone.
#          - local_timezone : local timezone as a string according to pytz nomenclature.
#
# OUTPUT : - df : dataframe with a "datetime" column at local timezone.
# ================================================================================================ #
def convert_utc_to_loc(df, local_timezone):
    
    # convert utc datetime to local time
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.tz_localize("UTC").dt.tz_convert(local_timezone)
    
    # remove timezone info in datetime64 type to limit interference with other functions (e.g. pyplot)
    df["datetime"] = df["datetime"].dt.tz_localize(None)
    
    return(df)

    
# ================================================================================================ #
# INPUT  : - df : dataframe with a "datetime" column at local_timezone.
#          - local_timezone : local timezone as a string according to pytz nomenclature.
#
# OUTPUT : - df : dataframe with a "datetime" column at utc timezone.
# ================================================================================================ #
def convert_loc_to_utc(df, local_timezone):
    
    # convert local datetime to utc
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.tz_localize(local_timezone).dt.tz_convert("UTC")
    
    # remove timezone info in datetime64 type to limit interference with other functions (e.g. pyplot)
    df["datetime"] = df["datetime"].dt.tz_localize(None)
    
    return(df)
    
    
# ================================================================================================ #
# INPUT  : - XXXX
#
# OUTPUT : - XXXX
# ================================================================================================ #
def interpolate_lonlat(df, interp_freq, verbose=False):
    
    # vector of desired interpolation
    interp_datetime = pd.date_range(start=df["datetime"].iloc[0], end=df["datetime"].iloc[-1], freq=pd.Timedelta(seconds=interp_freq), periods=None)
    n_step = len(interp_datetime)
    
    # build interpolation dataframe 
    df_interp = pd.DataFrame(columns=["datetime", "longitude", "latitude", "interp_proxy"])
    df_interp["datetime"] = interp_datetime
    df_interp["latitude"] = np.interp(interp_datetime.values.astype(float), df["datetime"].values.astype(float), df["latitude"].values).round(6)
    df_interp["longitude"] = np.interp(interp_datetime.values.astype(float), df["datetime"].values.astype(float), df["longitude"].values).round(6)
    df_interp["interp_proxy"] = [0.0]*n_step
    for k in range(n_step):
        
        # display progress
        if (k % 25 == 0) & (k>0) & (verbose):
            print(f"lon/lat : %.1f%%" % (100*k/n_step))
        
        # find gps lat/lon before and after interpolation datetime
        t = df_interp.loc[k, "datetime"]
        idx = np.searchsorted(df["datetime"], t)
        if (idx == 0):
            t2 = df.loc[idx, "datetime"]
            df_interp.loc[k,"interp_proxy"] = (t2 - t).total_seconds()
        elif (idx == len(df)):
            t1 = df.loc[idx-1, "datetime"]
            df_interp.loc[k,"interp_proxy"] = (t - t1).total_seconds()
        else:
            t1 = df.loc[idx-1,"datetime"]
            t2 = df.loc[idx,"datetime"]
            df_interp.loc[k, "interp_proxy"] = min((t - t1).total_seconds(), (t2 - t).total_seconds())
        
    # reformat column
    df_interp["latitude"] = df_interp["latitude"].round(6)
    df_interp["longitude"] = df_interp["longitude"].round(6)
    df_interp["interp_proxy"] = df_interp["interp_proxy"].round(1)
    
    return(df_interp)

