# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import math
from cpforager import diagnostic
import matplotlib.pyplot as plt


# ======================================================= #
# STATS SUMMARY [TDR_COLLECTION METHOD]
# ======================================================= #
def plot_stats_summary(self, fig_dir, file_id, plot_params, quantiles=[0.25, 0.50, 0.75, 0.90]):
    
    """    
    Produce the dive statistics summary of every TDR data.
    
    :param self: a TDR_Collection object
    :type self: cpforager.TDR_Collection
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
    
    # get parameters
    dpi = plot_params.get("fig_dpi")
    
    # get attributes
    dive_statistics_all = self.dive_statistics_all

    # produce diagnostic
    fig = plt.figure(figsize=(20, 5), dpi=dpi)
    fig.subplots_adjust(hspace=0.45, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(3, 2)

    fig.add_subplot(gs[0,0])
    diagnostic.plot_hist(dive_statistics_all, plot_params, "duration", "Dive duration", "Time [s]")
    fig.add_subplot(gs[1,0])
    diagnostic.plot_box(dive_statistics_all, plot_params, "duration", "Dive duration", "Time [s]")
    fig.add_subplot(gs[2,0])
    diagnostic.plot_cumulative_distribution(dive_statistics_all, plot_params, "duration", "Dive duration", "Time [s]", quantiles)
    fig.add_subplot(gs[0,1])
    diagnostic.plot_hist(dive_statistics_all, plot_params, "max_depth", "Dive max depth", "Depth [m]")
    fig.add_subplot(gs[1,1])
    diagnostic.plot_box(dive_statistics_all, plot_params, "max_depth", "Dive max depth", "Depth [m]")
    fig.add_subplot(gs[2,1])
    diagnostic.plot_cumulative_distribution(dive_statistics_all, plot_params, "max_depth", "Dive max depth", "Depth [m]", quantiles)
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return(fig)


# ======================================================= #
# TDR INDIV DEPTH ALL [TDR_COLLECTION METHOD]
# ======================================================= #
def indiv_depth_all(self, fig_dir, file_id, plot_params):
    
    """    
    Produce the individual depth plot of every TDR in collection.
    
    :param self: a TDR_Collection object
    :type self: cpforager.TDR_Collection
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
    n_tdr = self.n_tdr
    tdr_collection = self.tdr_collection
    
    # get parameters
    dpi = plot_params.get("fig_dpi")
    
    # compute figure layout
    n_columns = 4
    n_rows = math.ceil(n_tdr/n_columns)
    
    # produce diagnostic
    fig = plt.figure(figsize=(n_columns*5, n_rows*5), dpi=dpi)
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(n_rows, n_columns)
    
    # loop over subplots
    for k in range(n_columns*n_rows):
        
        # plot tdr map if tdr in collection
        if k < n_tdr:
            
            # get tdr from collection
            tdr = tdr_collection[k]
            
            # get tdr infos
            n_dives = tdr.n_dives
            
            # add individual tdr map colored by dive
            ax = fig.add_subplot(gs[int(k/n_columns), k % n_columns])    
            diagnostic.plot_ts(ax, tdr.df, plot_params, "pressure", "%d Dives" % n_dives, "Pressure [hPa]", eph_cond=(tdr.df["dive"]>0))
        
        # empty plot if no tdr in collection    
        else:        
            ax = fig.add_subplot(gs[int(k/n_columns), k % n_columns])
            ax.axis("off")
            
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return(fig)