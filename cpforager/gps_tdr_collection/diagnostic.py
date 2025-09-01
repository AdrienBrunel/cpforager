# ======================================================= #
# LIBRARIES
# ======================================================= #


# ======================================================= #
# TRIP STATS SUMMARY [GPS_TDR_COLLECTION METHOD]
# ======================================================= #
def plot_trip_stats_summary(self, fig_dir, file_id, plot_params, quantiles=[0.25, 0.50, 0.75, 0.90]):
    
    """    
    Produce the trip statistics summary of every GPS_TDR data.
    
    :param self: an GPS_TDR_Collection object
    :type self: cpforager.GPS_TDR_Collection
    :param fig_dir: figure saving directory.
    :type fig_dir: str
    :param file_id: name of the saved figure.
    :type file_id: str
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param quantiles: quantiles to emphasize. 
    :type quantiles: array(float)
    :return: the full diagnostic figure.
    :rtype: matplotlib.pyplot.Figure 
    
    The figure is save at the png format. Plots are histogram, boxplot and cumulative distribution.
    """
            
    # get attributes
    gps_collection = self.gps_collection
    
    # plot using GPS_Collection method
    fig = gps_collection.plot_stats_summary(fig_dir, file_id, plot_params, quantiles)
    
    return(fig)


# ======================================================= #
# DIVE STATS SUMMARY [GPS_TDR_COLLECTION METHOD]
# ======================================================= #
def plot_dive_stats_summary(self, fig_dir, file_id, plot_params, quantiles=[0.25, 0.50, 0.75, 0.90]):
    
    """    
    Produce the dive statistics summary of every GPS_TDR data.
    
    :param self: an GPS_TDR_Collection object
    :type self: cpforager.GPS_TDR_Collection
    :param fig_dir: figure saving directory.
    :type fig_dir: str
    :param file_id: name of the saved figure.
    :type file_id: str
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param quantiles: quantiles to emphasize. 
    :type quantiles: array(float)
    :return: the full diagnostic figure.
    :rtype: matplotlib.pyplot.Figure 
    
    The figure is save at the png format. Plots are histogram, boxplot and cumulative distribution.
    """
            
    # get attributes
    tdr_collection = self.tdr_collection
    
    # plot using TDR_Collection method
    fig = tdr_collection.plot_stats_summary(fig_dir, file_id, plot_params, quantiles)
    
    return(fig)


# ======================================================= #
# GPS_TDR MAPS DIAG [GPS_TDR_COLLECTION METHOD]
# ======================================================= #
def maps_diagnostic(self, fig_dir, file_id, plot_params, rand=False):
    
    """    
    Produce the maps with every GPS_TDR data.
    
    :param self: an GPS_TDR_Collection object
    :type self: cpforager.GPS_TDR_Collection
    :param fig_dir: figure saving directory.
    :type fig_dir: str
    :param file_id: name of the saved figure.
    :type file_id: str
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param rand: True if colors should be random. 
    :type rand: bool
    :return: the full diagnostic figure.
    :rtype: matplotlib.pyplot.Figure 
    
    The figure is save at the png format.
    """
    
    # get attributes
    gps_collection = self.gps_collection
    
    # plot using GPS_Collection method
    fig = gps_collection.maps_diagnostic(fig_dir, file_id, plot_params, rand)
    
    return(fig)
    

# ======================================================= #
# GPS_TDR INDIV DEPTH ALL [GPS_TDR_COLLECTION METHOD]
# ======================================================= #
def indiv_map_all(self, fig_dir, file_id, plot_params):
    
    """    
    Produce the individual map of every GPS_TDR in collection.
    
    :param self: an GPS_TDR_Collection
    :type self: cpforager.GPS_TDR_Collection
    :param fig_dir: figure saving directory.
    :type fig_dir: str
    :param file_id: name of the saved figure.
    :type file_id: str
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :return: the full diagnostic figure.
    :rtype: matplotlib.pyplot.Figure 
    
    The figure is save at the png format.
    """
    
    # get attributes
    gps_collection = self.gps_collection
    
    # plot using GPS_Collection method
    fig = gps_collection.indiv_map_all(fig_dir, file_id, plot_params)
    
    return(fig)


# ======================================================= #
# GPS_TDR INDIV DEPTH ALL [GPS_TDR_COLLECTION METHOD]
# ======================================================= #
def indiv_depth_all(self, fig_dir, file_id, plot_params):
    
    """    
    Produce the individual depth plot of every GPS_TDR in collection.
    
    :param self: an GPS_TDR_Collection object
    :type self: cpforager.GPS_TDR_Collection
    :param fig_dir: figure saving directory.
    :type fig_dir: str
    :param file_id: name of the saved figure.
    :type file_id: str
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :return: the full diagnostic figure.
    :rtype: matplotlib.pyplot.Figure 
    
    The figure is save at the png format.
    """
    
    # get attributes
    tdr_collection = self.tdr_collection
    
    # plot using TDR_Collection method
    fig = tdr_collection.indiv_depth_all(fig_dir, file_id, plot_params)
    
    return(fig)


# ======================================================= #
# GPS_TDR FOLIUM MAPS [GPS_TDR_COLLECTION METHOD]
# ======================================================= #
def folium_map(self, fig_dir, file_id, plot_params, rand=False):
    
    """    
    Produce the html map with every GPS_TDR data colored randomly.
    
    :param self: an GPS_TDR_Collection
    :type self: cpforager.GPS_TDR_Collection
    :param fig_dir: figure saving directory.
    :type fig_dir: str
    :param file_id: name of the saved figure.
    :type file_id: str
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param rand: True if colors should be random. 
    :type rand: bool
    :return: the folium map.
    :rtype: folium.Map
    
    The figure is save at the html format.
    """
    
    # get attributes
    gps_collection = self.gps_collection
   
    # plot using GPS_Collection method
    fmap = gps_collection.folium_map(fig_dir, file_id, plot_params, rand)

    return(fmap)