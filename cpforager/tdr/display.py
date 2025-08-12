# ======================================================= #
# LIBRARIES
# ======================================================= #


# ======================================================= #
# DISPLAY [TDR METHODS]
# ======================================================= #
def display_data_summary(self, standalone=True):
    
    """    
    Print in terminal the TDR data summary.
    
    :param self: a TDR object
    :type self: cpforager.TDR
    :param standalone: display information standalone if True.
    :type standalone: bool
    """
                
    # print information
    if standalone:
        print("# ============================== SUMMARY ============================== #")
        print("# ------------------------------ METADATA ----------------------------- #")
        print("# + Group = %s" % self.group)
        print("# + Id    = %s" % self.id)
    print("# ------------------------------ TDR DATA ----------------------------- #")
    print("# + Nb of measures   = %d" % self.n_df)
    print("# + Number of dives  = %d" % self.n_dives)
    print("# + Median pressure  = %.1f hPa" % self.median_pressure)
    print("# + Median depth     = %.2f m" % self.median_depth)
    print("# + Max depth        = %.2f m" % self.max_depth)
    print("# + Mean temperature = %.1f °C" % self.mean_temperature)
    if self.n_dives>0:
        print("# ------------------------------ DIVES -------------------------------- #")
        print("# + Longest dive          = %.1f s" % self.dive_statistics["duration"].max())
        print("# + Median dive duration  = %.1f s" % self.dive_statistics["duration"].quantile(0.5))
        print("# + Median dive max depth = %.2f m" % self.dive_statistics["max_depth"].quantile(0.5))
    if standalone:
        print("# ===================================================================== #")