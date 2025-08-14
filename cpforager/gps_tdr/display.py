# ======================================================= #
# LIBRARIES
# ======================================================= #


# ======================================================= #
# DISPLAY [GPS_TDR METHODS]
# ======================================================= #
def display_data_summary(self, standalone=True):
                
    """    
    Print in terminal the GPS_TDR data summary.
    
    :param self: a GPS_TDR object
    :type self: cpforager.GPS_TDR
    :param standalone: display information standalone if True.
    :type standalone: bool
    """

    # print information
    if standalone:
        print("# ============================== SUMMARY ============================== #")
        print("# ------------------------------ METADATA ----------------------------- #")
        print("# + Group = %s" % self.group)
        print("# + Id    = %s" % self.id)
    self.gps.display_data_summary(standalone=False)
    self.tdr.display_data_summary(standalone=False)
    if standalone:
        print("# ===================================================================== #")