# ======================================================= #
# LIBRARIES
# ======================================================= #
import numpy as np


# ======================================================= #
# DISPLAY [GPS_COLLECTION METHODS]
# ======================================================= #
def display_data_summary(self, standalone=True):
    
    """    
    Print in terminal the GPS_Collection data summary.
    
    :param self: a GPS_Collection object
    :type self: cpforager.GPS_Collection
    """

    # get attributes
    gps_collection = self.gps_collection
    trip_statistics_all = self.trip_statistics_all
    
    # append groups
    groups = []
    for gps in gps_collection:
        groups.append(gps.group)
        
    # build string with group infos
    groups_str = "| "
    for group in np.unique(groups):
        groups_str = groups_str + "%s [%d GPS] | " % (group, sum(np.isin(groups, group)))
        
    # get quantiles trip statistics
    trip_length_quantiles = trip_statistics_all["length"].quantile([0,0.25,0.5,0.75,1])
    trip_duration_quantiles = trip_statistics_all["duration"].quantile([0,0.25,0.5,0.75,1])
    trip_dmax_quantiles = trip_statistics_all["dmax"].quantile([0,0.25,0.5,0.75,1])
    trip_nstep_quantiles = trip_statistics_all["n_step"].quantile([0,0.25,0.5,0.75,1])
    
    # print information
    if standalone:
        print("# ============================== SUMMARY ============================== #")
        print("# ------------------------------ METADATA ----------------------------- #")
        print("# + Nb of GPS   = %d" % self.n_gps)
        print("# + Nb of trips = %d" % self.n_trips)
        print("# + Groups      = %s" % groups_str)
    print("# ------------------------------ GPS COLLECTION DATA ------------------ #")
    print("# + Trip length   : mean=%.1fkm | std=%.1fkm" % (trip_statistics_all["length"].mean(), trip_statistics_all["length"].std()))
    print("# + Trip length   : min=%.1fkm | q25=%.1fkm | q50=%.1fkm | q75=%.1fkm | max=%.1fkm" % (trip_length_quantiles[0], trip_length_quantiles[0.25], trip_length_quantiles[0.5], trip_length_quantiles[0.75], trip_length_quantiles[1]))
    print("# + Trip duration : mean=%.1fh | std=%.1fh" % (trip_statistics_all["duration"].mean(), trip_statistics_all["duration"].std()))
    print("# + Trip duration : min=%.1fh | q25=%.1fh | q50=%.1fh | q75=%.1fh | max=%.1fh" % (trip_duration_quantiles[0], trip_duration_quantiles[0.25], trip_duration_quantiles[0.5], trip_duration_quantiles[0.75], trip_duration_quantiles[1]))
    print("# + Trip dist max : mean=%.1fkm | std=%.1fkm" % (trip_statistics_all["dmax"].mean(), trip_statistics_all["dmax"].std()))
    print("# + Trip dist max : min=%.1fkm | q25=%.1fkm | q50=%.1fkm | q75=%.1fkm | max=%.1fkm" % (trip_dmax_quantiles[0], trip_dmax_quantiles[0.25], trip_dmax_quantiles[0.5], trip_dmax_quantiles[0.75], trip_dmax_quantiles[1])) 
    print("# + Trip nb steps : mean=%.1f | std=%.1f" % (trip_statistics_all["n_step"].mean(), trip_statistics_all["n_step"].std()))
    print("# + Trip nb steps : min=%d | q25=%d | q50=%d | q75=%d | max=%d" % (trip_nstep_quantiles[0], trip_nstep_quantiles[0.25], trip_nstep_quantiles[0.5], trip_nstep_quantiles[0.75], trip_nstep_quantiles[1])) 
    if standalone:
        print("# ===================================================================== #")
    