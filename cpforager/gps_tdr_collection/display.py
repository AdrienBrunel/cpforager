# ======================================================= #
# LIBRARIES
# ======================================================= #
import numpy as np


# ======================================================= #
# DISPLAY [GPS_TDR_COLLECTION METHODS]
# ======================================================= #
def display_data_summary(self, standalone=True):
    
    """    
    Print in terminal the GPS_TDR_Collection data summary.
    
    :param self: a GPS_TDR_Collection object
    :type self: cpforager.GPS_TDR_Collection
    """

    # get attributes
    gps_tdr_collection = self.gps_tdr_collection
    gps_collection = self.gps_collection
    tdr_collection = self.tdr_collection
    
    # append groups
    groups = []
    for gps_tdr in gps_tdr_collection:
        groups.append(gps_tdr.group)
        
    # build string with group infos
    groups_str = "| "
    for group in np.unique(groups):
        groups_str = groups_str + "%s [%d GPS_TDR] | " % (group, sum(np.isin(groups, group)))
    
    # print information
    if standalone:
        print("# ============================== SUMMARY ============================== #")
        print("# ------------------------------ METADATA ----------------------------- #")
        print("# + Nb of GPS_TDR = %d" % self.n_gps_tdr)
        print("# + Nb of trips   = %d" % self.n_trips)
        print("# + Groups        = %s" % groups_str)
    gps_collection.display_data_summary(standalone=False)
    tdr_collection.display_data_summary(standalone=False)
    if standalone:
        print("# ===================================================================== #")
    