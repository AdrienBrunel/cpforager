# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import math
import numpy as np
import pandas as pd


# ================================================================================================ #
# ORTHODROMIC DISTANCE
# ================================================================================================ #
def ortho_distance(lon_1, lat_1, lon_2, lat_2):
    
    """
    Compute the orthodromic distance in kilometers between (lon_1, lat_1) and (lon_2, lat_2). 
    
    :param lon_1: longitude in degrees of the first position.
    :type lon_1: float
    :param lat_1: latitude in degrees of the first position.
    :type lat_1: float
    :param lon_2: longitude in degrees of the second position.
    :type lon_2: float
    :param lat_2: latitude in degrees of the second position.
    :type lat_2: float
    :return: the distance in kilometers between (lon_1, lat_1) and (lon_2, lat_2).
    :rtype: float
    
    Orthodromic distance is computed using the trigonometric haversine formula.
    """

    # convert degrees to radians
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
# SPHERICAL HEADING
# ================================================================================================ #
def spherical_heading(lon_1, lat_1, lon_2, lat_2):

    """
    Compute the spherical heading in degrees between the north and the direction formed by the two positions (lon_1, lat_1) and (lon_2, lat_2).
    
    :param lon_1: longitude in degrees of the first position.
    :type lon_1: float
    :param lat_1: latitude in degrees of the first position.
    :type lat_1: float
    :param lon_2: longitude in degrees of the second position.
    :type lon_2: float
    :param lat_2: latitude in degrees of the second position.
    :type lat_2: float
    :return: the spherical heading in degrees between the north and the direction formed by the two positions (lon_1, lat_1) and (lon_2, lat_2).
    :rtype: float
    """
    
    # convert degrees to radians
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

    # convert radians to degrees
    heading_deg = 180/math.pi*heading_rad

    return(heading_deg)


# ================================================================================================ #
# UTC TO LOC
# ================================================================================================ #
def convert_utc_to_loc(df, local_timezone):
    
    """
    Convert ``datetime`` from UTC to the local timezone.
    
    :param df: dataframe with a ``datetime`` column at the UTC timezone.
    :type df: pandas.DataFrame
    :param local_timezone: local timezone following the pytz nomenclature (see ``pytz.all_timezones``).
    :type local_timezone: str
    :return: the dataframe with a ``datetime`` column converted the local timezone.
    :rtype: pandas.DataFrame
    """
    
    # convert utc datetime to local time
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.tz_localize("UTC").dt.tz_convert(local_timezone)
    
    # remove timezone info in datetime64 type to limit interference with other functions (e.g. pyplot)
    df["datetime"] = df["datetime"].dt.tz_localize(None)
    
    return(df)

    
# ================================================================================================ #
# LOC TO UTC
# ================================================================================================ #
def convert_loc_to_utc(df, local_timezone):
    
    """
    Convert ``datetime`` column from the local timezone to UTC.
    
    :param df: dataframe with a ``datetime`` column at the local timezone.
    :type df: pandas.DataFrame
    :param local_timezone: local timezone following the pytz nomenclature (see ``pytz.all_timezones``).
    :type local_timezone: str
    :return: the dataframe with a ``datetime`` column to UTC timezone.
    :rtype: pandas.DataFrame
    """
    
    # convert local datetime to utc
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.tz_localize(local_timezone).dt.tz_convert("UTC")
    
    # remove timezone info in datetime64 type to limit interference with other functions (e.g. pyplot)
    df["datetime"] = df["datetime"].dt.tz_localize(None)
    
    return(df)
    

