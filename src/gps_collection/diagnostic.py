# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
import numpy as np
import pandas as pd
from src import diagnostic, misc
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.dates as mdates
import folium

# ======================================================= #
# STATS SUMMARY [GPS_COLLECTION METHOD]
# ======================================================= #
def plot_stats_summary(self, fig_dir=str, file_id=str, plot_params=dict, quantiles=[0.25, 0.50, 0.75, 0.90]):
    
    # get parameters
    dpi = plot_params.get("fig_dpi")
    
    # get attributes
    trip_statistics_all = self.trip_statistics_all

    # produce diagnostic
    fig = plt.figure(figsize=(20, 10), dpi=dpi)
    fig.subplots_adjust(hspace=0.45, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(4, 4)

    fig.add_subplot(gs[0,0])
    diagnostic.plot_hist(trip_statistics_all, plot_params, "length", "Trip length", "Length [km]")
    fig.add_subplot(gs[1,0])
    diagnostic.plot_box(trip_statistics_all, plot_params, "length", "Trip length", "Length [km]")
    # diagnostic.plot_violin(trip_statistics_all, plot_params, "length", "Trip length", "Length [km]", quantiles)
    fig.add_subplot(gs[2,0])
    diagnostic.plot_cumulative_distribution(trip_statistics_all, "length", "Trip length", "Distance [km]", plot_params, quantiles)
    fig.add_subplot(gs[0,1])
    diagnostic.plot_hist(trip_statistics_all, plot_params, "duration", "Trip duration", "Time [h]")
    fig.add_subplot(gs[1,1])
    diagnostic.plot_box(trip_statistics_all, plot_params, "duration", "Trip duration", "Time [h]")
    # diagnostic.plot_violin(trip_statistics_all, plot_params, "duration", "Trip duration", "Time [h]", quantiles)
    fig.add_subplot(gs[2,1])
    diagnostic.plot_cumulative_distribution(trip_statistics_all, "duration", "Trip duration", "Time [h]", plot_params, quantiles)
    fig.add_subplot(gs[0,2])
    diagnostic.plot_hist(trip_statistics_all, plot_params, "n_step", "Trip number of step", "Steps")
    fig.add_subplot(gs[1,2])
    diagnostic.plot_box(trip_statistics_all, plot_params, "n_step", "Trip number of step", "Steps")
    # diagnostic.plot_violin(trip_statistics_all, plot_params, "n_step", "Trip number of step", "Steps", quantiles)
    fig.add_subplot(gs[2,2])
    diagnostic.plot_cumulative_distribution(trip_statistics_all, "n_step", "Trip number of step", "Steps", plot_params, quantiles)
    fig.add_subplot(gs[0,3])
    diagnostic.plot_hist(trip_statistics_all, plot_params, "dmax", "Distance max to nest", "Distance [km]")
    fig.add_subplot(gs[1,3])
    diagnostic.plot_box(trip_statistics_all, plot_params, "dmax", "Distance max to nest", "Distance [km]")
    # diagnostic.plot_violin(trip_statistics_all, plot_params, "dmax", "Distance max to nest", "Distance [km]", quantiles)
    fig.add_subplot(gs[2,3])
    diagnostic.plot_cumulative_distribution(trip_statistics_all, "dmax", "Distance max to nest", "Distance [km]", plot_params, quantiles)
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return(fig)


# ======================================================= #
# GPS MAPS DIAG [GPS_COLLECTION METHOD]
# ======================================================= #
def maps_diagnostic(self, fig_dir=str, file_id=str, plot_params=dict):
    
    # get parameters
    dpi = plot_params.get("fig_dpi")
    cols_2 = plot_params.get("cols_2")
    params = self.gps_collection[0].params
    colony = params.get("colony")
    
    # get attributes
    df_all = self.df_all
    n_trip = self.n_trip
        
    # produce diagnostic
    fig = plt.figure(figsize=(10, 10), dpi=dpi)
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(2, 2)
    
    # set random colors
    cols_rand = misc.random_colors(3)
    
    # trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,0], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df_all, params, plot_params, cols_rand, n_trip, colony["center"][0], colony["center"][1], 0)
    
    # zoom trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,1], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df_all, params, plot_params, cols_rand, n_trip, colony["center"][0], colony["center"][1], 10)

    # global trajectory with a step speed color gradient
    ax = fig.add_subplot(gs[1,0], projection=ccrs.PlateCarree())
    diagnostic.plot_map_colorgrad(ax, df_all, params, plot_params, "step_speed", cols_2, colony["center"][0], colony["center"][1], "Trajectory [speed color gradient]", 0.95, 0)
    
    # global trajectory with a step speed color gradient
    ax = fig.add_subplot(gs[1,0], projection=ccrs.PlateCarree())
    ax.axis("off")
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return(fig)


# ======================================================= #
# GPS FOLIUM MAPS [GPS_COLLECTION METHOD]
# ======================================================= #
def folium_map(self, fig_dir=str, file_id=str):
    
    # get attributes
    params = self.gps_collection[0].params
    gps_collection = self.gps_collection
    
    # get parameters
    colony = params.get("colony")
    
    # produce folium map
    fmap = folium.Map(location=[colony["center"][1], colony["center"][0]])
    for gps in gps_collection:
        colony = gps.params.get("colony")
        folium.Marker(location=[colony["center"][1], colony["center"][0]], popup="<i>Colony</i>").add_to(fmap)
        folium.PolyLine(tooltip=gps.id, locations=gps.df[["latitude", "longitude"]].values.tolist(), 
                        color=misc.rgb_to_hex(misc.random_colors()[0]), weight=2, opacity=0.7).add_to(fmap)   
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.html" % file_id)
    fmap.save(fig_path) 

    return(fmap)