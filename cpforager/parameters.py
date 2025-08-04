# ======================================================= #
# LIBRARIES
# ======================================================= #
import numpy as np
import matplotlib.pyplot as plt
import cartopy.mpl.ticker as cmpl


# ======================================================= #
# DICTIONARY OF PARAMETERS
# ======================================================= #
"""
.. py:function:: get_params(colony)

   Return a dictionary of parameters needed for GPS, TDR and AXY classes.
   
   The dictionary is composed of the following fields : 
   +----------------------------+---------------------------------------------------------------+
   | name                       | description
   +----------------------------+---------------------------------------------------------------+
    `colony`                    | longitude/latitude bounding box inside which the searbird's nest is to be found. 
    `local_tz`                  | local timezone of the seabird's nest.
    `max_possible_speed`        | speed threshold in km/h above which a longitude/latitude measure can be considered as an error and will be deleted.
    `dist_threshold`            | distance from the nest threshold in km above which the seabird is considered in a foraging trip.
    `speed_threshold`           | speed threshold in km/h above which the seabird is still considered in a foraging trip despite being below the distance threshold.
    `nesting_speed`             | speed threshold in km/h below which the seabird is considered at nest.
    `trip_min_duration`         | duration in seconds above which a trip is valid.
    `trip_max_duration`         | duration in seconds below which a trip is valid.
    `trip_min_length`           | length in km above which a trip is valid.
    `trip_max_length`           | length in km below which a trip is valid.
    `trip_min_steps`            | number of steps above which a trip is valid.
    `diving_depth_threshold`    | set the depth threshold above which a seabird is considered to be diving.
    `dive_min_duration`         | set the minimum duration in seconds of a dive for the considered seabird.
   +----------------------------+---------------------------------------------------------------+

   :colony: codified name of the considered colony.
   :type kind: str
   :return: The dictionary of parameters.
   :rtype: dict
"""        

def get_params(colony):
    
    # colony parameters 
    # (https://mapscaping.com/bounding-box-calculator/)
    if(colony == "PER_GNP_SUR"): 
        params_colony = {"colony" : {"center" : [-78.96730, -8.56530], "box_longitude" : [-78.9705, -78.9641], "box_latitude" : [-8.5687, -8.5619]}}
        params_tz = {"local_tz" : "America/Lima"}
    if(colony == "PER_PSC_PSC"): 
        params_colony = {"colony" : {"center" : [-77.26315, -11.77425], "box_longitude" : [-77.2686, -77.2577], "box_latitude" : [-11.7790, -11.7695]}}
        params_tz = {"local_tz" : "America/Lima"}
    if(colony == "BRA_FDN_MEI"): 
        params_colony = {"colony" : {"center" : [-32.39280, -3.81980], "box_longitude" : [-32.3958, -32.3898], "box_latitude" : [-3.8226, -3.8170]}}
        params_tz = {"local_tz" : "America/Noronha"}
    if(colony == "BRA_FDN_CHA"): 
        params_colony = {"colony" : {"center" : [-32.42150, -3.87075], "box_longitude" : [-32.4230, -32.4200], "box_latitude" : [-3.8720, -3.8695]}}
        params_tz = {"local_tz" : "America/Noronha"}
    if(colony == "BRA_ABR_SBA"): 
        params_colony = {"colony" : {"center" : [-38.69885, -17.96350], "box_longitude" : [-38.7066, -38.6911], "box_latitude" : [-17.9662,-17.9608]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "BRA_ABR_SIR"): 
        params_colony = {"colony" : {"center" : [-38.70995, -17.97070], "box_longitude" : [-38.7117, -38.7082], "box_latitude" : [-17.9716,-17.9698]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "BRA_ABR_SUE"): 
        params_colony = {"colony" : {"center" : [-38.69880, -17.98060], "box_longitude" : [-38.7016, -38.6960], "box_latitude" : [-17.9822, -17.9790]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "BRA_ABR_RED"): 
        params_colony = {"colony" : {"center" : [-38.71045, -17.96555], "box_longitude" : [-38.7127, -38.7082], "box_latitude" : [-17.9675,-17.9636]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "BRA_SPS_BEL"): 
        params_colony = {"colony" : {"center" : [-29.34570, 0.91670], "box_longitude" : [-29.3462, -29.3452], "box_latitude" : [0.9160, 0.9174]}}
        params_tz = {"local_tz" : "America/Noronha"}
    if(colony == "BRA_SAN_FRA"): 
        params_colony = {"colony" : {"center" : [-41.69175, -22.40100], "box_longitude" : [-41.6985, -41.6850], "box_latitude" : [-22.4065, -22.3955]}}
        params_tz = {"local_tz" : "America/Bahia"}
    if(colony == "CUB_SCA_FBA"): 
        params_colony = {"colony" : {"center" : [-78.62310, 22.61165], "box_longitude" : [-78.6253, -78.6209], "box_latitude" : [22.6098, 22.6135]}}   
        params_tz = {"local_tz" : "Cuba"} 
    if(colony == "CUB_SCA_FBA"): 
        params_colony = {"colony" : {"center" : [-78.62310, 22.61165], "box_longitude" : [-78.6253, -78.6209], "box_latitude" : [22.6098, 22.6135]}}   
        params_tz = {"local_tz" : "Cuba"} 
    if(colony == "Zeebrugge"): 
        params_colony = {"colony" : {"center" : [3.182, 51.341], "box_longitude" : [3.182-0.015, 3.182+0.015], "box_latitude" : [51.341-0.009, 51.341+0.009]}}   
        params_tz = {"local_tz" : "Europe/Paris"} 
    if(colony == "Vlissingen"): 
        params_colony = {"colony" : {"center" : [3.689, 51.450], "box_longitude" : [3.689-0.015, 3.689+0.015], "box_latitude" : [51.450-0.009, 51.450+0.009]}}   
        params_tz = {"local_tz" : "Europe/Paris"} 
    if(colony == "Ostend"): 
        params_colony = {"colony" : {"center" : [2.931, 51.233], "box_longitude" : [2.931-0.015, 2.931+0.015], "box_latitude" : [51.233-0.009, 51.233+0.009]}}   
        params_tz = {"local_tz" : "Europe/Paris"} 
    
    # cleaning parameters
    params_cleaning = {"max_possible_speed" : 150}
    
    # trip segmentation parameters
    params_segmentation = {"dist_threshold" : 2,
                           "speed_threshold" : 5,
                           "nesting_speed" : 1,
                           "trip_min_duration" : 20*60,
                           "trip_max_duration" : 14*24*60*60,
                           "trip_min_length": 10,
                           "trip_max_length": 10000,
                           "trip_min_steps": 10}    
    
    # dives parameters    
    params_dives = {"diving_depth_threshold" : 2, "dive_min_duration" : 2}
    
    # append dictionaries
    params = {}
    params.update(params_colony)
    params.update(params_tz)
    params.update(params_cleaning)
    params.update(params_segmentation)
    params.update(params_dives)
    
    return(params)


# ======================================================= #
# DICTIONARY OF PLOT PARAMETERS
# ======================================================= #
def get_plot_params():
        
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