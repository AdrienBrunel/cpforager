# ======================================================= #
# LIBRARIES
# ======================================================= #
import numpy as np


# ======================================================= #
# DISPLAY [TDR_COLLECTION METHODS]
# ======================================================= #
def display_data_summary(self, standalone=True):
    
    """    
    Print in terminal the TDR_Collection data summary.
    
    :param self: a TDR_Collection object
    :type self: cpforager.TDR_Collection
    """

    # get attributes
    tdr_collection = self.tdr_collection
    dive_statistics_all = self.dive_statistics_all
    
    # append groups
    groups = []
    for tdr in tdr_collection:
        groups.append(tdr.group)
        
    # build string with group infos
    groups_str = "| "
    for group in np.unique(groups):
        groups_str = groups_str + "%s [%d TDR] | " % (group, sum(np.isin(groups, group)))
        
    # get quantiles dive statistics
    dive_duration_quantiles = dive_statistics_all["duration"].quantile([0,0.25,0.5,0.75,1])
    dive_dmax_quantiles = dive_statistics_all["max_depth"].quantile([0,0.25,0.5,0.75,1])
    
    # print information
    if standalone:
        print("# ============================== SUMMARY ============================== #")
        print("# ------------------------------ METADATA ----------------------------- #")
        print("# + Nb of TDR   = %d" % self.n_tdr)
        print("# + Nb of dives = %d" % self.n_dives)
        print("# + Groups      = %s" % groups_str)
    print("# ------------------------------ TDR COLLECTION DATA ------------------ #")
    print("# + Dive duration  : mean=%.1fs | std=%.1fs" % (dive_statistics_all["duration"].mean(), dive_statistics_all["duration"].std()))
    print("# + Dive duration  : min=%.1fs | q25=%.1fs | q50=%.1fs | q75=%.1fs | max=%.1fs" % (dive_duration_quantiles[0], dive_duration_quantiles[0.25], dive_duration_quantiles[0.5], dive_duration_quantiles[0.75], dive_duration_quantiles[1]))
    print("# + Dive max depth : mean=%.1fm | std=%.1fm" % (dive_statistics_all["max_depth"].mean(), dive_statistics_all["max_depth"].std()))
    print("# + Dive max depth : min=%.1fm | q25=%.1fm | q50=%.1fm | q75=%.1fm | max=%.1fm" % (dive_dmax_quantiles[0], dive_dmax_quantiles[0.25], dive_dmax_quantiles[0.5], dive_dmax_quantiles[0.75], dive_dmax_quantiles[1])) 
    if standalone:
        print("# ===================================================================== #")
    