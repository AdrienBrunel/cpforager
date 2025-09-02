# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #


# ================================================================================================ #
# CHECK DATETIME TYPE
# ================================================================================================ #
def check_datetime_type(df, verbose=True):
    
    """
    Check if the dataframe ``datetime`` column type is datetime64. 
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe ``datetime`` column type is datetime64.
    :rtype: bool
    """
    
    # init boolean
    check = True
    
    # trigger warning if type is not datetime64
    if(df.dtypes["datetime"] != "datetime64[ns]"):
        check = False
        if verbose: print("WARNING : the \"datetime\" column type is not \"datetime64[ns]\" but rather %s" % (df.dtypes["datetime"]))
    
    return(check)


# ================================================================================================ #
# CHECK IF DATETIME ARE SORTED
# ================================================================================================ #
def check_datetime_order(df, verbose=True):
    
    """
    Check if the dataframe ``datetime`` column is sorted. 
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe ``datetime`` column is sorted. 
    :rtype: bool
    """
    
    # init boolean
    check = True
    
    # trigger warning if there are unsorted values
    if ((df["datetime"].argsort() != df["datetime"].argsort().index).sum()>0):
        check = False
        if verbose: print("WARNING : the \"datetime\" column has %d unsorted rows" % ((df["datetime"].argsort() != df["datetime"].argsort().index).sum()))
    
    return(check)


# ================================================================================================ #
# CHECK IF DATETIME HAS DUPLICATES
# ================================================================================================ #
def check_datetime_duplicates(df, verbose=True):
    
    """
    Check if the dataframe ``datetime`` column does not have duplicates. 
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe ``datetime`` column does not have duplicates. 
    :rtype: bool
    """
    
    # init boolean
    check = True
    
    # trigger warning if there are duplicates
    if (df["datetime"].duplicated(keep=False).sum()>0):
        check = False
        if verbose: print("WARNING : the \"datetime\" column has %d duplicates" % (df["datetime"].duplicated(keep=False).sum()))
        
    return(check)


# ================================================================================================ #
# CHECK IF DATETIME HAS A REALISTIC RANGE
# ================================================================================================ #
def check_datetime_range(df, verbose=True):
    
    """
    Check if the dataframe ``datetime`` column cover a realistic range. 
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe ``datetime`` column cover a realistic range. 
    :rtype: bool
    
    Datetime range is considered realistic if it is bigger than 8 hours and smaller than 30 days.
    """
    
    # init boolean
    check = True
    
    # trigger warning if datetime range is bigger than 12 hours and smaller than 7 days
    if (((df["datetime"].max()-df["datetime"].min()).total_seconds()/(3600*24) < 8/24) | ((df["datetime"].max()-df["datetime"].min()).total_seconds()/(3600*24) > 30)):
        check = False
        if verbose: print("WARNING : the recording covers a time range of %.2f days which may be suspicious" % ((df["datetime"].max()-df["datetime"].min()).total_seconds()/(3600*24)))
        
    return(check)


# ================================================================================================ #
# CHECK IF DATETIME IS OK OVERALL
# ================================================================================================ #
def check_datetime(df, verbose=True):
    
    """
    Check if the dataframe ``datetime`` column is ok overall.
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if datetime is ok overall.
    :rtype: bool
    
    Practically, check if the dataframe ``datetime`` column type is datetime64, is sorted, does not have duplicates and cover a realistic range. 
    """
    
    # check every feature
    check_1 = check_datetime_type(df, verbose)
    check_2 = check_datetime_order(df, verbose)
    check_3 = check_datetime_duplicates(df, verbose)
    check_4 = check_datetime_range(df, verbose)
    
    return(check_1*check_2*check_3*check_4)


# ================================================================================================ #
# CHECK IF DATAFRAME HAS LON/LAT DATA
# ================================================================================================ #
def check_longitude_latitude(df, verbose=True):
    
    """
    Check if ``longitude`` and ``latitude`` columns do not only contain NaN values. 
    
    :param df: the dataframe with ``longitude`` and ``latitude`` columns.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe ``longitude`` and ``latitude`` columns do not only contain NaN values. 
    :rtype: bool
    """
    
    # init boolean
    check = True

    # trigger warning if longitude is full of NaN
    if ((df["longitude"].isna()).sum() == len(df)):
        check = False
        if verbose: print("WARNING : the \"longitude\" column only contains NaN values")

    # trigger warning if latitude is full of NaN
    if ((df["latitude"].isna()).sum() == len(df)):
        check = False
        if verbose: print("WARNING : the \"latitude\" column only contains NaN values")
        
    return(check)


