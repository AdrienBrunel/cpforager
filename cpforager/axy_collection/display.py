# ======================================================= #
# LIBRARIES
# ======================================================= #
import numpy as np


# ======================================================= #
# DISPLAY [AXY_COLLECTION METHODS]
# ======================================================= #
def display_data_summary(self, standalone=True):
    
    """    
    Print in terminal the AXY_Collection data summary.
    
    :param self: a AXY_Collection object
    :type self: cpforager.AXY_Collection
    """

    # get attributes
    axy_collection = self.axy_collection
    gps_collection = self.gps_collection
    tdr_collection = self.tdr_collection
    
    # append groups
    groups = []
    for axy in axy_collection:
        groups.append(axy.group)
        
    # build string with group infos
    groups_str = "| "
    for group in np.unique(groups):
        groups_str = groups_str + "%s [%d AXY] | " % (group, sum(np.isin(groups, group)))
    
    # print information
    if standalone:
        print("# ============================== SUMMARY ============================== #")
        print("# ------------------------------ METADATA ----------------------------- #")
        print("# + Nb of AXY   = %d" % self.n_axy)
        print("# + Nb of trips = %d" % self.n_trips)
        print("# + Groups      = %s" % groups_str)
    gps_collection.display_data_summary(standalone=False)
    tdr_collection.display_data_summary(standalone=False)
    if standalone:
        print("# ===================================================================== #")
    