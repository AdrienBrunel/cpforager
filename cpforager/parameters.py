# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import numpy as np
import matplotlib.pyplot as plt
import cartopy.mpl.ticker as cmpl
import yaml


# ================================================================================================ #
# DICTIONARY OF PARAMETERS
# ================================================================================================ #
def get_params(config_file_paths):
    
    """
    Create a parameters dictionary loaded from a list of *.yml* paths.
    
    :param config_file_paths: a list of the *.yml* configuration file paths.
    :type config_file_paths: list[str]
    :return: a dictionary of parameters.
    :rtype: dict
    
    The parameters dictionary is required to construct ``GPS``, ``TDR`` and ``AXY`` classes. The user-defined colony code allows to define a 
    dictionary of parameters according to a specific dataset. Find below the exhaustive table of parameters within the dictionary.
    
    .. important::
        Users only have to write the *.yml* files with parameter values consistent with their dataset and their need. 
        
    .. warning::
        Even if all your parameters are written in a unique *.yml* file, you must express it as a single-element list *e.g.* ``params = get_params(["my_unique_config_path.yml"])``.
        
    .. note::
        The website at https://mapscaping.com/bounding-box-calculator/ is a user-friendly tool that can help define the colony bounding box.
        
    .. csv-table::  
        :header: "name", "description", "required"
        :widths: auto

        ``colony``, "dictionary with infos about the searbird's colony", "``GPS``"
        ``colony["name"]``, "name of the searbird's colony", "``GPS``"
        ``colony["center"]``, "longitude/latitude center of the searbird's colony", "``GPS``"
        ``colony["box_longitude"]``, "longitude bounding box inside which the searbird's nest is to be found", "``GPS``"
        ``colony["box_latitude"]``, "latitude bounding box inside which the searbird's nest is to be found", "``GPS``"
        ``local_tz``, "local timezone of the seabird's nest", "``GPS``, ``AXY``, ``TDR``"
        ``max_possible_speed``, "speed threshold in km/h above which a longitude/latitude measure can be considered an error", "``GPS``"
        ``dist_threshold``, "distance from the nest threshold in km above which the seabird is considered in a foraging trip", "``GPS``"
        ``speed_threshold``, "speed threshold in km/h above which the seabird is still considered in a foraging trip despite being below the distance threshold", "``GPS``"
        ``nesting_speed``, "local timezone of the seabird's nest", "``GPS``"
        ``nest_position``, "longitude and latitude of the seabird's nest if known beforehand", "``GPS``"
        ``trip_min_duration``, "duration in seconds above which a trip is valid", "``GPS``"
        ``trip_max_duration``, "duration in seconds below which a trip is valid", "``GPS``"
        ``trip_min_length``, "length in km above which a trip is valid", "``GPS``"
        ``trip_max_length``, "length in km below which a trip is valid", "``GPS``"
        ``trip_min_steps``, "length in km below which a trip is valid", "``GPS``"
        ``zoc_time_windows``, "widths of successive rolling time windows used for zero-offset correction", "``TDR``"
        ``zoc_quantiles``, "quantiles to keep during the successive rolling time windows used for zero-offset correction", "``TDR``"
        ``diving_depth_threshold``, "depth threshold above which a seabird is considered to be diving", "``TDR``"
        ``dive_min_duration``, "minimum duration in seconds of a dive", "``TDR``"
        ``odba_p_norm``, "p-norm used for the computation of overall dyanmical body acceleration", "``AXY``"
        ``filter_type``, "choose type of filter for accelerations measures (``rolling_avg`` or ``high_pass``)", "``AXY``"
        ``acc_time_window``, "duration in seconds of the rolling window used for filtering dynamic acceleration", "``AXY``"
        ``cutoff_f``, "cutoff frequency in Hz for the Butterworth high-pass filter", "``AXY``"
        ``order``, "order of the Butterworth high-pass filter", "``AXY``"
    """
    
    # init parameters dictionary
    params = {}
    
    # from yml files to a single parameters dictionary
    for config_file_path in config_file_paths:
        with open(config_file_path, "r") as f:
            params.update(yaml.safe_load(f))
    
    return(params)


