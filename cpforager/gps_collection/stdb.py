# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import pandas as pd
from cpforager import utils, GPS


# ================================================================================================ #
# CONVERT TO SEABIRD TRACKING DATABASE FORMAT [GPS_COLLECTION METHODS]
# ================================================================================================ #
def convert_to_stdb_format(self, metadata):
    
    """    
    Produce the dataframe formatted for Seabird Tracking Database from GPS_collection.
    
    :param self: a GPS_Collection object
    :type self: cpforager.GPS_Collection
    :param metadata: the dataframe with the metadata needed for Seabird Tracking Database.
    :type metadata: pandas.DataFrame.
    :return: the dataframe at the Seabird Tracking Database format.
    :rtype: pandas.DataFrame
    
    The resulting dataframe contains all the position recordings found in the GPS_Collection and its associated metadata 
    (thus duplicated). The correspondance between data and metadata is done using the ``bird_id`` column of the metadata 
    and the ``id`` field of each GPS in the GPS_Collection. Since ``equinox`` and ``argos_quality`` are not relevant for 
    GPS but are for Seabird Tracking, they are set to "NA". See `STDB <https://www.seabirdtracking.org/>`_ for more details 
    about the format.
    
    .. note::
        The required fields in the metadata dataframe are ``bird_id``,``sex``,``age``,``breed_stage``, ``equinox`` and 
        ``argos_quality``. Possible values for these fields are constrained by Seabird Tracking Database.
    """

    # get attributes
    gps_collection = self.gps_collection
    n_gps = self.n_gps
    
    # columns of a seabird tracking csv file
    stdb_columns_dtypes = {"bird_id":"str", "sex":"str", "age":"str", "breed_stage":"str", "track_id":"str", "date_gmt":"str", "time_gmt":"str", "latitude":"float", "longitude":"float", "equinox":"str", "argos_quality":"str"}

    # initialize the overall seabird tracking dataframe
    df_stdb = pd.DataFrame(columns=stdb_columns_dtypes.keys())
    df_stdb = df_stdb.astype(dtype=stdb_columns_dtypes)
    
    # loop over gps in the gps collection
    for k in range(n_gps):
        
        # load individual gps data from the gps collection
        gps = gps_collection[k]
        df = gps.df.copy(deep=True)
        
        # convert datetime from local to utc timezone
        local_timezone = gps.params.get("local_tz")
        df = utils.convert_loc_to_utc(df, local_timezone)
        
        # find row in metadata corresponding to id
        metadata_row = metadata.loc[metadata["bird_id"] == gps.id].reset_index(drop=True)
        
        if(len(metadata_row)>0):
            
            # define new column in dataframe constantly equals to metadata
            df["bird_id"] = metadata_row["bird_id"][0]
            df["sex"] = metadata_row["sex"][0]
            df["age"] = metadata_row["age"][0]
            df["breed_stage"] = metadata_row["breed_stage"][0]
            
            # track_id as a string with leading zeros
            df["track_id"] = df["trip"].apply(lambda x: "%02d" % x)
            
            # reformat UTC datetime
            df["date_gmt"] = df["datetime"].dt.strftime("%d/%m/%Y")
            df["time_gmt"] = df["datetime"].dt.strftime("%H:%M:%S")        
            
            # define to NA the required columns equinox (GLS) and argos_quality (PTT)
            df["equinox"] = "NA"
            df["argos_quality"] = "NA"

            # only select columns of interest
            df = df[stdb_columns_dtypes.keys()]
            
            # concatenate to the overall dataframe
            df_stdb = pd.concat([df_stdb, df]).reset_index(drop=True)
            
        else:
            print("WARNING : GPS id %s not found in metadata" % (gps.id))
        
    return(df_stdb)


# ================================================================================================ #
# CONVERT A SEABIRD TRACKING DATABASE FILE TO GPS_COLLECTION
# ================================================================================================ #
def convert_to_gps_collection(df_stdb, group, params):
    
    """    
    Construct a GPS_Collection object from a Seabird Tracking Database dataframe.
    
    :param self: a dataframe at the Seabird Tracking Database format.
    :type self: pandas.DataFrame
    :param params: the parameters dictionary.
    :type params: dict
    :return: the GPS_Collection object
    :rtype: cpforager.GPS_Collection
    
    See `STDB <https://www.seabirdtracking.org/>`_ for more details about the format.
    """
    
    # get unique identifier
    bird_ids = df_stdb["bird_id"].unique()
    
    # initialize the metadata dataframe
    metadata = pd.DataFrame(columns=["bird_id", "sex", "age", "breed_stage"])
    metadata["bird_id"] = bird_ids
    
    # initialize the gps collection
    gps_collection = []
    
    # loop over bird ids
    for k in range(len(metadata)):
        
        # set bird id
        bird_id = metadata.loc[k, "bird_id"]
        
        # extract dataframe of given bird id
        df = df_stdb.loc[df_stdb["bird_id"]==bird_id].reset_index(drop=True)
        
        # produce "datetime" column of type datetime64
        df["datetime"] = pd.to_datetime(df["date_gmt"] + " " + df["time_gmt"], format="%d/%m/%Y %H:%M:%S")
        df = utils.convert_utc_to_loc(df, params.get("local_tz"))
        
        # construct GPS object
        gps = GPS(df, group, bird_id, params)
        
        # append gps to collection 
        gps_collection.append(gps)
        
        # complete metadata dataframe
        metadata.loc[k, "sex"] = df["sex"].unique()
        metadata.loc[k, "age"] = df["age"].unique()
        metadata.loc[k, "breed_stage"] = df["breed_stage"].unique()
    
    return(gps_collection, metadata)
