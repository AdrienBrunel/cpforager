# ======================================================= #
# LIBRARIES
# ======================================================= #
from cpforager import processing


# ======================================================= #
# GPS INTERPOLATION [GPS METHOD]
# ======================================================= #
def interpolate_lat_lon(self, interp_datetime, add_proxy=False):
    
    # get attributes
    df = self.df
    
    # interpolation of GPS data only
    df_interp = processing.interpolate_lat_lon(df[["datetime", "longitude", "latitude"]], interp_datetime, add_proxy)

    return(df_interp)