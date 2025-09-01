# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import numpy as np
import matplotlib.pyplot as plt
import cartopy.mpl.ticker as cmpl


# ================================================================================================ #
# DICTIONARY OF PARAMETERS
# ================================================================================================ #
def get_params(colony):
    
    """
    Create a parameters dictionary.
    
    :param colony: codified name of the considered colony
    :type colony: str
    :return: a dictionary of parameters
    :rtype: dict
    
    The parameters dictionary is required to construct GPS, TDR and AXY classes. The user-defined colony code allows to define a 
    dictionary of parameters according to a specific dataset. Find below the exhaustive table of parameters within the dictionary.
    
    .. important::
        Users should modify the parameters values according to their dataset and/or add if block with the colony code of their choice. 
    
    .. csv-table::  
        :header: "name", "description", "required"
        :widths: auto

        ``colony``, "name, longitude/latitude center and bounding box inside which the searbird's nest is to be found", "GPS"
        ``local_tz``, "local timezone of the seabird's nest", "GPS, TDR, AXY"
        ``max_possible_speed``, "speed threshold in km/h above which a longitude/latitude measure can be considered as an error and will be deleted", "GPS"
        ``dist_threshold``, "distance from the nest threshold in km above which the seabird is considered in a foraging trip", "GPS"
        ``speed_threshold``, "speed threshold in km/h above which the seabird is still considered in a foraging trip despite being below the distance threshold", "GPS"
        ``nesting_speed``, "local timezone of the seabird's nest", "GPS"
        ``nest_position``, "longitude and latitude of the seabird's nest if known", "GPS"
        ``trip_min_duration``, "duration in seconds above which a trip is valid", "GPS"
        ``trip_max_duration``, "duration in seconds below which a trip is valid", "GPS"
        ``trip_min_length``, "length in km above which a trip is valid", "GPS"
        ``trip_max_length``, "length in km below which a trip is valid", "GPS"
        ``trip_min_steps``, "length in km below which a trip is valid", "GPS"
        ``diving_depth_threshold``, "depth threshold above which a seabird is considered to be diving", "TDR"
        ``dive_min_duration``, "minimum duration in seconds of a dive", "TDR"
        ``odba_p_norm``, "p-norm used for the computation of overall dyanmical body acceleration", "AXY"
        ``filter_type``, "choose type of filter for accelerations measures among (rolling average or high-pass) ", "AXY"
        ``acc_time_window``, "duration in seconds of the rolling window used for filtering dynamic acceleration", "AXY"
        ``cutoff_f``, "cutoff frequency in Hz for the Butterworth high-pass filter", "AXY"
        ``order``, "order of the Butterworth high-pass filter", "AXY"
    """        
    
    # colony parameters 
    # (https://mapscaping.com/bounding-box-calculator/)
    if(colony == "PER_GNP_SUR"): 
        params_colony = {"colony" : {"name" : "PER_GNP_SUR", "center" : [-78.96730, -8.56530], "box_longitude" : [-78.9705, -78.9641], "box_latitude" : [-8.5687, -8.5619]}}
        params_tz = {"local_tz" : "America/Lima"}
    if(colony == "PER_PSC_PSC"): 
        params_colony = {"colony" : {"name" : "PER_PSC_PSC", "center" : [-77.26315, -11.77425], "box_longitude" : [-77.2686, -77.2577], "box_latitude" : [-11.7790, -11.7695]}}
        params_tz = {"local_tz" : "America/Lima"}
    if(colony == "BRA_FDN_MEI"): 
        params_colony = {"colony" : {"name" : "BRA_FDN_MEI", "center" : [-32.39280, -3.81980], "box_longitude" : [-32.3958, -32.3898], "box_latitude" : [-3.8226, -3.8170]}}
        params_tz = {"local_tz" : "America/Noronha"}
    if(colony == "BRA_FDN_CHA"): 
        params_colony = {"colony" : {"name" : "BRA_FDN_CHA", "center" : [-32.42150, -3.87075], "box_longitude" : [-32.4230, -32.4200], "box_latitude" : [-3.8720, -3.8695]}}
        params_tz = {"local_tz" : "America/Noronha"}
    if(colony == "BRA_ABR_SBA"): 
        params_colony = {"colony" : {"name" : "BRA_ABR_SBA", "center" : [-38.69885, -17.96350], "box_longitude" : [-38.7066, -38.6911], "box_latitude" : [-17.9662,-17.9608]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "BRA_ABR_SIR"): 
        params_colony = {"colony" : {"name" : "BRA_ABR_SIR", "center" : [-38.70995, -17.97070], "box_longitude" : [-38.7117, -38.7082], "box_latitude" : [-17.9716,-17.9698]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "BRA_ABR_SUE"): 
        params_colony = {"colony" : {"name" : "BRA_ABR_SUE", "center" : [-38.69880, -17.98060], "box_longitude" : [-38.7016, -38.6960], "box_latitude" : [-17.9822, -17.9790]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "BRA_ABR_RED"): 
        params_colony = {"colony" : {"name" : "BRA_ABR_RED", "center" : [-38.71045, -17.96555], "box_longitude" : [-38.7127, -38.7082], "box_latitude" : [-17.9675,-17.9636]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "BRA_SPS_BEL"): 
        params_colony = {"colony" : {"name" : "BRA_SPS_BEL", "center" : [-29.34570, 0.91670], "box_longitude" : [-29.3462, -29.3452], "box_latitude" : [0.9160, 0.9174]}}
        params_tz = {"local_tz" : "America/Noronha"}
    if(colony == "BRA_SAN_FRA"): 
        params_colony = {"colony" : {"name" : "BRA_SAN_FRA", "center" : [-41.69175, -22.40100], "box_longitude" : [-41.6985, -41.6850], "box_latitude" : [-22.4065, -22.3955]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "CUB_SCA_FBA"): 
        params_colony = {"colony" : {"name" : "CUB_SCA_FBA", "center" : [-78.62310, 22.61165], "box_longitude" : [-78.6253, -78.6209], "box_latitude" : [22.6098, 22.6135]}}   
        params_tz = {"local_tz" : "Cuba"} 
    if(colony == "Zeebrugge"): 
        params_colony = {"colony" : {"name" : "Zeebrugge", "center" : [3.182, 51.341], "box_longitude" : [3.182-0.015, 3.182+0.015], "box_latitude" : [51.341-0.009, 51.341+0.009]}}   
        params_tz = {"local_tz" : "Europe/Paris"} 
    if(colony == "Vlissingen"): 
        params_colony = {"colony" : {"name" : "Vlissingen", "center" : [3.689, 51.450], "box_longitude" : [3.689-0.015, 3.689+0.015], "box_latitude" : [51.450-0.009, 51.450+0.009]}}   
        params_tz = {"local_tz" : "Europe/Paris"} 
    if(colony == "Ostend"): 
        params_colony = {"colony" : {"name" : "Ostend", "center" : [2.931, 51.233], "box_longitude" : [2.931-0.015, 2.931+0.015], "box_latitude" : [51.233-0.009, 51.233+0.009]}}   
        params_tz = {"local_tz" : "Europe/Paris"} 
    
    # cleaning parameters
    params_cleaning = {"max_possible_speed" : 150.0}
    
    # trip segmentation parameters
    params_segmentation = {"dist_threshold" : 2.0,
                           "speed_threshold" : 5.0,
                           "nesting_speed" : 1.0,
                           "nest_position" : None,
                           "trip_min_duration" : 20*60.0,
                           "trip_max_duration" : 14*24*60*60.0,
                           "trip_min_length": 10.0,
                           "trip_max_length": 10000.0,
                           "trip_min_steps": 10}    
    
    # dive segmentation parameters
    params_dives = {"diving_depth_threshold" : -1.0, "dive_min_duration" : 2.0}
    
    # acceleration filtering parameters    
    params_acc = {"filter_type" : "rolling_avg",
                  "odba_p_norm" : 1}
    
    # if rolling average filtering
    if params_acc["filter_type"] == "rolling_avg":
        params_acc_f = {"acc_time_window" : 2.0}
        
    # if high-pass filtering
    if params_acc["filter_type"] == "high_pass":
        params_acc_f = {"cutoff_f" : 0.8,
                        "order" : 4}
    params_acc.update(params_acc_f)
        
    # append dictionaries
    params = {}
    params.update(params_colony)
    params.update(params_tz)
    params.update(params_cleaning)
    params.update(params_segmentation)
    params.update(params_dives)
    params.update(params_acc)
    
    return(params)


# ================================================================================================ #
# DICTIONARY OF DATA TYPES FOR DATAFRAME
# ================================================================================================ #
def get_columns_dtypes(column_names):
    
    """
    Extract a dtype dictionary by dataframe column names.
        
    :param column_names: list of column names.
    :type column_names: list
    :return: a dictionary of dtypes by column names.
    :rtype: dict 
    
    The dtypes must be compatible with a dataframe containing NaN, *i.e* `Int64` and `Float64` instead of `int64` and `float64`. The full dictionary among which to
    extract the dictionary is hard-coded.
    """
    
    # define the dictionaries of types by columns
    dtypes_columns_metadata = {"group":"str", "id":"str"}
    dtypes_columns_basic = {"datetime":"object", "step_time":"Float64", "is_night":"Int64"}
    dtypes_columns_gps = {"longitude":"Float64", "latitude":"Float64", "step_length":"Float64", "step_speed":"Float64", "step_heading":"Float64","step_turning_angle":"Float64", 
                          "step_heading_to_colony":"Float64", "is_suspicious":"Int64", "dist_to_nest":"Float64", "trip":"Int64"}
    dtypes_columns_tdr = {"pressure":"Float64", "temperature":"Float64", "depth":"Float64", "dive":"Int64"}
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


# ================================================================================================ #
# DICTIONARY OF PLOT PARAMETERS
# ================================================================================================ #
def get_plot_params():
    
    """
    Create a plot parameters dictionary.
        
    :param: None
    :return: a dictionary of plot parameters
    :rtype: dict 
    
    The dictionary of plot parameters required to produce the diagnostic of GPS, TDR and AXY classes. Find below the 
    exhaustive table of parameters within the dictionary.
    
    .. csv-table::  
        :header: "name", "description", "required"
        :widths: 20, 30, 20

        ``cols_1``, "discrete contrasted color palette for trips", "GPS, AXY"
        ``cols_2``, "continuous color palette for speed gradient", "GPS, AXY"
        ``cols_3``, "continuous color palette for time gradient", "GPS, AXY"
        ``main_fs``, "fontsize of the plot title", "GPS, TDR, AXY"
        ``labs_fs``, "fontsize of the plot labels", "GPS, TDR, AXY"
        ``axis_fs``, "fontsize of the plot axes", "GPS, TDR, AXY"
        ``text_fs``, "fontsize of the plot texts", "GPS, TDR, AXY"
        ``pnt_size``, "size of the scatter plot points", "GPS, TDR, AXY"
        ``eph_size``, "size of the scatter plot emphasized points", "GPS, TDR, AXY"
        ``mrk_size``, "size of vplot markers", "GPS, TDR, AXY"
        ``pnt_type``, "type of the scatter plot points", "GPS, TDR, AXY"
        ``grid_lwd``, "linewidth of the plot background grid", "GPS, TDR, AXY"
        ``grid_col``, "line color of the plot background grid", "GPS, TDR, AXY"
        ``grid_lty``, "line type of the plot background grid", "GPS, TDR, AXY"
        ``night_transp``, "transparency applied to night grey box in timeserie plot", "GPS, TDR, AXY"
        ``cb_shrink``, "colorbar shrink factor", "GPS, AXY"
        ``cb_pad``, "colorbar padding factor", "GPS, AXY"
        ``cb_aspect``, "colorbar size", "GPS, AXY"
        ``fig_dpi``, "dots per inch of a saved figure", "GPS, TDR, AXY"
        ``lon_fmt``, "longitude formatter", "GPS, AXY"
        ``lat_fmt``, "latitude formatter", "GPS, AXY"
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