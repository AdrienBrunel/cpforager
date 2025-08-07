# ======================================================= #
# LIBRARIES
# ======================================================= #
from cpforager import utils


# ======================================================= #
# DISPLAY [AXY METHODS]
# ======================================================= #
def display_data_summary(self):
                
    """    
    Print in terminal the AXY data summary.
    
    :param self: a AXY object
    :type self: cpforager.AXY
    """
    
    # compute distance between first position and the estimated nest position    
    pos0 = [self.df_gps.loc[0,"longitude"], self.df_gps.loc[0,"latitude"]]
    nest = self.nest_position
    d_pos0_nest = utils.ortho_distance(nest[0], nest[1], pos0[0], pos0[1])

    # print information
    print("# ============================== SUMMARY ============================== #")
    print("# ------------------------------ METADATA ----------------------------- #")
    print("# + Group = %s" % self.group)
    print("# + Id    = %s" % self.id)
    print("# ------------------------------ ACC DATA ----------------------------- #")
    print("# + Nb of measures            = %d" % self.n_df)
    print("# + Date range                = %s | %s" % (self.start_datetime, self.end_datetime))     
    print("# + Frequency                 = %.1f Hz" % self.frequency)
    print("# + Median (ax, ay, az)       = (%.3f, %.3f, %.3f)" % (self.df["ax"].median(), self.df["ay"].median(), self.df["az"].median()))
    print("# + Median (ax_f, ay_f, az_f) = (%.3f, %.3f, %.3f)" % (self.df["ax_f"].median(), self.df["ay_f"].median(), self.df["az_f"].median()))
    print("# + Median odba               = %.3f" % self.median_odba)
    print("# + Median odba_f             = %.3f" % self.median_odba_f)
    print("# ------------------------------ GPS DATA ----------------------------- #")
    print("# + Nb of measures       = %d" % self.n_df_gps)  
    print("# + Nb of trips          = %d" % self.n_trip) 
    print("# + Time resolution      = %.1f s" % self.gps_resolution)
    print("# + Total duration       = %.2f days" % self.total_duration)
    print("# + Total length         = %.1f km" % self.total_length)
    print("# + Max distance to nest = %.1f km" % self.dmax)
    if self.n_trip>0:
        print("# ------------------------------ TRIP --------------------------------- #")
        print("# + Longest trip         = %.1f h" % self.trip_statistics["duration"].max())
        print("# + Median trip duration = %.1f h" % self.trip_statistics["duration"].quantile(0.5))
        print("# + Largest trip         = %.1f km" % self.trip_statistics["length"].max())
        print("# + Median trip length   = %.1f km" % self.trip_statistics["length"].quantile(0.5))
    print("# + First position (%.5f, %.5f) is %.3fkm away from the estimated nest position (%.5f, %.5f)" % (pos0[0], pos0[1], d_pos0_nest, nest[0], nest[1]))
    print("# ------------------------------ TDR DATA ----------------------------- #")
    print("# + Nb of measures   = %d" % self.n_df_tdr)
    print("# + Number of dives  = %d" % self.nb_dives)
    print("# + Time resolution  = %.1f s" % self.tdr_resolution)
    print("# + Median pressure  = %.1f hPa" % self.median_pressure)
    print("# + Median depth     = %.2f m" % self.median_depth)
    print("# + Max depth        = %.2f m" % self.max_depth)
    print("# + Mean temperature = %.1f °C" % self.mean_temperature)
    if self.nb_dives>0:
        print("# ------------------------------ DIVE --------------------------------- #")
        print("# + Longest dive          = %.1f s" % self.dive_statistics["duration"].max())
        print("# + Median dive duration  = %.1f s" % self.dive_statistics["duration"].quantile(0.5))
        print("# + Median dive max depth = %.2f m" % self.dive_statistics["max_depth"].quantile(0.5))
    print("# ===================================================================== #")