# ================================================================================================ #
# CHECK IF AT LEAST ONE TRIP
# ================================================================================================ #
def check_trip_existence(df, verbose=True):
    
    """
    Check if dataframe contains at least one trip. 
    
    :param df: the dataframe with a ``trip`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if dataframe has at least one trip. 
    :rtype: bool
    """
    
    # init boolean
    check = True

    # trigger warning if only one value among trip ids
    if (len(df["trip"].unique()) <= 1):
        check = False
        if verbose: print("WARNING : no trip found.")
        
    return(check)


# ================================================================================================ #
# CHECK IF DATAFRAME HAS A TRIP RECORDING INTERRUPTED
# ================================================================================================ #
def check_trip_interruption(df, verbose=True):
    
    """
    Check if trip recording is interrupted. 
    
    :param df: the dataframe with a ``trip`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if trip recording is interrupted. 
    :rtype: bool
    """
    
    # init boolean
    check = True

    # trigger warning if last position is not at nest
    if (df["trip"][-1:].values[0] > 0):
        check = False
        if verbose: print("WARNING : last trip recording seems interrupted.")
        
    return(check)


# ================================================================================================ #
# CHECK IF GPS DATA IS OK OVERALL
# ================================================================================================ #
def check_gps(df, verbose=True):
    
    """
    Check if the gps data is ok overall. 
    
    :param df: the dataframe with ``longitude``, ``latitude`` and ``trip`` columns.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if if the gps data is ok overall. 
    :rtype: bool
    
    Practically, check if the dataframe ``longitude`` and ``latitude`` columns do not only contain NaN values, if there is at least one trip and if last trip is not interrupted. 
    """
    
    # check every feature
    check_1 = check_longitude_latitude(df, verbose)
    check_2 = check_trip_existence(df, verbose)
    check_3 = check_trip_interruption(df, verbose)
    
    return(check_1*check_2*check_3)


# ================================================================================================ #
# CHECK IF DATAFRAME HAS PRESSURE/TEMPERATURE DATA
# ================================================================================================ #
def check_pressure_temperature(df, verbose=True):
    
    """
    Check if ``pressure`` and ``temperature`` columns do not only contain NaN values. 
    
    :param df: the dataframe with with ``pressure`` and ``temperature`` columns.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe ``pressure`` and ``temperature`` columns do not only contain NaN values. 
    :rtype: bool
    """
    
    # init boolean
    check = True

    # trigger warning if pressure is full of NaN
    if ((df["pressure"].isna()).sum() == len(df)):
        check = False
        if verbose: print("WARNING : the \"pressure\" column only contains NaN values")

    # trigger warning if temperature is full of NaN
    if ((df["temperature"].isna()).sum() == len(df)):
        check = False
        if verbose: print("WARNING : the \"temperature\" column only contains NaN values")
        
    return(check)


# ================================================================================================ #
# CHECK IF TDR DATA IS OK OVERALL
# ================================================================================================ #
def check_tdr(df, verbose=True):
    
    """
    Check if the tdr data is ok overall. 
    
    :param df: the dataframe with ``pressure`` and ``temperature`` columns.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the tdr data is ok overall. 
    :rtype: bool
    
    Practically, check if the dataframe ``pressure`` and ``temperature`` columns do not only contain NaN values. 
    """
    
    # check every feature
    check_1 = check_pressure_temperature(df, verbose)
    
    return(check_1)


# ================================================================================================ #
# CHECK IF DATAFRAME HAS ACCELERATIONS DATA
# ================================================================================================ #
def check_accelerations(df, verbose=True):
    
    """
    Check if ``ax``, ``ay`` and ``az`` columns do not only contain NaN values. 
    
    :param df: the dataframe with ``ax``, ``ay`` and ``az`` columns.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe ``ax``, ``ay`` and ``az`` columns do not only contain NaN values. 
    :rtype: bool
    """
    
    # init boolean
    check = True

    # trigger warning if ax is full of NaN
    if ((df["ax"].isna()).sum() == len(df)):
        check = False
        if verbose: print("WARNING : the \"ax\" column only contains NaN values")

    # trigger warning if ay is full of NaN
    if ((df["ay"].isna()).sum() == len(df)):
        check = False
        if verbose: print("WARNING : the \"ay\" column only contains NaN values")
        
    # trigger warning if az is full of NaN
    if ((df["az"].isna()).sum() == len(df)):
        check = False
        if verbose: print("WARNING : the \"az\" column only contains NaN values")
        
    return(check)


# ================================================================================================ #
# CHECK IF ACC DATA IS OK OVERALL
# ================================================================================================ #
def check_acc(df, verbose=True):
    
    """
    Check if the acceleration data is ok overall. 
    
    :param df: the dataframe with ``ax``, ``ay`` and ``az`` columns.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the acceleration data is ok overall. 
    :rtype: bool
    
    Practically, check if the dataframe ``ax``, ``ay`` and ``az`` columns do not only contain NaN values. 
    """
    
    # check every feature
    check_1 = check_accelerations(df, verbose)
    
    return(check_1)