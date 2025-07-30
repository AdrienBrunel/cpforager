# ======================================================= #
# LIBRARIES
# ======================================================= #


# ======================================================= #
# DISPLAY [TDR METHODS]
# ======================================================= #
def display_data_summary(self):
                
    # print information
    print("# ============================== SUMMARY ============================== #")
    print("# ------------------------------ METADATA ----------------------------- #")
    print("# + Group = %s" % self.group)
    print("# + Id    = %s" % self.id)
    print("# ------------------------------ TDR DATA ----------------------------- #")
    print("# + Nb of measures   = %d" % self.n_df)
    print("# + Number of dives  = %d" % self.nb_dives)
    print("# + Median pressure  = %.1f hPa" % self.median_pressure)
    print("# + Median depth     = %.2f m" % self.median_depth)
    print("# + Mean temperature = %.1f °C" % self.mean_temperature)
    print("# ===================================================================== #")