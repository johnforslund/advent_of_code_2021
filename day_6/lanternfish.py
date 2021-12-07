#######################################
##  Advent of Code 2021              ##
##  Day 6 - Lanternfish              ##
##  John Forslund                    ##
#######################################

# Imports
import pandas as pd
import numpy as np



######################
##      Part 1      ##
######################

# Load input data:
inputs = pd.read_csv("day_6/input.txt", names=["timer"], index_col=False)
school = np.array(inputs.timer)

max_timer = 6       # Every fish reproduces every x days (counting 0)
added_timer = 2     # Every new fish requires y extra days
days = 80           # Days to calculate nr of fish

nr_of_fish = np.zeros(days+1)
nr_of_fish[0] = school.shape[0]

print("Initial state:", school, "-", nr_of_fish[0], "fish in total.")
school = school-1
nr_of_fish[1] = school.shape[0]
print("After 1 day:", school, "-", nr_of_fish[1], "fish in total.")
for i in range(2, (days+1)):
    new_fish = 0
    school = school-1
    reproducing_fish = np.where(school < 0)[0].shape[0]
    if reproducing_fish > 0:
        new_fish = np.full(reproducing_fish, max_timer + added_timer)
        school = np.append(school, new_fish)
        school = np.where(school < 0, max_timer, school)
    nr_of_fish[i] = school.shape[0]
    print("After", i, "days:", school, "-", nr_of_fish[i], "fish in total.")



##################################
##      Part 2 - Attempt 1      ##
##################################
"""
days = 256
# Run same for loop as above.
# However, this causes a timeout.
"""


##################################
##      Part 2 - Attempt 2      ##
##################################


"""
days = 256           # Days to calculate nr of fish

# With days = 256, its no longer feasible to do above for-loop due to memory usage.
# Instead, we keep track of the school and its fish with classes, which are able to go up to 5 days at a time, instead of 1 day.

max_timer = 6       # Every fish reproduces every x days (counting 0)
added_timer = 2     # Every new fish requires y extra days

class Fish:
    def __init__(self, start_timer):
        self.timer = start_timer
    
    def decrease_timer(self, days):
        self.timer -= days
        if self.timer < 0:
            self.timer = self.timer + (max_timer+1)
            return (self.timer + added_timer)
        return
"""
"""
class School:
    def __init__(self, initial_timers):
        self.day = 0
        self.nr_fishes = 0
        self.fishes = []
        self.new_fishes(initial_timers)
        
    def new_fishes(self, start_timers):
        new_fishes = []
        for start_timer in start_timers:
            fish = Fish(start_timer)
            new_fishes.append(fish)
        self.fishes.extend(new_fishes)
        self.nr_fishes += len(new_fishes)
        return fish

    def days_passed(self, nr_days):
        new_spawn_timers = []
        for fish in self.fishes:
            potential_spawn_timer = fish.decrease_timer(nr_days)
            if potential_spawn_timer:
                #print("new fish")
                new_spawn_timers.append(potential_spawn_timer)
        self.new_fishes(new_spawn_timers)
        self.day += nr_days
"""
"""
initial_timers = inputs.timer.tolist()
school = School(initial_timers)

school.day
school.nr_fishes

day = school.day
while day != days:
    school.days_passed(4)
    day = school.day

school.day
school.nr_fishes
"""
# This times out as well, most likely due to the every-growing list school.fishes that keep getting appended.
# We need to find a solution without this list-issue.



##################################
##      Part 2 - Attempt 3      ##
##################################


# This solution does not utilize classes, and no array that keeps track of timers each day.
# Instead it focuses on NEW spawns, and uses an array to keep track of only how many new fish are created each day.
# It does this by calculating how often a fish creates a new spawn.
# It starts from day 0, and then for-loops through each day.

# Simple example:
# fish 1                has a new spawn at day 2, 9, 16, 23, etc... i.e. the starting 2 days for fish 1 to reach negative, then every 7 days.
# spawn 1 of fish 1     has a new spawn at day 11, 18, 23, etc...   i.e. the starting 2 days for spawn 1 to reach negative + the starting 2 days for fish 1 to reach negative, then every 7 days.
# etc...

max_timer = 6       # Every fish reproduces every x days (counting 0)
added_timer = 2     # Every new fish requires y extra days
days = 256           # Days to calculate nr of fish

print("Initial state:", inputs.timer.values)

new_fish = np.zeros(shape=(days + 1))       # Array that keeps track of newly added fish per day.
new_fish[0] = inputs.timer.values.shape[0]  # Starts by filling day 0 with the initial starting fish.

print("Day 0:", int(new_fish[0]), "fish in total.")

# For every initial fish, map out where they create a NEW spawn (i.e. not counting spawns of spawns):
for fish_timer in inputs.timer.values:
    #first_spawn_day = fish_timer+1          # Day when the fish gets its first spawn (i.e. goes "below" 0)
    n = fish_timer + 1
    first_spawn_day = [n]
    n += max_timer + 1
    while n <= days:
        first_spawn_day.append(n)
        n += max_timer + 1
    new_fish[first_spawn_day] += 1

# For each day, create a NEW spawn of the first-spawns mapped out from above for-loop:
for day in range(1, days + 1 - max_timer):
    if new_fish[day] == 0:
        pass
    else:
        n = day + max_timer + added_timer + 1
        first_spawn_day = [n]
        if n > days:
            pass
        else:
            n += max_timer + 1
            while n <= days:
                first_spawn_day.append(n)
                n += max_timer + 1
            new_fish[first_spawn_day] += new_fish[day]

# Summarize total number of new fish each day:
total_fish = new_fish.sum()
print("Day " + str(days) + ":", int(total_fish), "fish in total.")

# Runtime is a couple of seconds.