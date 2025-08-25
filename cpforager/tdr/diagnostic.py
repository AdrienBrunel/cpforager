# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
from cpforager import diagnostic
import matplotlib.pyplot as plt


# ======================================================= #
# TDR FULL DIAG [TDR METHOD]
# ======================================================= #
def full_diagnostic(self, fig_dir, file_id, plot_params):   
    
    """    
    Produce the full diagnostic of the TDR data.
    
    :param self: a TDR object
    :type self: cpforager.TDR
    :param fig_dir: figure saving directory.
    :type fig_dir: str
    :param file_id: name of the saved figure.
    :type file_id: str
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :return: the full diagnostic figure.
    :rtype: matplotlib.pyplot.Figure 
    """
    
    # get attributes
    df = self.df
    group = self.group
    id = self.id
    params = self.params
    n_df = self.n_df
    start_datetime = self.start_datetime
    end_datetime = self.end_datetime
    resolution = self.resolution
    total_duration = self.total_duration
    n_dives = self.n_dives
    median_pressure = self.median_pressure
    median_depth = self.median_depth
    max_depth = self.max_depth
    mean_temperature = self.mean_temperature
    dive_statistics = self.dive_statistics

    # get parameters
    diving_depth_threshold = params.get("diving_depth_threshold")
    
    # set infos to print on diagnostic
    infos = []
    infos.append("Group = %s" % group)
    infos.append("Id = %s" % id)
    infos.append("Number of TDR measures = %d" % n_df)
    infos.append("Start date = %s | End date = %s" % (start_datetime.strftime("%Y-%m-%d"), end_datetime.strftime("%Y-%m-%d")))
    infos.append("TDR time resolution = %.1f s" % resolution)
    infos.append("Total duration = %.2f days" % total_duration)
    infos.append("Number of dives = %d" % n_dives)
    infos.append("Median pressure = %.1f hPa" % median_pressure)
    infos.append("Median depth = %.2f m" % median_depth)
    infos.append("Max depth = %.2f m" % max_depth)
    infos.append("Mean temperature = %.1f °C" % mean_temperature)
    if n_dives>0:
        infos.append("Longest dive = %.1f s" % dive_statistics["duration"].max())
        infos.append("Median dive duration = %.1f s" % dive_statistics["duration"].quantile(0.5))
        infos.append("Median dive max depth = %.2f m" % dive_statistics["max_depth"].quantile(0.5))
    
    # produce diagnostic
    fig = plt.figure(figsize=(20, 10), dpi=plot_params.get("fig_dpi"))
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(2, 3)

    # pressure
    ax = fig.add_subplot(gs[0,0])
    diagnostic.plot_ts(ax, df, plot_params, "pressure", "%d Dives" % n_dives, "Pressure [hPa]", eph_cond=(df["dive"]>0))
    
    # step time timeserie
    ax = fig.add_subplot(gs[0,1])
    diagnostic.plot_ts(ax, df, plot_params, "step_time", "TDR step time", "Time [s]")
    
    # plot infos
    ax = fig.add_subplot(gs[0,2])
    diagnostic.plot_infos(infos, plot_params)
    
    # depth
    ax = fig.add_subplot(gs[1,0])
    diagnostic.plot_ts(ax, df, plot_params, "depth", "%d Dives" % n_dives, "Depth [m]", hline=diving_depth_threshold, eph_cond=(df["dive"]>0))
    
    # temperature
    ax = fig.add_subplot(gs[1,1])
    diagnostic.plot_ts(ax, df, plot_params, "temperature", "Temperature", "Temperature [°C]", hline=mean_temperature)
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return fig