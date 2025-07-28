# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import csv
import numpy as np

# ================================================================================================ #
# INPUT  : - filename : complete path of the csv file to be read.
#
# OUTPUT : - sep : determined separator of the csv file among ";", "\t", ",", " ".
# ================================================================================================ #
def derive_separator(filename):

    # list of possible separators
    separators = [";", "\t", ",", " "]

    # read first line
    with open(filename, 'r') as f:
        first_line = f.readline()

    # read as dataframe with all possible separators
    if first_line:
        nb_fields = [0] * len(separators)
        for k, sep in enumerate(separators):
            reader = csv.reader([first_line], delimiter=sep)
            nb_fields[k] = len(next(reader))
        
        sep = separators[nb_fields.index(max(nb_fields))]
    else:
        print("WARNING: %s is empty" % filename)
        sep = ""

    # return the separator with greater number of fields in dataframe
    return(sep)



# ================================================================================================ #
# INPUT  : - strings : array of strings.
#          - pattern : pattern to be found in strings.
#
# OUTPUT : - strings_with_pattern : array of strings that contain the pattern.
# ================================================================================================ #
def grep_pattern(strings, pattern):

    strings_with_pattern = [s for s in strings if pattern in s]

    return(strings_with_pattern)


# ================================================================================================ #
# INPUT  : - n_cols : number of random colors desired.
#
# OUTPUT : - rand_colors : array of n_cols random colors (3 RGB numbers between 0 and 1).
# ================================================================================================ #
def random_colors(n_cols=1):
    rand_colors = np.random.uniform(0,1,(n_cols,3))
    return(rand_colors)


# ================================================================================================ #
# INPUT  : - n_cols : number of random colors desired.
#
# OUTPUT : - rand_colors : array of n_cols random colors (3 RGB numbers between 0 and 1).
# ================================================================================================ #
def rgb_to_hex(rgb_col):
    hex_col = "#{:02x}{:02x}{:02x}".format(int(255*rgb_col[0]),int(255*rgb_col[1]),int(255*rgb_col[2]))
    return(hex_col)

