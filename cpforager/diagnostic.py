import numpy as np
from cpforager import misc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcols
from matplotlib.patches import Rectangle
import cartopy.feature as cfeature
import folium


# ======================================================= #
# GET LOCATOR AND FORMATTER OF DATETIME
# ======================================================= # 
def get_datetime_locator_formatter(df, custom_locator=None, custom_formatter=None):
    
    """    
    :param df: dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param custom_locator: data locator. 
    :type custom_locator: matplotlib.dates.DayLocator
    :param custom_formatter: date formatter. 
    :type custom_formatter: matplotlib.dates.DateFormatter
    :return: the dictionary of axy infos.
    :rtype: dict
    
    Return the date locator and formatter for timeserie plots.
    """
    
    # set datetime locator/formatter to auto values
    if ((df["datetime"].max() - df["datetime"].min()).total_seconds() > 14*86400):
        datetime_formatter = mdates.DateFormatter("%d/%m")
        datetime_locator = mdates.DayLocator(interval=7)
    else:
        datetime_formatter = mdates.DateFormatter("%d/%m")
        datetime_locator = mdates.DayLocator(interval=1)
    
    # set datetime locator/formatter to custom values        
    if not(custom_locator is None): datetime_locator = custom_locator
    if not(custom_formatter is None): datetime_formatter = custom_formatter
        
    return(datetime_locator, datetime_formatter)


# ======================================================= #
# PLOT NIGHT
# ======================================================= #
def plot_night(df, plot_params):
        
    """    
    :param df: dataframe with ``datetime`` and ``is_night`` columns.
    :type df: pandas.DataFrame
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :return: the timeserie plot with night represented by grey rectangles.
    :rtype: matplotlib.pyplot
    
    Return the timeserie plot with night represented by grey rectangles.
    """
    
    # compute index when night starts and ends
    n_df = len(df)
    idx_start_night = np.where(df["is_night"].diff() == 1)[0]
    idx_end_night = np.where(df["is_night"].diff() == -1)[0]
    if df.loc[0,"is_night"] == 1:
        idx_start_night = np.append(0, idx_start_night)
    if df.loc[n_df-1,"is_night"] == 1:
        idx_end_night = np.append(idx_end_night, n_df-1)
    n_days = len(idx_start_night)
    
    # plot night as rectangle
    for k in range(n_days):
        plt.axvspan(df.loc[idx_start_night[k],"datetime"], df.loc[idx_end_night[k],"datetime"], color="grey", alpha=plot_params["night_transp"])
        
        
