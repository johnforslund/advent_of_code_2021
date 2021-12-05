#######################################
##  Advent of Code 2021              ##
##  Day 3 - Binary Diagnostic        ##
##  John Forslund                    ##
#######################################

# Imports
import pandas as pd
import numpy as np



######################
##      Part 1      ##
######################

# Load input data:
inputs = pd.read_csv("day_3/input.txt", names=["diag"], dtype=str)

# Format into separate columns:
inputs = pd.DataFrame(data=[list(c) for c in list(inputs.diag)])
inputs = inputs.astype(int)

# Find the gamma rate (most common bit in each column):
def common_bits(a, inverse):
    if inverse==False:
        bits = a.sum().apply(lambda x: 1 if x >= a.shape[0]/2 else 0).astype(str).tolist()  # most common bits as list of strings
    else:
        bits = a.sum().apply(lambda x: 1 if x < a.shape[0]/2 else 0).astype(str).tolist()  # most uncommon bits as list of strings
    bits = ''.join(bits)    # as one string
    return bits    
    
gamma_bits = common_bits(inputs, False)
epsilon_bits = common_bits(inputs, True)

gamma_decimal = int(gamma_bits, 2)  # convert to decimal, the 2 is to indicate it is binary
epsilon_decimal = int(epsilon_bits, 2)

power_cons = gamma_decimal * epsilon_decimal



######################
##      Part 2      ##
######################

# Same input, but start with only considering the first bit.

# Find oxygen generator rating:
inputs_to_check = inputs.copy()
for c in inputs.columns:    # for loop through every column of bits
    if inputs_to_check.shape[0] == 1:   # break if only one row left (the result)
        break
    common_bit = 1 if inputs_to_check[c].sum() >= (inputs_to_check.shape[0] / 2) else 0      # most common bit in the column
    inputs_to_check = inputs_to_check[inputs_to_check[c] == common_bit]             # only keep rows where the column contains most common bit
oxygen_generator_bits = "".join(inputs_to_check.astype(str).values.tolist()[0])
oxygen_generator_decimal = int(oxygen_generator_bits, 2)


# Find CO2 scrubber rating:
inputs_to_check = inputs.copy()
for c in inputs.columns:    # for loop through every column of bits
    if inputs_to_check.shape[0] == 1:   # break if only one row left (the result)
        break
    uncommon_bit = 0 if inputs_to_check[c].sum() >= (inputs_to_check.shape[0] / 2) else 1      # most common bit in the column
    inputs_to_check = inputs_to_check[inputs_to_check[c] == uncommon_bit]             # only keep rows where the column contains most common bit
CO2_scrubber_bits = "".join(inputs_to_check.astype(str).values.tolist()[0])
CO2_scrubber_decimal = int(CO2_scrubber_bits, 2)


life_support = oxygen_generator_decimal * CO2_scrubber_decimal