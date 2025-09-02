# ======================================================= #
# LIBRARIES
# ======================================================= #
import os
from cpforager import diagnostic
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


# ======================================================= #
# GPS FULL DIAG [GPS METHOD]
# ======================================================= #
def full_diagnostic(self, fig_dir, file_id, plot_params):   
    
    """    
    Produce the full diagnostic of the GPS data.
    
    :param self: a GPS object
    :type self: cpforager.GPS
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
    
    # get parameters
    cols_1 = plot_params.get("cols_1")
    cols_2 = plot_params.get("cols_2")
    cols_3 = plot_params.get("cols_3")
    
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
    total_length = self.total_length
    dmax = self.dmax
    n_trips = self.n_trips
    [nest_lon, nest_lat] = self.nest_position
    trip_statistics = self.trip_statistics
    trip_duration = trip_statistics["duration"]
    trip_length = trip_statistics["length"]

    # set infos to print on diagnostic
    infos = []
    infos.append("Group = %s" % group)
    infos.append("Id = %s" % id)
    infos.append("Number of measures = %d" % n_df)
    infos.append("Start date = %s | End date = %s" % (start_datetime.strftime("%Y-%m-%d"), end_datetime.strftime("%Y-%m-%d")))
    infos.append("Time resolution = %.1f s" % resolution)
    infos.append("Total duration = %.2f days" % total_duration)
    infos.append("Total length = %.1f km" % total_length)
    infos.append("Maximum distance to nest = %.1f km" % dmax)
    infos.append("Number of trips = %d" % n_trips)
    if n_trips>0:
        infos.append("Longest trip = %.1f h" % trip_statistics["duration"].max())
        infos.append("Median trip duration = %.1f h" % trip_statistics["duration"].quantile(0.5))
        infos.append("Largest trip = %.1f km" % trip_statistics["length"].max())
        infos.append("Median trip length = %.1f km" % trip_statistics["length"].quantile(0.5))
    
    # produce diagnostic
    fig = plt.figure(figsize=(30, 16), dpi=plot_params.get("fig_dpi"))
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(4, 5)
    
    # trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,0], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df, params, plot_params, cols_1, n_trips, nest_lon, nest_lat, "Trajectory [trip color gradient]", 0, trip_length, trip_duration)
    
    # zoom trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,1], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df, params, plot_params, cols_1, n_trips, nest_lon, nest_lat, "Trajectory [trip color gradient]", 10, trip_length, trip_duration)
    
    # global trajectory with a step speed color gradient
    ax = fig.add_subplot(gs[0,2], projection=ccrs.PlateCarree())
    diagnostic.plot_map_colorgrad(ax, df, params, plot_params, "step_speed", cols_2, nest_lon, nest_lat, "Trajectory [speed color gradient]", 0.95, 0)
    
    # global trajectory with a time color gradient
    ax = fig.add_subplot(gs[0,3], projection=ccrs.PlateCarree())
    df["duration"] = (df["datetime"]-df["datetime"].min()).dt.total_seconds()/3600
    diagnostic.plot_map_colorgrad(ax, df, params, plot_params, "duration", cols_3, nest_lon, nest_lat, "Trajectory [duration color gradient]", 1.0, 0)
    del df["duration"]
    
    # plot infos
    ax = fig.add_subplot(gs[0,4])
    diagnostic.plot_infos(infos, plot_params)
    
    # step time timeserie
    ax = fig.add_subplot(gs[1,0])
    diagnostic.plot_ts(ax, df, plot_params, "step_time", "Step time", "Time [s]")
    
    # step length timeserie
    ax = fig.add_subplot(gs[1,1])
    diagnostic.plot_ts(ax, df, plot_params, "step_length", "Step length", "Length [km]")

    # step speed timeserie
    ax = fig.add_subplot(gs[1,2])
    diagnostic.plot_ts(ax, df, plot_params, "step_speed", "Step speed", "Speed [km/h]")
    
    # step turning angle timeserie
    ax = fig.add_subplot(gs[1,3])
    diagnostic.plot_ts(ax, df, plot_params, "step_turning_angle", "Step turning angle", "Angle [°]")
    
    # step heading angle timeserie
    ax = fig.add_subplot(gs[1,4])
    diagnostic.plot_ts(ax, df, plot_params, "step_heading_to_colony", "Step heading to colony", "Angle [°]")
    
    # step time histogram
    ax = fig.add_subplot(gs[2,0])
    diagnostic.plot_hist(df, plot_params, "step_time", "Step time", "Time [s]")

    # step length histogram
    ax = fig.add_subplot(gs[2,1])
    diagnostic.plot_hist(df, plot_params, "step_length", "Step length", "Length [km]")
    
    # step speed histogram
    ax = fig.add_subplot(gs[2,2])
    diagnostic.plot_hist(df, plot_params, "step_speed", "Step speed", "Speed [km/h]")

    # step turning angle histogram
    ax = fig.add_subplot(gs[2,3])
    diagnostic.plot_hist(df, plot_params, "step_turning_angle", "Step turning angle", "Angle [°]")
    
    # heading polar plot
    ax = fig.add_subplot(gs[2,4], projection="polar")
    if(n_trips>0):
        df["step_heading_to_colony_trip"] = df.loc[df["trip"]>0, "step_heading_to_colony"]
        diagnostic.plot_angle_polar(ax, df, plot_params, "step_heading_to_colony_trip", "Step heading to colony", "Angle [°]")
        del df["step_heading_to_colony_trip"]
    else:
        diagnostic.plot_angle_polar(ax, df, plot_params, "step_heading_to_colony", "Step heading to colony", "Angle [°]")
    
    # distance to nest by trip
    ax = fig.add_subplot(gs[3,0:5])
    diagnostic.plot_ts_wtrips(ax, df, plot_params, n_trips, "dist_to_nest", "Distance to nest", "Distance [km]")
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return(fig)


# ======================================================= #
# GPS MAPS DIAG [GPS METHOD]
# ======================================================= #
def maps_diagnostic(self, fig_dir, file_id, plot_params):
    
    """    
    Produce the maps of the GPS data.
    
    :param self: a GPS object
    :type self: cpforager.GPS
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
    
    # get parameters
    cols_1 = plot_params.get("cols_1")
    cols_2 = plot_params.get("cols_2")
    cols_3 = plot_params.get("cols_3")
    
    # get attributes
    df = self.df
    params = self.params
    
    # get infos
    n_trips = self.n_trips
    [nest_lon, nest_lat] = self.nest_position
    trip_statistics = self.trip_statistics
    trip_duration = trip_statistics["duration"]
    trip_length =trip_statistics["length"]
    
    # produce diagnostic
    fig = plt.figure(figsize=(10, 10), dpi=plot_params.get("fig_dpi"))
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(2, 2)
    
    # trajectory with a colony color gradient
    ax = fig.add_subplot(gs[0,0], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df, params, plot_params, cols_1, n_trips, nest_lon, nest_lat, "Trajectory [trip color gradient]", 0, trip_length, trip_duration)
    
    # zoom trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,1], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df, params, plot_params, cols_1, n_trips, nest_lon, nest_lat, "Trajectory [trip color gradient]", 10)
    
    # global trajectory with a step speed color gradient
    ax = fig.add_subplot(gs[1,0], projection=ccrs.PlateCarree())
    diagnostic.plot_map_colorgrad(ax, df, params, plot_params, "step_speed", cols_2, nest_lon, nest_lat, "Trajectory [speed color gradient]", 0.95, 0)
    
    # global trajectory with a time color gradient
    ax = fig.add_subplot(gs[1,1], projection=ccrs.PlateCarree())
    df["duration"] = (df["datetime"]-df["datetime"].min()).dt.total_seconds()/3600
    diagnostic.plot_map_colorgrad(ax, df, params, plot_params, "duration", cols_3, nest_lon, nest_lat, "Trajectory [duration color gradient]", 1.0, 0)
    del df["duration"]
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return(fig)


