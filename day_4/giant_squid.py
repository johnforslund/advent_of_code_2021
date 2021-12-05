#######################################
##  Advent of Code 2021              ##
##  Day 4 - Giant Squid              ##
##  John Forslund                    ##
#######################################

# Imports
import pandas as pd
import numpy as np



######################
##      Part 1      ##
######################

# Load input data:
bingo_numbers = pd.read_csv("day_4/bingo_numbers.txt").numbers
boards = pd.read_csv("day_4/input.txt", names=[0], index_col=False)

# Format into separate columns, and removing clutter/NaN:
boards = boards.dropna()            # remove NaN
boards = boards[0].str.split(" ")   # split into lists

for i in range(boards.shape[0]):    # remove empty strings
    boards.iloc[i] = [x for x in boards.iloc[i] if x]

boards = boards.reset_index(drop=True)       # reset index after dropping NaN rows
boards2 = pd.DataFrame(data=boards.values.split(), columns=[0,1,2,3,4])

boards = pd.DataFrame(data=[list(c) for c in list(boards)])     # sort them into columns
boards = boards.astype(int)

# Format into separate boards:
boards = boards.values      # converting to numpy array for easier handling
boards = boards.reshape((int(boards.shape[0]/boards.shape[1]), 5, 5))
# We now have 100 boards with 5 rows and 5 columns.

# Set up interface for game, and classes for boards etc:

class BingoBoard:
    def __init__(self, numbers):
        self.numbers = numbers
        self.win = False
        self.points = 0
        self.last_chosen_number = None
        # create chosen_numbers binary array:
        self.chosen_numbers = np.zeros((numbers.shape))
    
    def is_number_chosen(self, chosen_number):
        if chosen_number in self.numbers:
            self.last_chosen_number = chosen_number
            self.chosen_numbers[np.where(self.numbers==chosen_number)] = 1

    def five_in_a_row(self):
        if ((self.chosen_numbers.sum(axis=0) == 5).any() | (self.chosen_numbers.sum(axis=1) == 5).any()):
            self.win = True
            self.points = self.calculate_points()
            print("WINNER!")
            print("Board:")
            print("---------")
            print(self.numbers)
            print("---------")
            print("Chosen numbers:")
            print("---------")
            print(self.chosen_numbers)
            print("---------")
            print("Total points:")
            print(self.points)
            return True
        return False
    
    def calculate_points(self):
        unmarked_points = self.numbers[self.chosen_numbers == 0].sum()
        total_points = unmarked_points * self.last_chosen_number
        return total_points


class BingoSubsystem:
    def __init__(self, boards, bingo_numbers):
        # Create board classes:
        self.bingo_numbers = bingo_numbers      # pre-selected bingo numbers
        self.number = 0
        self.boards = []
        for b in boards:
            self.boards.append(BingoBoard(b))
        self.gameover = False
        self.boards_won = 0

    def choose_next_number(self):
        print("Round", self.number, "-", self.bingo_numbers[self.number], "was drawn!")
        for b in self.boards:
            b.is_number_chosen(self.bingo_numbers[self.number])
        self.check_winning_boards()
        self.number += 1

    def check_winning_boards(self):
        winning_board = False
        for b in self.boards:
            if b.win == False:
                winning_board = b.five_in_a_row()
                if winning_board:
                    self.boards_won += 1
                    self.gameover = True
                    print("Game over! We have a winner!")
                    winning_board = False
        else:
            pass

# Set up a game of bingo:
bingo = BingoSubsystem(boards, bingo_numbers)

# Play the first round:
bingo.choose_next_number()

# Continue playing until there is a winner:
while bingo.gameover == False:
    bingo.choose_next_number()


######################
##      Part 2      ##
######################

# Set up a new game of bingo:
bingo2 = BingoSubsystem(boards, bingo_numbers)

# Play the first round:
bingo2.choose_next_number()

# Continue playing untill all boards have won:
while bingo2.boards_won < len(bingo2.boards):
    bingo2.choose_next_number()
