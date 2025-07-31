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
def full_diagnostic(self, fig_dir=str, file_id=str, plot_params=dict):   
    
    # get attributes
    df = self.df
    df_gps = self.df_gps
    df_tdr = self.df_tdr
    group = self.group
    id = self.id
    params = self.params
    n_df = self.n_df
    n_df_gps = self.n_df_gps
    n_df_tdr = self.n_df_tdr
    start_datetime = self.start_datetime
    end_datetime = self.end_datetime
    gps_resolution = self.gps_resolution
    frequency = self.frequency
    total_duration = self.total_duration
    total_length = self.total_length
    dmax = self.dmax
    n_trip = self.n_trip
    median_odba = self.median_odba
    median_odba_f = self.median_odba_f
    nb_dives = self.nb_dives
    median_pressure = self.median_pressure
    median_depth = self.median_depth
    mean_temperature = self.mean_temperature
    [nest_lon, nest_lat] = self.nest_position
    trip_statistics = self.trip_statistics
    trip_duration = trip_statistics["duration"]
    trip_length = trip_statistics["length"]

    # get parameters
    cols_1 = plot_params.get("cols_1")
    cols_2 = plot_params.get("cols_2")
    cols_3 = plot_params.get("cols_3")
    diving_depth_threshold = params.get("diving_depth_threshold")
    
    # set infos to print on diagnostic
    infos = []
    infos.append("Group = %s" % group)
    infos.append("Id = %s" % id)
    infos.append("Number of AXY measures = %d" % n_df)
    infos.append("Number of GPS measures = %d" % n_df_gps)
    infos.append("Number of TDR measures = %d" % n_df_tdr)
    infos.append("Start date = %s | End date = %s" % (start_datetime.strftime("%Y-%m-%d"), end_datetime.strftime("%Y-%m-%d")))
    infos.append("GPS time resolution = %.1f s" % gps_resolution)
    infos.append("AXY frequency = %.1f Hz" % frequency)
    infos.append("Total duration = %.2f days" % total_duration)
    infos.append("Total length = %.1f km" % total_length)
    infos.append("Maximum distance to nest = %.1f km" % dmax)
    infos.append("Number of trips = %d" % n_trip)
    if n_trip>0:
        infos.append("Longest trip = %.1f h" % trip_statistics["duration"].max())
        infos.append("Median trip duration = %.1f h" % trip_statistics["duration"].quantile(0.5))
        infos.append("Largest trip = %.1f km" % trip_statistics["length"].max())
        infos.append("Median trip length = %.1f km" % trip_statistics["length"].quantile(0.5))
    infos.append("Median odba = %.3f" % median_odba)
    infos.append("Median odba_f = %.3f" % median_odba_f)
    infos.append("Number of dives = %d" % nb_dives)
    infos.append("Median pressure = %.1f hPa" % median_pressure)
    infos.append("Median depth = %.2f m" % median_depth)
    infos.append("Mean temperature = %.1f °C" % mean_temperature)
    
    # produce diagnostic
    fig = plt.figure(figsize=(30, 24), dpi=plot_params.get("fig_dpi"))
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3, wspace=0.25, bottom=0.06, top=0.95, left=0.05, right=0.95)
    gs = fig.add_gridspec(6, 5)
    
    # trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,0], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df_gps, params, plot_params, cols_1, n_trip, nest_lon, nest_lat, 0, trip_length, trip_duration)
    
    # zoom trajectory with a trip color gradient
    ax = fig.add_subplot(gs[0,1], projection=ccrs.PlateCarree())
    diagnostic.plot_map_wtrips(ax, df_gps, params, plot_params, cols_1, n_trip, nest_lon, nest_lat, 10, trip_length, trip_duration)
    
    # global trajectory with a step speed color gradient
    ax = fig.add_subplot(gs[0,2], projection=ccrs.PlateCarree())
    diagnostic.plot_map_colorgrad(ax, df_gps, params, plot_params, "step_speed", cols_2, nest_lon, nest_lat, "Trajectory [speed color gradient]", 0.95, 0)
    
    # global trajectory with a time color gradient
    ax = fig.add_subplot(gs[0,3], projection=ccrs.PlateCarree())
    df_gps["duration"] = (df_gps["datetime"]-df_gps["datetime"].min()).dt.total_seconds()/3600
    diagnostic.plot_map_colorgrad(ax, df_gps, params, plot_params, "duration", cols_3, nest_lon, nest_lat, "Trajectory [duration color gradient]", 1.0, 0)
    del df_gps["duration"]
    
    # plot infos
    ax = fig.add_subplot(gs[0,4])
    diagnostic.plot_infos(infos, plot_params)
    
    # step time timeserie
    ax = fig.add_subplot(gs[1,0])
    diagnostic.plot_ts(ax, df_gps, plot_params, "step_time", "GPS step time", "Time [s]")
    
    # step length timeserie
    ax = fig.add_subplot(gs[1,1])
    diagnostic.plot_ts(ax, df_gps, plot_params, "step_length", "Step length", "Length [km]")

    # step speed timeserie
    ax = fig.add_subplot(gs[1,2])
    diagnostic.plot_ts(ax, df_gps, plot_params, "step_speed", "Step speed", "Speed [km/h]")
    
    # step turning angle timeserie
    ax = fig.add_subplot(gs[1,3])
    diagnostic.plot_ts(ax, df_gps, plot_params, "step_turning_angle", "Step turning angle", "Angle [°]")
    
    # step heading angle timeserie
    ax = fig.add_subplot(gs[1,4])
    diagnostic.plot_ts(ax, df_gps, plot_params, "step_heading_to_colony", "Step heading to colony", "Angle [°]")
    
    # step time histogram
    ax = fig.add_subplot(gs[2,0])
    diagnostic.plot_hist(df_gps, plot_params, "step_time", "GPS step time", "Time [s]")

    # step length histogram
    ax = fig.add_subplot(gs[2,1])
    diagnostic.plot_hist(df_gps, plot_params, "step_length", "Step length", "Length [km]")
    
    # step speed histogram
    ax = fig.add_subplot(gs[2,2])
    diagnostic.plot_hist(df_gps, plot_params, "step_speed", "Step speed", "Speed [km/h]")

    # step turning angle histogram
    ax = fig.add_subplot(gs[2,3])
    diagnostic.plot_hist(df_gps, plot_params, "step_turning_angle", "Step turning angle", "Angle [°]")
    
    # heading polar plot
    ax = fig.add_subplot(gs[2,4], projection="polar")
    if(n_trip>0):
        df_gps["step_heading_to_colony_trip"] = df_gps.loc[df_gps["trip"]>0, "step_heading_to_colony"]
        diagnostic.plot_angle_polar(ax, df_gps, plot_params, "step_heading_to_colony_trip", "Step heading to colony", "Angle [°]")
        del df_gps["step_heading_to_colony_trip"]
    else:
        diagnostic.plot_angle_polar(ax, df_gps, plot_params, "step_heading_to_colony", "Step heading to colony", "Angle [°]")
    
    # distance to nest by trip
    ax = fig.add_subplot(gs[3,0:5])
    diagnostic.plot_ts_wtrips(ax, df_gps, plot_params, n_trip, "dist_to_nest", "Distance to nest", "Distance [km]")
    
    # ax timeserie
    ax = fig.add_subplot(gs[4,0])
    diagnostic.plot_ts_twinx(ax, df, plot_params, "ax", "Acceleration x-axis", "Ax [g]")
    
    # ay timeserie
    ax = fig.add_subplot(gs[4,1])
    diagnostic.plot_ts_twinx(ax, df, plot_params, "ay", "Acceleration y-axis", "Ay [g]")
    
    # az timeserie
    ax = fig.add_subplot(gs[4,2])
    diagnostic.plot_ts_twinx(ax, df, plot_params, "az", "Acceleration z-axis", "Az [g]")
     
    # odba timeserie
    ax = fig.add_subplot(gs[4,3])
    diagnostic.plot_ts_twinx(ax, df, plot_params, "odba", "Overall Dynamic Body Acceleration", "ODBA [g]")
        
    # odba timeserie zoom (50% to 50.1% dataframe length)
    ax = fig.add_subplot(gs[4,4])
    diagnostic.plot_ts_twinx(ax, df.iloc[int(0.5*n_df):int((0.5+0.001)*n_df)].reset_index(drop=True), plot_params, "odba", "Overall Dynamic Body Acceleration [Zoom]", "ODBA [g]", scatter=False)
    
    # pressure
    ax = fig.add_subplot(gs[5,0])
    diagnostic.plot_ts(ax, df_tdr, plot_params, "pressure", "%d Dives" % nb_dives, "Pressure [hPa]", eph_cond=(df_tdr["dive"]>0))
        
    # depth
    ax = fig.add_subplot(gs[5,1:3])
    diagnostic.plot_ts(ax, df_tdr, plot_params, "depth", "%d Dives" % nb_dives, "Depth [m]", hline=diving_depth_threshold, eph_cond=(df_tdr["dive"]>0))
    
    # temperature
    ax = fig.add_subplot(gs[5,3:5])
    diagnostic.plot_ts(ax, df_tdr, plot_params, "temperature", "Temperature", "Temperature [°C]", hline=mean_temperature)
    
    # save figure
    fig_path = os.path.join(fig_dir, "%s.png" % file_id)
    plt.savefig(fig_path, format="png", bbox_inches="tight")
    fig.clear()
    plt.close(fig)
    
    return fig


