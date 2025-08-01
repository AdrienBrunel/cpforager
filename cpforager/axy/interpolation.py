# ======================================================= #
# LIBRARIES
# ======================================================= #
from cpforager import processing


# ======================================================= #
# AXY INTERPOLATION [AXY METHOD]
# ======================================================= #
def interpolate_lat_lon(self, interp_datetime, add_proxy=False):
    
    # get attributes
    df_gps = self.df_gps
    
    # interpolation of GPS data only
    df_interp = processing.interpolate_lat_lon(df_gps[["datetime", "longitude", "latitude"]], interp_datetime, add_proxy)
    
    return(df_interp)