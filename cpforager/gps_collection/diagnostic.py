# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
from cpforager import diagnostic, misc, utils
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import folium


# ======================================================= #
# STATS SUMMARY [GPS_COLLECTION METHOD]
# ======================================================= #
def plot_stats_summary(self, fig_dir, file_id, plot_params, quantiles=[0.25, 0.50, 0.75, 0.90]):
    
    """    
    Produce the trip statistics summary of every GPS data.
    
    :param self: a GPS_Collection object
    :type self: cpforager.GPS_Collection
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
    trip_statistics_all = self.trip_statistics_all

    # produce diagnostic
    fig = plt.figure(figsize=(20, 10), dpi=dpi)
    fig.subplots_adjust(hspace=0.45, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(3, 4)
    
    # add subplots
    fig.add_subplot(gs[0,0])
    diagnostic.plot_hist(trip_statistics_all, plot_params, "length", "Trip length", "Length [km]")
    fig.add_subplot(gs[1,0])
    diagnostic.plot_box(trip_statistics_all, plot_params, "length", "Trip length", "Length [km]")
    fig.add_subplot(gs[2,0])
    diagnostic.plot_cumulative_distribution(trip_statistics_all, plot_params, "length", "Trip length", "Distance [km]", quantiles)
    fig.add_subplot(gs[0,1])
    diagnostic.plot_hist(trip_statistics_all, plot_params, "duration", "Trip duration", "Time [h]")
    fig.add_subplot(gs[1,1])
    diagnostic.plot_box(trip_statistics_all, plot_params, "duration", "Trip duration", "Time [h]")
    fig.add_subplot(gs[2,1])
    diagnostic.plot_cumulative_distribution(trip_statistics_all, plot_params, "duration", "Trip duration", "Time [h]", quantiles)
    fig.add_subplot(gs[0,2])
    diagnostic.plot_hist(trip_statistics_all, plot_params, "n_step", "Trip number of step", "Steps")
    fig.add_subplot(gs[1,2])
    diagnostic.plot_box(trip_statistics_all, plot_params, "n_step", "Trip number of step", "Steps")
    fig.add_subplot(gs[2,2])
    diagnostic.plot_cumulative_distribution(trip_statistics_all, plot_params, "n_step", "Trip number of step", "Steps", quantiles)
    fig.add_subplot(gs[0,3])
    diagnostic.plot_hist(trip_statistics_all, plot_params, "dmax", "Distance max to nest", "Distance [km]")
    fig.add_subplot(gs[1,3])
    diagnostic.plot_box(trip_statistics_all, plot_params, "dmax", "Distance max to nest", "Distance [km]")
    fig.add_subplot(gs[2,3])
    diagnostic.plot_cumulative_distribution(trip_statistics_all, plot_params, "dmax", "Distance max to nest", "Distance [km]", quantiles)
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return(fig)


# ======================================================= #
# GPS MAPS DIAG [GPS_COLLECTION METHOD]
# ======================================================= #
def maps_diagnostic(self, fig_dir, file_id, plot_params, rand=False):
    
    """    
    Produce the maps with every GPS data.
    
    :param self: a GPS_Collection object
    :type self: cpforager.GPS_Collection_Collection
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
    df_all = self.df_all
    n_trips = self.n_trips
    params = self.gps_collection[0].params
    
    # get parameters
    dpi = plot_params.get("fig_dpi")
    cols_1 = plot_params.get("cols_1")
    cols_2 = plot_params.get("cols_2")
    colony = params.get("colony")
        
    # produce diagnostic
    fig = plt.figure(figsize=(10, 10), dpi=dpi)
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(2, 2)
    
    # set discrete color palette
    disc_color_palette = cols_1
    if rand:
        disc_color_palette = misc.random_colors(n_trips)
    
    # renumber trips in df_all for a better trip visualisation 
    df_all_rnb_trips = df_all[["longitude", "latitude", "trip"]].copy(deep=True)
    nonzero_mask = (df_all_rnb_trips["trip"] != 0)
    is_trip_start = nonzero_mask & (~nonzero_mask.shift(1, fill_value=False))
    df_all_rnb_trips["trip"] = is_trip_start.cumsum()
    df_all_rnb_trips.loc[~nonzero_mask, "trip"] = 0       
    
    # trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,0], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df_all_rnb_trips, params, plot_params, disc_color_palette, n_trips, colony["center"][0], colony["center"][1], "Trajectory [trip color gradient]", 0)
    
    # zoom trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,1], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df_all_rnb_trips, params, plot_params, disc_color_palette, n_trips, colony["center"][0], colony["center"][1], "Trajectory [trip color gradient]", 10)

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
# GPS INDIV MAP ALL [GPS_COLLECTION METHOD]
# ======================================================= #
def indiv_map_all(self, fig_dir, file_id, plot_params):
    
    """    
    Produce the individual map of every GPS in collection.
    
    :param self: a GPS_Collection object
    :type self: cpforager.GPS_Collection
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
    n_gps = self.n_gps
    gps_collection = self.gps_collection
    
    # get parameters
    dpi = plot_params.get("fig_dpi")
    cols_1 = plot_params.get("cols_1")
    
    # compute figure layout
    n_columns, n_rows = utils.nearsq_grid_layout(n_gps) 
    
    # produce diagnostic
    fig = plt.figure(figsize=(n_columns*5, n_rows*5), dpi=dpi)
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(n_rows, n_columns)
    
    # loop over subplots
    for k in range(n_columns*n_rows):
        
        # plot gps map if gps in collection
        if k < n_gps:
            
            # get gps from collection
            gps = gps_collection[k]
            
            # get gps infos
            n_trips = gps.n_trips
            [nest_lon, nest_lat] = gps.nest_position
            trip_statistics = gps.trip_statistics
            trip_duration = trip_statistics["duration"]
            trip_length =trip_statistics["length"]
            
            # add individual gps map colored by trip
            ax = fig.add_subplot(gs[int(k/n_columns), k % n_columns], projection=ccrs.PlateCarree())
            diagnostic.plot_map_wtrips(ax, gps.df, gps.params, plot_params, cols_1, n_trips, nest_lon, nest_lat, "Trajectory [trip color gradient]", 0, trip_length, trip_duration)
        
        # empty plot if no gps in collection    
        else:        
            ax = fig.add_subplot(gs[int(k/n_columns), k % n_columns], projection=ccrs.PlateCarree())
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
def folium_map(self, fig_dir, file_id, plot_params, rand=False):
    
    """    
    Produce the html map with every GPS data colored by seabird id.
    
    :param self: a GPS_Collection object
    :type self: cpforager.GPS_Collection
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
    n_gps = self.n_gps
    params_0 = self.gps_collection[0].params
    
    # get parameters
    colony_0 = params_0.get("colony")
    cols_1 = plot_params.get("cols_1")
    
    # produce folium map
    fmap = folium.Map(location=[colony_0["center"][1], colony_0["center"][0]])
    for k in range(n_gps):
        gps = gps_collection[k]
        colony = gps.params.get("colony")
        folium.Marker(location=[colony["center"][1], colony["center"][0]], popup="<i>Colony %s</i>" % (colony["name"])).add_to(fmap)
        if rand:
            folium.PolyLine(tooltip="<i>Id %s</i>" % (gps.id), locations=gps.df[["latitude", "longitude"]].values.tolist(), 
                            color=misc.rgb_to_hex(misc.random_colors()[0]), weight=2, opacity=0.7).add_to(fmap)   
        else:
            folium.PolyLine(tooltip="<i>Id %s</i>" % (gps.id), locations=gps.df[["latitude", "longitude"]].values.tolist(), 
                            color=misc.rgb_to_hex(cols_1[k % len(cols_1)]), weight=2, opacity=0.7).add_to(fmap)   
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.html" % file_id)
    fmap.save(fig_path) 

    return(fmap)