# ================================================================================================ #
# DICTIONARY OF PLOT PARAMETERS
# ================================================================================================ #
def get_plot_params():
    
    """
    Create a plot parameters dictionary.
        
    :param: None
    :return: a dictionary of plot parameters.
    :rtype: dict 
    
    The dictionary of plot parameters required to produce the diagnostic of ``GPS``, ``TDR`` and ``AXY`` classes. Find below the 
    exhaustive table of parameters within the dictionary.
    
    .. csv-table::  
        :header: "name", "description", "required"
        :widths: 20, 30, 20

        ``cols_1``, "discrete contrasted color palette for trips", "``GPS``, ``AXY``"
        ``cols_2``, "continuous color palette for speed gradient", "``GPS``, ``AXY``"
        ``cols_3``, "continuous color palette for time gradient", "``GPS``, ``AXY``"
        ``main_fs``, "fontsize of the plot title", "``GPS``, ``AXY``, ``TDR``"
        ``labs_fs``, "fontsize of the plot labels", "``GPS``, ``AXY``, ``TDR``"
        ``axis_fs``, "fontsize of the plot axes", "``GPS``, ``AXY``, ``TDR``"
        ``text_fs``, "fontsize of the plot texts", "``GPS``, ``AXY``, ``TDR``"
        ``pnt_size``, "size of the scatter plot points", "``GPS``, ``AXY``, ``TDR``"
        ``eph_size``, "size of the scatter plot emphasized points", "``GPS``, ``AXY``, ``TDR``"
        ``mrk_size``, "size of vplot markers", "``GPS``, ``AXY``, ``TDR``"
        ``pnt_type``, "type of the scatter plot points", "``GPS``, ``AXY``, ``TDR``"
        ``grid_lwd``, "linewidth of the plot background grid", "``GPS``, ``AXY``, ``TDR``"
        ``grid_col``, "line color of the plot background grid", "``GPS``, ``AXY``, ``TDR``"
        ``grid_lty``, "line type of the plot background grid", "``GPS``, ``AXY``, ``TDR``"
        ``night_transp``, "transparency applied to night grey box in timeserie plot", "``GPS``, ``AXY``, ``TDR``"
        ``cb_shrink``, "colorbar shrink factor", "``GPS``, ``AXY``"
        ``cb_pad``, "colorbar padding factor", "``GPS``, ``AXY``"
        ``cb_aspect``, "colorbar size", "``GPS``, ``AXY``"
        ``fig_dpi``, "dots per inch of a saved figure", "``GPS``, ``AXY``, ``TDR``"
        ``lon_fmt``, "longitude formatter", "``GPS``, ``AXY``"
        ``lat_fmt``, "latitude formatter", "``GPS``, ``AXY``"
    """
    
    # colors
    colors = {"cols_1" : np.tile(plt.cm.Set1(range(9)), (1, 1)),
              "cols_2" : plt.cm.viridis(np.linspace(0, 1, 100)),
              "cols_3" : plt.cm.plasma(np.linspace(0, 1, 100))}

    # fontsizes
    fontsizes = {"main_fs" : 9,
                 "labs_fs" : 8,
                 "axis_fs" : 8,
                 "text_fs" : 8}

    # scatter plot
    scatter = {"pnt_size" : 0.25,
               "eph_size" : 1.0,
               "mrk_size" : 8.0,
               "pnt_type" : "o"}

    # grid
    grid = {"grid_lwd" : 0.25,
            "grid_col" : "grey",
            "grid_lty" : "--"}
    
    # transparency
    transp = {"night_transp" : 0.25}

    # colorbar
    colorbar = {"cb_shrink" : 0.8,
                "cb_pad" : 0.05,
                "cb_aspect" : 18}

    # fig
    dpi = {"fig_dpi" : 150}
    
    # formatter
    formatters = {"lon_fmt" : cmpl.LongitudeFormatter(number_format=".2f", dms=False),
                  "lat_fmt" : cmpl.LatitudeFormatter(number_format=".2f", dms=False)}
    
    # append dictionaries
    params = {}
    params.update(colors)
    params.update(fontsizes)
    params.update(scatter)
    params.update(grid)
    params.update(transp)
    params.update(colorbar)
    params.update(dpi)
    params.update(formatters)
    
    return(params)


# ================================================================================================ #
# DICTIONARY OF DATA TYPES FOR DATAFRAME
# ================================================================================================ #
def get_columns_dtypes(column_names):
    
    """
    Extract a dtype dictionary by dataframe column names.
        
    :param column_names: list of column names.
    :type column_names: list[str]
    :return: a dictionary of dtypes by column names.
    :rtype: dict 
    
    The dtypes must be compatible with a dataframe containing NaN values, *i.e* ``Int64`` and ``Float64`` instead of ``int64`` and ``float64``. 
    The full dictionary among which to extract the dictionary is hard-coded.
    """
    
    # define the dictionaries of types by columns
    dtypes_columns_metadata = {"group":"str", "id":"str"}
    dtypes_columns_basic = {"datetime":"object", "step_time":"Float64", "is_night":"Int64"}
    dtypes_columns_gps = {"longitude":"Float64", "latitude":"Float64", "step_length":"Float64", "step_speed":"Float64", "step_heading":"Float64","step_turning_angle":"Float64", 
                          "step_heading_to_colony":"Float64", "is_suspicious":"Int64", "dist_to_nest":"Float64", "trip":"Int64"}
    dtypes_columns_tdr = {"pressure":"Float64", "temperature":"Float64", "depth":"Float64", "dive":"Int64", "zoc":"Float64"}
    dtypes_columns_acc = {"ax":"Float64", "ay":"Float64", "az":"Float64", "ax_f":"Float64", "ay_f":"Float64", "az_f":"Float64","odba":"Float64", "odba_f":"Float64"}
    dtypes_trip_stats = {"trip_id":"str", "length":"float", "duration":"float", "max_hole":"float", "dmax":"float", "n_step":"int"}
    dtypes_dive_stats = {"dive_id":"str", "duration":"float", "max_depth":"float"}
    
    # append dictionaries
    dtypes_columns_dict = {}
    dtypes_columns_dict.update(dtypes_columns_metadata)
    dtypes_columns_dict.update(dtypes_columns_basic)
    dtypes_columns_dict.update(dtypes_columns_gps)
    dtypes_columns_dict.update(dtypes_columns_tdr)
    dtypes_columns_dict.update(dtypes_columns_acc)
    dtypes_columns_dict.update(dtypes_trip_stats)
    dtypes_columns_dict.update(dtypes_dive_stats)
    
    # extract dtypes by columns subdictionary
    dtypes_columns_subdict = {key:dtypes_columns_dict[key] for key in column_names}
    
    return(dtypes_columns_subdict)