# ================================================================================================ #
# APPLY FUNCTION BETWEEN SAMPLES
# ================================================================================================ #
def apply_functions_between_samples(df, resolution, columns_functions, verbose=False):
    
    """
    Apply a chosen function (*e.g.* sum, mean, min, max) over every high resolution elements between two subsamples defined by a given resolution.
    
    :param df: dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param resolution: boolean dataframe of the subsampling resolution.
    :type resolution: pandas.DataFrame(dtype=bool)
    :param columns_functions: dictionary giving for each specified column the function to apply.
    :type columns_functions: dict
    :param verbose: display progress if True.
    :type verbose: bool
    :return: the dataframe with the additional columns "column_function" composed of NaN values everywhere except at the subsampling resolution where the function was applied to every elements between two subsamples.
    :rtype: pandas.DataFrame
    
    This function is key to handle data with different resolutions, such as high-resolution acceleration measures and low-resolution position and 
    pressure measures. It thus allows to produce a low-resolution version of the high-resolution data by summarising it using a function between 
    subsamples. Find below the exhaustive table of possible functions to apply.
    
    .. important::
        Output dataframe is of same size as the input dataframe, though only indices corresponding to the subsampling resolution have non-NaN values.
    
    .. csv-table::  
        :header: "function", "description"
        :widths: auto

        ``sum``, "compute the sum of every elements bewteen two subsamples"
        ``mean``, "compute the mean of every elements bewteen two subsamples"
        ``min``, "keep the minimum value of every elements bewteen two subsamples"
        ``max``, "keep the maximum value of every elements bewteen two subsamples"
        ``len_unique_pos``, "compute the number of different positive values of every elements bewteen two subsamples"
    """
    
    # set of possible values for funcs
    funcs_possible_values = ["sum", "mean", "min", "max", "len_unique_pos"]
        
    # set subsampled dataframe at subsampling resolution
    df_subsamples = df.loc[resolution].reset_index(drop=True)
    n_subsamples = resolution.sum()
    n_df = len(df)
    
    # if subsampling resolution is thicker than sampling resolution
    if n_subsamples < n_df:
        
        # initialize new columns in df
        for c, f in columns_functions.items():
            new_column = "%s_%s" % (c, f)
            df[new_column] = np.nan*n_df
            
        # loop over subsamples
        for k in range(n_subsamples):
            
            # display progress
            if(verbose & (k % int(n_subsamples/20) == 0)): print("%d/%d - %.1f%%" % (k, n_subsamples, 100*k/n_subsamples))
            
            # find points between samples
            if k == 0:
                idx_0 = 0 
                idx_1 = np.searchsorted(df["datetime"], df_subsamples.loc[k, "datetime"], side="right")
                between_subsamples_points = np.arange(idx_0, idx_1)
            else:       
                idx_0 = np.searchsorted(df["datetime"], df_subsamples.loc[k-1, "datetime"], side="right")
                idx_1 = np.searchsorted(df["datetime"], df_subsamples.loc[k, "datetime"], side="right")
                between_subsamples_points = np.arange(idx_0, idx_1)
            
            # loop over columns to be processed (sum, mean, min or max) between samples
            if len(between_subsamples_points) > 0:
                for c, f in columns_functions.items():
                    new_column = "%s_%s" % (c, f)
                    if f=="sum": df.loc[idx_1-1,new_column] = df.loc[between_subsamples_points,c].sum()
                    elif f=="mean": df.loc[idx_1-1,new_column] = df.loc[between_subsamples_points,c].mean()
                    elif f=="min": df.loc[idx_1-1,new_column] = df.loc[between_subsamples_points,c].min()
                    elif f=="max": df.loc[idx_1-1,new_column] = df.loc[between_subsamples_points,c].max()
                    elif f=="len_unique_pos": df.loc[idx_1-1,new_column] = (df.loc[between_subsamples_points,c].unique()>0).sum()
                    else: print("WARNING : \"%s\" cannot be found within the array of possible values, i.e. %s" %(f, funcs_possible_values))
                    
    # if subsampling resolution is thiner than sampling resolution
    else:
        for c, f in columns_functions.items():
            new_column = "%s_%s" % (c, f)
            df[new_column] = df[c]
            
    return(df)


# ================================================================================================ #
# NEAR-SQUARE GRID LAYOUT
# ================================================================================================ #
# https://stackoverflow.com/questions/32017327/calculate-the-optimal-grid-layout-dimensions-for-a-given-amount-of-plots-in-r
def get_largest_factor(n):
    """
    Compute the largest factor of an integer. 
    
    :param n: integer we want the largest factor.
    :type n: int
    :return: the largest factor.
    :rtype: int
            
    .. note::
        n>0.
    """
    
    k = math.floor(math.sqrt(n))
    while(n % k != 0):
        k = k-1
    return(k)

def nearsq_grid_layout(n, tol=5/3+0.001):
    
    """
    Compute the near-square grid layout dimensions with a width-to-height ratio being smaller than a given tolerance.
    
    :param n: integer we want the near-square dimensions.
    :type n: int
    :param tol: tolerance.
    :type tol: float
    :return: the dimensions (a,b) such that n = a x b and a/b<tol.
    :rtype: tuple(int, int)
            
    .. note::
        n>0 and tol>1.
    """
    
    m = math.ceil(math.sqrt(n)) ** 2
    for i in range(n, m + 1):
        a = get_largest_factor(i)
        b = int(i/a)
        if b/a < tol:
            return (a, b)