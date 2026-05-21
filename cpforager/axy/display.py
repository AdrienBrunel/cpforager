# ======================================================= #
# LIBRARIES
# ======================================================= #


# ======================================================= #
# DISPLAY [AXY METHODS]
# ======================================================= #
def display_data_summary(self, standalone=True):
                
    """    
    Print in terminal the AXY data summary.
    
    :param self: a AXY object
    :type self: cpforager.AXY
    :param standalone: display information standalone if True.
    :type standalone: bool
    """

    # get attributes
    gps = self.gps
    tdr = self.tdr
    
    # print information
    if standalone:
        print("# ============================== SUMMARY ============================== #")
        print("# ------------------------------ METADATA ----------------------------- #")
        print("# + Group = %s" % self.group)
        print("# + Id    = %s" % self.id)
    gps.display_data_summary(standalone=False)
    tdr.display_data_summary(standalone=False)
    print("# ------------------------------ ACC DATA ----------------------------- #")
    print("# + Nb of measures            = %d" % self.n_df)
    print("# + Date range                = %s | %s" % (self.start_datetime, self.end_datetime))     
    print("# + Frequency                 = %.1f Hz" % self.frequency)
    print("# + Median (ax, ay, az)       = (%.3f, %.3f, %.3f)" % (self.df["ax"].median(), self.df["ay"].median(), self.df["az"].median()))
    print("# + Median (ax_s, ay_s, az_s) = (%.3f, %.3f, %.3f)" % (self.df["ax_s"].median(), self.df["ay_s"].median(), self.df["az_s"].median()))
    print("# + Median (ax_d, ay_d, az_d) = (%.3f, %.3f, %.3f)" % (self.df["ax_d"].median(), self.df["ay_d"].median(), self.df["az_d"].median()))
    print("# + Median odba               = %.3f" % self.median_odba)
    print("# + Median vedba               = %.3f" % self.median_vedba)
    print("# + Circular mean pitch              = %.3f" % self.circ_mean_pitch)
    print("# + Circular mean roll              = %.3f" % self.circ_mean_roll)
    # ajouter vedba
    if standalone:
        print("# ===================================================================== #")