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
    print("# + Median (ax_f, ay_f, az_f) = (%.3f, %.3f, %.3f)" % (self.df["ax_f"].median(), self.df["ay_f"].median(), self.df["az_f"].median()))
    print("# + Median odba               = %.3f" % self.median_odba)
    print("# + Median odba_f             = %.3f" % self.median_odba_f)
    if standalone:
        print("# ===================================================================== #")