# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import math
import numpy as np
import pandas as pd
import pulp as plp


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
# COMPUTE OPTIMAL LAYOUT (NB OF COLUMNS AND ROWS)
# ================================================================================================ #
# def rows_columns_computation(n_plots):
    
#     # decision variables
#     n_columns = plp.LpVariable("n_columns", lowBound=1, cat=plp.LpInteger)
#     n_rows = plp.LpVariable("n_rows", lowBound=1, cat=plp.LpInteger)
#     # z = plp.LpVariable("z", lowBound=n_plots, cat=plp.LpInteger)

#     # model
#     model = plp.LpProblem("plot_auto_layout", plp.LpMinimize)

#     # objective function
#     model.setObjective(n_rows-n_columns)
#     # model.setObjective(n_rows-n_columns+z)

#     # constraints
#     model += plp.LpConstraint(e=n_rows-n_columns, sense=plp.LpConstraintGE, name='square_shape', rhs=0)
#     model += plp.LpConstraint(e=n_rows*n_columns, sense=plp.LpConstraintGE, name='sufficient_nb_panels', rhs=n_plots)
#     # model += plp.LpConstraint(e=z, sense=plp.LpConstraintGE, name='sufficient_nb_panels', rhs=n_plots)
    
#     # solve
#     model.solve()
#     print(int(n_columns.value()), int(n_rows.value()), int(z.value()))
    
#     return(n_rows, n_columns)

# def get_divisors(n):

#     # compute divisors of n_plots
#     divisors = []
    
#     # compute divisors
#     for i in np.flip(np.arange(1,int(math.sqrt(n)))):
#         if n % i == 0: divisors.append(i)
        
#     return(divisors)
    
# def near_square_layout(n_plots):
    
#     # compute divisors of n_plots
#     divisors = get_divisors(n_plots)
#     n_divisors = len(divisors)
        
#     for k in np.flip(np.arange(math.ceil(math.sqrt(n_plots))**2,n_plots)):
#         a = get_divisors(k)
#         b = k/a
        
#     m = math.ceil(math.sqrt(n_plots))**2
    
#     # init dataframe of possibles values for (n_rows, n_columns) combinations
#     df_possible_layout = pd.DataFrame(np.zeros((n_divisors, 2), dtype=int), columns=["n_rows", "n_columns"])
    
#     # loop over divisors
#     for k in range(n_divisors):
#         df_possible_layout.loc[k, "n_rows"] = divisors[k]
#         df_possible_layout.loc[k, "n_columns"] = n_plots/divisors[k]
        
#     # compute squareness index
#     df_possible_layout["squareness"] = df_possible_layout["n_rows"]-df_possible_layout["n_columns"]
    
#     # remove case when n_rows < n_columns
#     df_possible_layout = df_possible_layout.loc[df_possible_layout["squareness"] >= 0].reset_index(drop=True)
    
#     # get smallest n_rows - n_columns
#     n_rows, n_columns = df_possible_layout.iloc[df_possible_layout["squareness"].argmin()][["n_rows", "n_columns"]].values
    
#     return(n_rows, n_columns)
    
    