# ======================================================= #
# GPS FOLIUM MAP BEAUTIFUL [GPS METHOD]
# ======================================================= #
def folium_map(self, fig_dir, file_id, plot_params):
    
    """    
    Produce the html map of the GPS data with the possibility to choose a color gradient.
    
    :param self: a GPS object
    :type self: cpforager.GPS
    :param fig_dir: figure saving directory.
    :type fig_dir: str
    :param file_id: name of the saved figure.
    :type file_id: str
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :return: the folium map.
    :rtype: folium.Map
    
    The figure is saved at the html format.
    
    .. warning::
        Producing the figure may take some time and the resulting html may be heavy.
    """
    
    # get attributes
    df = self.df
    params = self.params
    id = self.id
    
    # get parameters
    cols_1 = plot_params.get("cols_1")
    cols_2 = plot_params.get("cols_2")
    
    # define color palettes
    discrete_color_palettes = {"trip":cols_1}
    continuous_color_palettes = {"step_speed":cols_2, "duration":cols_2}

    # produce beautiful map
    df["duration"] = (df["datetime"]-df["datetime"].min()).dt.total_seconds()/3600
    fmap = diagnostic.plot_folium_map_multiple_colorgrad(df, params, id, discrete_color_palettes, continuous_color_palettes, 0.99)
    del df["duration"]
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.html" % file_id)
    fmap.save(fig_path) 
    
    return(fmap)