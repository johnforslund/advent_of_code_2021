#######################################
##  Advent of Code 2021              ##
##  Day 7 - The Treachery of Whales  ##
##  John Forslund                    ##
#######################################

# Imports
import pandas as pd
import numpy as np



######################
##      Part 1      ##
######################

# Load input data:
inputs = pd.read_csv("day_7/test_input.txt", names=["positions"], index_col=False)


# Create dataframe that ranges from all possible positions, and specifies number of crabs currently at each position:
all_positions = pd.DataFrame(data=range(inputs.positions.min(), inputs.positions.max()+1), columns=["position"])
all_positions["crabs"] = inputs.positions.value_counts().astype(int)
all_positions["crabs"] = all_positions.crabs.fillna(0).astype(int)

# Calculate total fuel needed for all crabs to converge on one position:
all_positions["fuel_cost"] = np.nan     # Create column for it

# We can calculate the fuel cost for only the most likely positions, based on quartiles:
lower_quartile = int(np.floor(inputs.describe().loc["25%"]))
upper_quartile = int(np.ceil(inputs.describe().loc["75%"]))
likely_positions = range(lower_quartile, upper_quartile + 1)

for pos in likely_positions:
#for pos in all_positions.position:     # to calc ALL positions' fuel costs.
    all_positions.loc[all_positions.position==pos, "fuel_cost"] = all_positions[all_positions.crabs != 0].apply(lambda x: abs(x.position - pos) * x.crabs, axis=1).sum()

# Takes roughly 5 seconds to calculate only the likely positions,
# and about 15 seconds to calculate all positions.

# Most efficient position (& fuel cost) to converge at:
most_efficient_fuel_cost = all_positions.fuel_cost.min()
most_efficient_pos = int(all_positions[all_positions.fuel_cost == most_efficient_fuel_cost].position)

# Fun fact: it appears to always be the median position.



######################
##      Part 2      ##
######################

# Fuel cost is now increasing with 1 for each step, i.e. move 1 position costs 1 fuel, 2 costs 1+2, 3 costs 1+2+3, 4 costs 1+2+3+4 etc.

# The new fuel cost formula is whats called triangular numbers in mathematics:
def triangular_numbers(n):
    number = 0
    for i in range(0, int(n+1)):
        number += i
    return number

for pos in likely_positions:
#for pos in all_positions.position:     # to calc ALL positions' fuel costs.
    all_positions.loc[all_positions.position==pos, "fuel_cost"] = all_positions[all_positions.crabs != 0].apply(lambda x: triangular_numbers(abs(x.position - pos)) * x.crabs, axis=1).sum()

# Most efficient position (& fuel cost) to converge at:
most_efficient_fuel_cost = all_positions.fuel_cost.min()
most_efficient_pos = int(all_positions[all_positions.fuel_cost == most_efficient_fuel_cost].position)

# Roughly 10 seconds to calculate all likely positions' fuel costs.
# Roughly 40 seconds to calculate all positions' fuel costs.

# Fun fact: is it now always the integer closest to the mean position?
