#######################################
##  Advent of Code 2021              ##
##  Day 2 - Dive!                    ##
##  John Forslund                    ##
#######################################

# Imports
import pandas as pd
import numpy as np



######################
##      Part 1      ##
######################

# Load input data:
inputs = pd.read_csv("day_2/input.txt", names=["commands"])

# Arrange input into df with diff cols:
inputs = inputs.commands.str.split(" ", expand=True)
inputs = inputs.rename({0: "action", 1: "distance"}, axis=1)
inputs["distance"] = inputs.distance.astype(int)

# Calculate total distance per action (order of actions does not matter):
down_up_sum = inputs[inputs.action == "down"].distance.sum() - inputs[inputs.action == "up"].distance.sum()
forward_sum = inputs[inputs.action == "forward"].distance.sum()

# Calculate position in the end:
x_coord, y_coord = 0, 0     # start position
x_coord += forward_sum
y_coord += down_up_sum

# Multiply x and y coords:
output = x_coord * y_coord



######################
##      Part 2      ##
######################

# Inputs is the same, but changing up to negative values:
inputs["distance"] = inputs.distance.where(inputs.action.isin(["down", "forward"]), -inputs.distance)

# We now have to keep track of aim, and this time order does matter.
inputs["aim"] = inputs[inputs.action.isin(["up", "down"])].distance.cumsum()    # Change aim based on only up/down actions.
inputs["aim"] = inputs["aim"].fillna(method='ffill')        # Forward-fill the NaN values.
inputs["aim"] = inputs["aim"].fillna(0)                     # Fill NaN values with 0, e.g. the first row.

# Starting positions
x_coord2 = 0
y_coord2 = 0

forward_inputs = inputs[inputs.action=="forward"]               # We'll only use forward actions to determine positions.

x_coord2 += forward_inputs.distance.sum()     # Summarize x-coord by simply counting forward distances.
y_coord2 += (forward_inputs.aim * forward_inputs.distance).sum()    # Summarize y-coord by multiplying dist with aim on forward actions.

# Multiply x and y coords:
output2 = x_coord2 * y_coord2

