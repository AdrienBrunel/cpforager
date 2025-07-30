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
# GOAL   : apply a chosen function (e.g. sum, mean, min, max) over every elements between samples 
#          at a given resolution. Note that the output is of same size of the input, though only
#          indices corresponding to subsample resolution have nonzero values.
# INPUT  : - df : XXXX.
#          - resolution : XXXX. 
#          - columns : XXXX. 
#          - func : XXXX. 
#
# OUTPUT : - df : dataframe at resolution
# ================================================================================================ #
def func_between_samples(df, resolution, columns, func=["sum", "mean", "min", "max"], verbose=False):

    # subsample of the initial dataframe
    df_subsamples = df.loc[resolution].reset_index(drop=True)
    n_subsamples = resolution.sum()
    n_df = len(df)
    
    # if subsampling resolution is thicker than sampling resolution
    if n_subsamples < n_df:
        
        # loop over columns to be processed (sum, mean, min or max) between subsamples
        for c in columns:
            new_column = "%s_%s" % (c, func)
            df[new_column] = 0.0*n_df
            
            # loop over subsamples
            for k in range(n_subsamples):
                
                # display progress
                if(verbose & (k % int(n_subsamples/20) == 0)): print("%d/%d - %.1f%%" % (k, n_subsamples, 100*k/n_subsamples))
                
                # computation between samples
                if k == 0:
                    idx_0 = 0 
                    idx_1 = np.searchsorted(df["datetime"], df_subsamples.loc[k, "datetime"], side="right")
                    between_subsamples_points = np.arange(idx_0, idx_1)
                else:       
                    idx_0 = np.searchsorted(df["datetime"], df_subsamples.loc[k-1, "datetime"], side="right")
                    idx_1 = np.searchsorted(df["datetime"], df_subsamples.loc[k, "datetime"], side="right")
                    between_subsamples_points = np.arange(idx_0, idx_1)
                if len(between_subsamples_points) > 0:
                    if func=="sum": df.loc[idx_1-1,new_column] = df.loc[between_subsamples_points,c].sum()
                    if func=="mean": df.loc[idx_1-1,new_column] = df.loc[between_subsamples_points,c].mean()
                    if func=="min": df.loc[idx_1-1,new_column] = df.loc[between_subsamples_points,c].min()
                    if func=="max": df.loc[idx_1-1,new_column] = df.loc[between_subsamples_points,c].max()
                    
    # if subsampling resolution is thiner than sampling resolution
    else:
        for c in columns:
            new_column = "%s_%s" % (c, func)
            df[new_column] = df[c]
            
    return(df)