# ======================================================= #
# PLOT TIMESERIES
# ======================================================= #        
def plot_ts(ax, df, plot_params, var, title, var_lab, custom_locator=None, custom_formatter=None, scatter=True, hline=None, eph_cond=None):
        
    """    
    :param ax: 
    :type ax: 
    :param df: dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param var: name of the column in df.
    :type var: str
    :param title: plot title.
    :type title: str
    :param var_lab: y-axis label.
    :type var_lab: str
    :param custom_locator: data locator. 
    :type custom_locator: matplotlib.dates.DayLocator
    :param custom_formatter: date formatter. 
    :type custom_formatter: matplotlib.dates.DateFormatter
    :param scatter: scatter plot if True, line plot otherwise.
    :type scatter: bool 
    :param hline: value of the horizontal line to plot. 
    :type hline: float
    :param eph_cond: condition to emphasize points.
    :type eph_cond: pandas.DataFrame
    :return: the timeserie plot of dataframe column named var.
    :rtype: matplotlib.pyplot
    
    Return the timeserie plot of dataframe column named var.
    """
    
    # plot timeserie of var in dataframe
    datetime_locator, datetime_formatter = get_datetime_locator_formatter(df, custom_locator, custom_formatter)
    plot_night(df, plot_params)
    if scatter:
        plt.scatter(df["datetime"], df[var], s=plot_params["pnt_size"], marker=plot_params["pnt_type"])
    else:
        plt.plot(df["datetime"], df[var], linewidth=plot_params["pnt_size"])
    if not(hline is None):
        plt.axhline(y=hline, color="orange", linestyle="--", linewidth=plot_params["pnt_size"])
    if not(eph_cond is None):
        plt.scatter(df.loc[eph_cond, "datetime"], df.loc[eph_cond, var], s=plot_params["eph_size"], color="red")
    plt.title(title, fontsize=plot_params["main_fs"])
    plt.xlabel("Time", fontsize=plot_params["labs_fs"])
    plt.ylabel(var_lab, fontsize=plot_params["labs_fs"])
    plt.tick_params(axis="both", labelsize=plot_params["axis_fs"])
    plt.grid(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"])
    ax.xaxis.set(major_locator=datetime_locator, major_formatter=datetime_formatter)


# ======================================================= #
# PLOT TIMESERIES WITH TRIP COLORS
# ======================================================= # 
def plot_ts_wtrips(ax, df, plot_params, n_trip, var, title, var_lab, custom_locator=None, custom_formatter=None):
        
    """    
    :param ax: 
    :type ax: 
    :param df: dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param n_trip: number of trips.
    :type n_trip: int
    :param var: name of the column in df.
    :type var: str
    :param title: plot title.
    :type title: str
    :param var_lab: y-axis label.
    :type var_lab: str
    :param custom_locator: data locator. 
    :type custom_locator: matplotlib.dates.DayLocator
    :param custom_formatter: date formatter. 
    :type custom_formatter: matplotlib.dates.DateFormatter
    :return: the timeserie plot of dataframe column named var colored by trips.
    :rtype: matplotlib.pyplot
    
    Return the timeserie plot of dataframe column named var colored by trips.
    """

    # plot timeserie of var in dataframe with trip colors
    n_cols = len(plot_params["cols_1"])
    datetime_locator, datetime_formatter = get_datetime_locator_formatter(df, custom_locator, custom_formatter)
    plot_night(df, plot_params)
    plt.scatter(df["datetime"], df[var], s=plot_params["pnt_size"], marker=plot_params["pnt_type"], color="black")
    if n_trip >= 1:
        for i in range(n_trip):
            trip_id = i+1
            plt.scatter(df.loc[df["trip"] == trip_id, "datetime"], df.loc[df["trip"] == trip_id, var], s=plot_params["pnt_size"], color=plot_params["cols_1"][i % n_cols])
    plt.title(title, fontsize=plot_params["main_fs"])
    plt.xlabel("Time", fontsize=plot_params["labs_fs"])
    plt.ylabel(var_lab, fontsize=plot_params["labs_fs"])
    plt.tick_params(axis="both", labelsize=plot_params["axis_fs"])
    plt.grid(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"])
    ax.xaxis.set(major_locator=datetime_locator, major_formatter=datetime_formatter)
    
    
# ======================================================= #
# PLOT RAW AND FILTERED VAR
# ======================================================= # 
def plot_ts_twinx(ax, df, plot_params, var, title, var_lab, custom_locator=None, custom_formatter=None, scatter=True):
        
    """    
    :param ax: 
    :type ax: 
    :param df: dataframe with a ``datetime`` column.
    :type df: pandas.DataFrame
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param var: name of the column in df.
    :type var: str
    :param title: plot title.
    :type title: str
    :param var_lab: y-axis label.
    :type var_lab: str
    :param custom_locator: data locator. 
    :type custom_locator: matplotlib.dates.DayLocator
    :param custom_formatter: date formatter. 
    :type custom_formatter: matplotlib.dates.DateFormatter
    :param scatter: scatter plot if True, line plot otherwise.
    :type scatter: bool 
    :return: the timeserie plot of dataframe column named var and var_f with two separated axes.
    :rtype: matplotlib.pyplot
    
    Return the timeserie plot of dataframe column named var and var_f with two separated axes. Useful to plot the raw and filtered data.
    """
    
    # plot timeserie of var and var_f in dataframe with two axes
    datetime_locator, datetime_formatter = get_datetime_locator_formatter(df, custom_locator, custom_formatter)
    plot_night(df, plot_params)
    if scatter:
        plt.scatter(df["datetime"], df[var], s=plot_params["pnt_size"], marker=plot_params["pnt_type"], edgecolor="None")
        ax_twinx = ax.twinx()
        ax_twinx.scatter(df["datetime"], df["%s_f" % var], s=plot_params["pnt_size"], marker=plot_params["pnt_type"], edgecolor="None", color="red")
    else:
        plt.plot(df["datetime"], df[var], linewidth=plot_params["pnt_size"])
        ax_twinx = ax.twinx()
        ax_twinx.plot(df["datetime"], df["%s_f" % var], linewidth=plot_params["pnt_size"], color="red")
    plt.title(title, fontsize=plot_params["main_fs"])
    plt.xlabel("Time", fontsize=plot_params["labs_fs"])
    plt.ylabel(var_lab, fontsize=plot_params["labs_fs"])
    plt.tick_params(axis="both", labelsize=plot_params["axis_fs"])
    plt.grid(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"])
    ax.xaxis.set(major_locator=datetime_locator, major_formatter=datetime_formatter)
    ax_twinx.spines["right"].set_color("red")
    ax_twinx.tick_params("y", colors="red")
    
    
# ======================================================= #
# PLOT CUMULATIVE DISTRIB OF TRIP/DIVE STATS
# ======================================================= #   
def plot_cumulative_distribution(df, plot_params, var, title, var_lab, v_qs=[0.25, 0.50, 0.75]):
        
    """    
    :param df: dataframe of trip/dive statistics.
    :type df: pandas.DataFrame
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param var: name of the column in df.
    :type var: str
    :param title: plot title.
    :type title: str
    :param var_lab: x-axis label.
    :type var_lab: str
    :param v_qs: array of quantiles to emphasize.
    :type v_qs: array(float)
    :return: the cumulative distribution plot.
    :rtype: matplotlib.pyplot
    
    Return the cumulative distribution plot. Useful to plot cumulative distribution of trip and dive statistics.
    """
    
    # total number of trips
    n_df = len(df)
    
    # compute cumulative distrib of var
    quantiles = np.arange(0,1,0.01)
    cumul_distrib = df[var].quantile(quantiles)

    # plot cumulative distrib of var
    plt.plot(cumul_distrib, quantiles*n_df)
    plt.xlabel(var_lab, fontsize=plot_params["labs_fs"])
    plt.ylabel("Number of trips", fontsize=plot_params["labs_fs"])
    plt.tick_params(axis="both", labelsize=plot_params["axis_fs"])
    plt.grid(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"])
    plt.axhline(y=n_df, color="black", linestyle="dashed", linewidth=1.0)
    title = "%s \n|" % title
    for v_q in v_qs:
        q = df[var].quantile(v_q, interpolation="lower")
        plt.axvline(x=q, color="red", linestyle="dashed", linewidth=1.0)
        plt.text(q, 0, "q%d" % int(100*v_q), rotation="vertical", fontsize=plot_params["labs_fs"])
        title = "%s q%d=%d |" % (title, int(100*v_q), int(q))
    plt.title("Cumulative distribution - %s" % title, fontsize=plot_params["main_fs"])


# ======================================================= #
# PLOT BOXPLOT
# ======================================================= #        
def plot_box(df, plot_params, var, title, var_lab):
        
    """    
    :param df: dataframe of trip/dive statistics.
    :type df: pandas.DataFrame
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param var: name of the column in df.
    :type var: str
    :param title: plot title.
    :type title: str
    :param var_lab: x-axis label.
    :type var_lab: str
    :return: the boxplot.
    :rtype: matplotlib.pyplot
    
    Return the boxplot.
    """
       
    # boxplot of var
    plt.boxplot(df[var], vert=False)
    plt.title(title, fontsize=plot_params["main_fs"])
    plt.xlabel(var_lab, fontsize=plot_params["labs_fs"])
    plt.tick_params(axis="both", labelsize=plot_params["axis_fs"])
    plt.grid(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"])
    
    
# ======================================================= #
# PLOT VIOLINPLOT
# ======================================================= #        
def plot_violin(df, plot_params, var, title, var_lab, quantiles=[0.25, 0.50, 0.75]):
        
    """    
    :param df: dataframe of trip/dive statistics.
    :type df: pandas.DataFrame
    :param plot_params: plot parameters dictionary. 
    :type plot_params: dict
    :param var: name of the column in df.
    :type var: str
    :param title: plot title.
    :type title: str
    :param var_lab: x-axis label.
    :type var_lab: str
    :param quantiles: array of quantiles to emphasize.
    :type quantiles: array(float)
    :return: the violin plot.
    :rtype: matplotlib.pyplot
    
    Return the violin plot.
    """
       
    # violinplot of var
    plt.violinplot(df[var], orientation="horizontal", quantiles=quantiles)
    plt.title(title, fontsize=plot_params["main_fs"])
    plt.xlabel(var_lab, fontsize=plot_params["labs_fs"])
    plt.tick_params(axis="both", labelsize=plot_params["axis_fs"])
    plt.grid(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"])
    
    
# ======================================================= #
# PLOT HISTOGRAMS
# ======================================================= #        
def plot_hist(df, plot_params, var, title, var_lab, bins=None, color=None, alpha=None, custom_locator=None, custom_formatter=None):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """
       
    # plot histogram of var
    plt.hist(df[var], density=True, edgecolor="white", bins=bins, color=color, alpha=alpha)
    plt.title(title, fontsize=plot_params["main_fs"])
    plt.xlabel(var_lab, fontsize=plot_params["labs_fs"])
    plt.ylabel("Frequency", fontsize=plot_params["labs_fs"])
    plt.tick_params(axis="both", labelsize=plot_params["axis_fs"])
    plt.grid(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"])
    if not((custom_locator is None) and (custom_formatter is None)):
        datetime_locator, datetime_formatter = get_datetime_locator_formatter(df, custom_locator, custom_formatter)
        plt.gca().xaxis.set(major_locator=datetime_locator, major_formatter=datetime_formatter)
    
 
# ======================================================= #
# PLOT POLAR HISTOGRAMS
# ======================================================= #    
def plot_angle_polar(ax, df, plot_params, var, title, var_lab):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """
       
    # plot polar histogram of var
    plt.hist(np.radians(df[var]), bins=np.linspace(0, 2*np.pi, 37), color="orange", alpha=0.9, edgecolor="black", density=True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_xticks(np.linspace(0, 2*np.pi, 8, endpoint=False))
    ax.set_xticklabels(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    plt.tick_params(labelsize=plot_params["axis_fs"])
    plt.title(title, fontsize=plot_params["main_fs"])
    plt.xlabel(var_lab, fontsize=plot_params["labs_fs"])
    plt.grid(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"])
    
    
# ======================================================= #
# PLOT MAPS WITH COLONY COLORS
# ======================================================= #  
def plot_colony(ax, params):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """

    # get parameters
    colony = params.get("colony")
    
    # trajectory with a colony color gradient
    ax.add_patch(Rectangle(xy=(colony["box_longitude"][0], colony["box_latitude"][0]), width=np.diff(colony["box_longitude"])[0], height=np.diff(colony["box_latitude"])[0], fill=False, color="red"))
    

# ======================================================= #
# PLOT MAPS WITH TRIP COLORS
# ======================================================= #  
def plot_map_wtrips(ax, df, params, plot_params, color_palette, n_trip, nest_lon, nest_lat, zoom, trip_length=None, trip_duration=None):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """
    
    # get parameters
    colony = params.get("colony")
    
    # trajectory with a trip color gradient
    n_cols = len(color_palette)
    plt.scatter(df["longitude"], df["latitude"], s=plot_params["pnt_size"], marker=plot_params["pnt_type"], color="black")
    if n_trip >= 1:
        for i in range(n_trip):
            trip_id = i+1
            if((trip_length is not None) and (trip_duration is not None)):
                trip_lgd_lab = "%.1fkm - %.1fh " % (trip_length[i], trip_duration[i])
                plt.scatter(df.loc[df["trip"] == trip_id, "longitude"], df.loc[df["trip"] == trip_id, "latitude"], s=plot_params["pnt_size"], color=color_palette[i % n_cols], label=trip_lgd_lab)   
            else:
                plt.scatter(df.loc[df["trip"] == trip_id, "longitude"], df.loc[df["trip"] == trip_id, "latitude"], s=plot_params["pnt_size"], color=color_palette[i % n_cols])   
    plot_colony(ax, params)
    plt.title("Trajectory [trip color gradient]", fontsize=plot_params["main_fs"])
    ax.set_xlabel("Longitude [°]", fontsize=plot_params["labs_fs"])
    ax.set_ylabel("Latitude [°]", fontsize=plot_params["labs_fs"])
    ax.gridlines(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"],
                 draw_labels=["bottom", "left"], xformatter=plot_params["lon_fmt"], yformatter=plot_params["lat_fmt"], 
                 xlabel_style={"size": plot_params["labs_fs"]}, ylabel_style={"size": plot_params["labs_fs"]})
    ax.add_feature(cfeature.LAND.with_scale("10m"), zorder=0)
    ax.add_feature(cfeature.COASTLINE.with_scale("10m"), zorder=1)
    if zoom>0:
        plt.scatter(nest_lon, nest_lat, marker="*", s=10*plot_params["mrk_size"], color="yellow", edgecolor="black")
        colony_clon = (colony["box_longitude"][0]+colony["box_longitude"][1])/2
        colony_clat = (colony["box_latitude"][0]+colony["box_latitude"][1])/2
        colony_dlon = (colony["box_longitude"][1]-colony["box_longitude"][0])/2
        colony_dlat = (colony["box_latitude"][1]-colony["box_latitude"][0])/2
        plt.xlim([colony_clon - zoom*colony_dlon, colony_clon + zoom*colony_dlon])
        plt.ylim([colony_clat - zoom*colony_dlat, colony_clat + zoom*colony_dlat])
    else:
        if((trip_length is not None) and (trip_duration is not None)):
            plt.legend(loc="best", fontsize=plot_params["text_fs"], markerscale=5)
        plt.axis("equal")


# ======================================================= #
# PLOT MAPS WITH COLOR GRADIENT
# ======================================================= #  
def plot_map_colorgrad(ax, df, params, plot_params, var, color_palette, nest_lon, nest_lat, title, q_th, zoom):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """
    
    # get parameters
    colony = params.get("colony")
    
    # global trajectory with a color gradient
    n_cols = len(color_palette)
    df[var] = df[var].fillna(0)
    t = (df[var]-df[var].min())/(df[var].max()-df[var].min())
    t[t > t.quantile(q_th)] = 1
    sbplt = plt.scatter(df["longitude"], df["latitude"], color=color_palette[np.round((n_cols-1)*t).values.round().astype(int)], s=plot_params["pnt_size"])
    plot_colony(ax, params)
    plt.title("Trajectory [%s color gradient]" % var, fontsize=plot_params["main_fs"])
    ax.set_xlabel("Longitude [°]", fontsize=plot_params["labs_fs"])
    ax.set_ylabel("Latitude [°]", fontsize=plot_params["labs_fs"])
    ax.gridlines(linestyle=plot_params["grid_lty"], linewidth=plot_params["grid_lwd"], color=plot_params["grid_col"],
                 draw_labels=["bottom", "left"], xformatter=plot_params["lon_fmt"], yformatter=plot_params["lat_fmt"], 
                 xlabel_style={"size": plot_params["labs_fs"]}, ylabel_style={"size": plot_params["labs_fs"]})
    ax.add_feature(cfeature.LAND.with_scale("10m"), zorder=0)
    ax.add_feature(cfeature.COASTLINE.with_scale("10m"), zorder=1)
    cb = plt.colorbar(sbplt, ax=ax, orientation="vertical", shrink=plot_params["cb_shrink"], pad=plot_params["cb_pad"], aspect=plot_params["cb_aspect"])
    sbplt.set_clim(df[var].min(), df[var].max())
    cb.ax.yaxis.get_offset_text().set(size=plot_params["axis_fs"]/2)
    cb.ax.tick_params(labelsize=plot_params["axis_fs"])
    cb.set_label(title, size=plot_params["labs_fs"])  
    sbplt.set_cmap(mcols.LinearSegmentedColormap.from_list("", color_palette))
    if zoom>0:
        plt.scatter(nest_lon, nest_lat, marker="*", s=10*plot_params["mrk_size"], color="yellow", edgecolor="black")
        colony_clon = (colony["box_longitude"][0]+colony["box_longitude"][1])/2
        colony_clat = (colony["box_latitude"][0]+colony["box_latitude"][1])/2
        colony_dlon = (colony["box_longitude"][1]-colony["box_longitude"][0])/2
        colony_dlat = (colony["box_latitude"][1]-colony["box_latitude"][0])/2
        plt.xlim([colony_clon - zoom*colony_dlon, colony_clon + zoom*colony_dlon])
        plt.ylim([colony_clat - zoom*colony_dlat, colony_clat + zoom*colony_dlat])
    else:
        # plt.legend(loc="best", fontsize=plot_params["text_fs"], markerscale=5)
        plt.axis("equal")
    
    
# ======================================================= #
# PLOT MAP FOLIUM
# ======================================================= # 
def plot_folium_map(df, params, id):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """
    
    # get parameters
    colony = params.get("colony")
    
    # produce folium map
    fmap = folium.Map(location = [colony["center"][1], colony["center"][0]])
    folium.Marker(location=[colony["center"][1], colony["center"][0]], popup="<i>Colony</i>").add_to(fmap)
    folium.PolyLine(tooltip=id, locations=df[["latitude", "longitude"]].values.tolist(), 
                    color=misc.rgb_to_hex(misc.random_colors()[0]), weight=3, opacity=0.7).add_to(fmap)
    
    return(fmap)


# ======================================================= #
# PLOT MAP FOLIUM WITH TRIP COLORS
# ======================================================= # 
def plot_folium_map_wtrips(df, params, id, n_trip, color_palette):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """
    
    # get parameters
    colony = params.get("colony")
    
    # produce folium map with a trip color gradient
    n_cols = len(color_palette)
    fmap = folium.Map(location = [colony["center"][1], colony["center"][0]])
    folium.Marker(location=[colony["center"][1], colony["center"][0]], popup="<i>Colony</i>").add_to(fmap)
    folium.PolyLine(tooltip=id, locations=df[["latitude", "longitude"]].values.tolist(), 
                    color="black", weight=3, opacity=0.7).add_to(fmap)
    if n_trip >= 1:
        for i in range(n_trip):
            trip_id = i+1
            folium.PolyLine(tooltip="%s - %d" % (id, trip_id), locations=df.loc[df["trip"] == trip_id, ["latitude", "longitude"]].values.tolist(), 
                            color=misc.rgb_to_hex(color_palette[i % n_cols]), weight=3, opacity=0.7).add_to(fmap)
    
    return(fmap)


# ======================================================= #
# PLOT MAP COLORGRAD FOLIUM
# ======================================================= # 
def plot_folium_map_colorgrad(df, params, var, color_palette, q_th):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """
    
    # get parameters
    colony = params.get("colony")

    # get size of color palette and dataframe
    n_df = len(df)
    n_cols = len(color_palette)
    
    # compute normalized values of var
    df[var] = df[var].fillna(0)
    t = (df[var]-df[var].min())/(df[var].max()-df[var].min())
    t[t > t.quantile(q_th)] = 1
    
    # produce folium map
    fmap = folium.Map(location=[colony["center"][1], colony["center"][0]])
    folium.Marker(location=[colony["center"][1], colony["center"][0]], popup="<i>Colony</i>").add_to(fmap)
    for k in range(n_df):
        folium.CircleMarker(location=(df.loc[k,"latitude"], df.loc[k,"longitude"]), fill=True, fill_opacity=0.7,
                            popup="Step Speed: %.1f" % (df.loc[k,"step_speed"]),radius=1, 
                            color=misc.rgb_to_hex(color_palette[np.round((n_cols-1)*t[k]).round().astype(int)])).add_to(fmap)
    return(fmap)
    
    
# ======================================================= #
# PLOT INFOS AS TEXT
# ======================================================= #
def plot_infos(infos, plot_params):
        
    # """    
    # :param df: dataframe with ``datetime`` and ``is_night`` columns.
    # :type df: pandas.DataFrame
    # :param plot_params: plot parameters dictionary. 
    # :type plot_params: dict
    # :return: XXXX.
    # :rtype: matplotlib.pyplot
    
    # Return the date locator and formatter for timeserie plots.
    # """
    
    n_infos = len(infos)
    plt.scatter(np.linspace(0,1,n_infos), range(n_infos), color="white", s=plot_params.get("pnt_size"))
    plt.ylim([0,0.9*n_infos])
    for k in range(n_infos):
        info = infos[k]
        x = -0.1
        y = 0.9*(n_infos - k)
        plt.text(x, y, info, fontsize=plot_params.get("text_fs"), ha="left", va="top")
    plt.axis("off")