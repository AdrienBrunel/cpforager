# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import pandas as pd


# ================================================================================================ #
# CHECK DATETIME TYPE
# ================================================================================================ #
def check_type(df=pd.DataFrame, verbose=True):
    
    """
    Check if the dataframe column ``datetime`` type is datetime64. 
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe column ``datetime`` type is datetime64.
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
def check_order(df=pd.DataFrame, verbose=True):
    
    """
    Check if the dataframe column ``datetime`` is sorted. 
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe column ``datetime`` is sorted. 
    :rtype: bool
    """
    
    # init boolean
    check = True
    
    # trigger warning if there are unsorted values
    if ((df["datetime"].argsort() != df["datetime"].argsort().index).sum()>0):
        check = False
        if verbose: print("WARNING  : the \"datetime\" column has %d unsorted rows" % ((df["datetime"].argsort() != df["datetime"].argsort().index).sum()))
    
    return(check)


# ================================================================================================ #
# CHECK IF DATETIME HAS DUPLICATES
# ================================================================================================ #
def check_duplicates(df=pd.DataFrame, verbose=True):
    
    """
    Check if the dataframe column ``datetime`` does not have duplicates. 
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe column ``datetime`` does not have duplicates. 
    :rtype: bool
    """
    
    # init boolean
    check = True
    
    # trigger warning if there are duplicates
    if (df["datetime"].duplicated(keep=False).sum()>0):
        check = False
        if verbose: print("WARNING  : the \"datetime\" column has %d duplicates" % (df["datetime"].duplicated(keep=False).sum()))
        
    return(check)


# ================================================================================================ #
# CHECK IF DATETIME IS OK OVERALL
# ================================================================================================ #
def check_full(df=pd.DataFrame, verbose=True):
    
    """
    Check if the dataframe column ``datetime`` type is datetime64, is sorted and does not have duplicates. 
    
    :param df: the dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param verbose: display warning if True.
    :type verbose: bool
    :return: True if the dataframe column ``datetime`` type is datetime64, is sorted and does not have duplicates. 
    :rtype: bool
    """
    
    # init booleans
    check_1 = check_type(df, verbose)
    check_2 = check_order(df, verbose)
    check_3 = check_duplicates(df, verbose)
    
    return(check_1*check_2*check_3)