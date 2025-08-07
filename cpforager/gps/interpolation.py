# ======================================================= #
# LIBRARIES
# ======================================================= #
from cpforager import processing


# ======================================================= #
# GPS INTERPOLATION [GPS METHOD]
# ======================================================= #
def interpolate_lat_lon(self, interp_datetime, add_proxy=False):
    
    """
    Interpolate longitude and latitude at a given datetime.
        
    :param self: a GPS object
    :type self: cpforager.GPS
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
    
    # get attributes
    df = self.df
    
    # interpolation of GPS data only
    df_interp = processing.interpolate_lat_lon(df[["datetime", "longitude", "latitude"]], interp_datetime, add_proxy)

    return(df_interp)