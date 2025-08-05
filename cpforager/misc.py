# ================================================================================================ #
# LIBRARIES
# ================================================================================================ #
import csv
import numpy as np


# ================================================================================================ #
# DERIVE SEPARATOR FROM CSV
# ================================================================================================ #
def derive_separator(file_path):
    
    """    
    :param file_path: complete path of the csv file to be read.
    :type file_path: str
    :return: the determined separator of the csv file.
    :rtype: str 
    
    Return the determined separator of the csv file among the following list ``[";", "\\t", ",", " "]`` by testing the first line.
    """

    # list of possible separators
    separators = [";", "\t", ",", " "]

    # read first line
    with open(file_path, 'r') as f:
        first_line = f.readline()

    # read as dataframe with all possible separators
    if first_line:
        nb_fields = [0] * len(separators)
        for k, sep in enumerate(separators):
            reader = csv.reader([first_line], delimiter=sep)
            nb_fields[k] = len(next(reader))
        
        sep = separators[nb_fields.index(max(nb_fields))]
    else:
        print("WARNING: %s is empty" % file_path)
        sep = ""

    # return the separator with greater number of fields in dataframe
    return(sep)


# ================================================================================================ #
# GREP PATTERN
# ================================================================================================ #
def grep_pattern(strings, pattern):
    
    """    
    :param strings: array of strings.
    :type strings: array(str)
    :param pattern: pattern to be found in strings.
    :type pattern: str
    :return: the array of strings that contain the pattern.
    :rtype: array(str) 
    
    Return the array of strings that contain the pattern. Useful to sort file names.
    """

    strings_with_pattern = [s for s in strings if pattern in s]

    return(strings_with_pattern)


# ================================================================================================ #
# RANDOM COLORS
# ================================================================================================ #
def random_colors(n_cols=1):
    
    """    
    :param n_cols: number of random colors desired.
    :type n_cols: int
    :return: the array of n_cols random colors.
    :rtype: array(array(float)) 
    
    Return the array of size (n_cols,3) composed of n_cols random colors defined by 3 RGB numbers between 0 and 1.
    """
    
    rand_colors = np.random.uniform(0,1,(n_cols,3))
    
    return(rand_colors)


# ================================================================================================ #
# RGB TO HEX
# ================================================================================================ #
def rgb_to_hex(rgb_col):
    
    """    
    :param rgb_col: RGB color array
    :type rgb_col: array(float)
    :return: the hexadecimal code of the RGB color
    :rtype: str
    
    Return the hexadecimal code of the RGB color.
    """
    
    hex_col = "#{:02x}{:02x}{:02x}".format(int(255*rgb_col[0]),int(255*rgb_col[1]),int(255*rgb_col[2]))
    
    return(hex_col)

