#######################################
##  Advent of Code 2021              ##
##  Day 5 - Hydrothermal Venture     ##
##  John Forslund                    ##
#######################################

# Imports
import pandas as pd
import numpy as np



######################
##      Part 1      ##
######################

# Load input data:
inputs = pd.read_csv("day_5/input.txt", names=["x1", "y1", "x2", "y2"], index_col=False)

# Only look at horizontal and vertical lines:
allowed_inputs = inputs[(inputs.y1==inputs.y2) | (inputs.x1==inputs.x2)]

# Create a class for the seafloor:
class Seafloor:
    def __init__(self, coords_input):
        # Create a 2d array which counts occurrences of vents, size is largest x and y coordinates:
        self.counts = np.zeros(shape=(coords_input[["x1", "x2"]].max().max()+1, coords_input[["y1", "y2"]].max().max()+1))

    def add_counts(self, coords):
        for n in range(coords.shape[0]):
            self.counts[coords[n][0], coords[n][1]] += 1

    def get_atleast_n_counts(self, n):
        atleast_n_counts = np.where(self.counts >= n)[0].shape[0]
        return atleast_n_counts

# Instantiate seafloor object:
seafloor = Seafloor(allowed_inputs)


def generate_coords(input_coords, seafloor):
    x1, y1, x2, y2 = input_coords.x1, input_coords.y1, input_coords.x2, input_coords.y2
    # For horizontal lines:
    if x1 == x2:
        if y1 > y2:     # Eventually swap start and end y-coordinates so they only increase positively
            y_temp = y1; y1 = y2; y2 = y_temp
        y = np.arange(y1, y2+1, 1)
        x = np.array([x1]*y.shape[0])
        coords = np.insert(y, np.arange(x.shape[0]), x)
        coords = np.reshape(coords, (coords.shape[0]//2, 2))
        seafloor.add_counts(coords)
    # For vertical lines:
    elif y1 == y2:
        if x1 > x2:     # Eventually swap start and end x-coordinates so they only increase positively
            x_temp = x1; x1 = x2; x2 = x_temp
        x = np.arange(x1, x2+1, 1)
        y = np.array([y1]*x.shape[0])
        coords = np.insert(y, np.arange(x.shape[0]), x)
        coords = np.reshape(coords, (coords.shape[0]//2, 2))
        seafloor.add_counts(coords)
    # For diagonal lines:
    else:
        if x1 > x2:
            x = np.flip(np.arange(x2, x1+1, 1))     # Flipped, so arange works (from smallest to largest)
        else:
            x = np.arange(x1, x2+1, 1)
        if y1 > y2:
            y = np.flip(np.arange(y2, y1+1, 1))     # Flipped, so arange works (from smallest to largest)
        else:
            y = np.arange(y1, y2+1, 1)
        coords = np.insert(y, np.arange(x.shape[0]), x)
        coords = np.reshape(coords, (coords.shape[0]//2, 2))
        seafloor.add_counts(coords)


# Generate all possible coords for each start and end coord:
allowed_inputs.apply(generate_coords, axis=1, args=(seafloor,))

# Get nr of points where atleast two lines overlap:
seafloor.get_atleast_n_counts(2)



######################
##      Part 2      ##
######################

# Instantiate seafloor object:
seafloor2 = Seafloor(inputs)

# Generate all possible coords for each start and end coord:
inputs.apply(generate_coords, axis=1, args=(seafloor2,))

# Get nr of points where atleast two lines overlap:
seafloor2.get_atleast_n_counts(2)