# ======================================================= #
# GPS MAPS DIAG [AXY METHOD]
# ======================================================= #
def maps_diagnostic(self, fig_dir=str, file_id=str, plot_params=dict):
        
    # get attributes
    gps = self.gps
    
    # plot using GPS method
    fig = gps.maps_diag(fig_dir, file_id, plot_params)
    
    return(fig)


# ======================================================= #
# GPS FOLIUM MAP [AXY METHOD]
# ======================================================= #
def folium_map(self, fig_dir=str, file_id=str):
        
    # get attributes
    gps = self.gps
    
    # plot using GPS method
    fmap = gps.folium_map(fig_dir, file_id)
    
    return(fmap)

# ======================================================= #
# GPS FOLIUM MAP [AXY METHOD]
# ======================================================= #
def folium_map_wtrips(self, fig_dir=str, file_id=str, plot_params=dict):
        
    # get attributes
    gps = self.gps
    
    # plot using GPS method
    fmap = gps.folium_map_wtrips(fig_dir, file_id, plot_params)

    return(fmap)

# ======================================================= #
# GPS FOLIUM MAP COLORGRAD [AXY METHOD]
# ======================================================= #
def folium_map_colorgrad(self, fig_dir=str, file_id=str, plot_params=dict):
    
    # get attributes
    gps = self.gps
    
    # plot using GPS method
    fmap = gps.folium_map_colorgrad(fig_dir, file_id, plot_params)

    return(fmap)