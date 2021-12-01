#######################################
##  Advent of Code 2021              ##
##  Day 1 - Count Increasing Depths  ##
##  John Forslund                    ##
#######################################

# Imports
import pandas as pd
import numpy as np



######################
##      Part 1      ##
######################

# Load input data:
inputs = pd.read_csv("day_1/input.txt", names=["depth"])


# Check which measurements increased :
def rolling_window(input_array, window):
    """
    Function needed to efficiently create rolling windows.

    input_array : numpy array to be windowed.
    window : size of the rolling windows.
    """
    shape = input_array.shape[:-1] + (input_array.shape[-1] - window + 1, window)
    strides = input_array.strides + (input_array.strides[-1],)
    return np.lib.stride_tricks.as_strided(input_array, shape=shape, strides=strides)

n = 1       # compare with the measurement before
x = np.concatenate([[np.nan] * (n), inputs["depth"].values])    # adding a nan before first (special case)
rolling_array = rolling_window(x, n + 1)                        # the input array divided into rolling windows
inputs["increased"] = rolling_array.argmax(axis=1)              # "increased" column is int indicating increased or not (1 or 0)


# Count increased measurements in total:
total_increasing = inputs["increased"].sum()

print(total_increasing)
# Answer is 1154 total increased measurements.


######################
##      Part 2      ##
######################

# Rolling windowing in order to calculate sum:
n_rolling = 2       # compare with the 2 measurements before
x_rolling = np.concatenate([[np.nan] * (n_rolling), inputs["depth"].values])    # adding 2 nan values before first (special case)
rolling_array2 = rolling_window(x_rolling, n_rolling + 1)                        # the input array divided into rolling windows

# Create a pandas DataFrame with new rolling inputs:
rolling_inputs = pd.DataFrame(data=rolling_array2, columns=["rolling_depth_0", "rolling_depth_1", "rolling_depth_2"])
rolling_inputs["depth_sum"] = rolling_inputs.sum(axis=1, skipna=False)

# Check which rolling measurements increased:
n_rolling2 = 1      # compare with the measurement sum before
x_rolling2 = np.concatenate([[np.nan] * (n_rolling2), rolling_inputs["depth_sum"].values])    # adding nan value before first (special case)
rolling_array3 = rolling_window(x_rolling2, n_rolling2 + 1)                        # the input array divided into rolling windows
rolling_inputs["increased"] = rolling_array3.argmax(axis=1)                     # "increased" column is int indicating increased or not (1 or 0)

# Count increased rolling measurements in total:
total_rolling_increasing = rolling_inputs["increased"].sum()

print(total_rolling_increasing)
# Answer is 1127 total increased rolling measurements.