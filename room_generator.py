# Created by: 龍ONE
# Date Created: October 1, 2020
# Date Edited: November 26, 2020
# Purpose: Generate zoom breakout rooms with the following conditions:
#          - gender is balanced
#          - if applicable, number of newcomers and leaders per group is balanced
#          - previous breakout rooms are considered -> tries to pair new people together

# imports
import room_generator_helpers as helper


def main():
    # create breakout rooms using algorithm and picks best breakout room after x number of trials
    # recommended number of trials: between 5000-10000
    helper.generateBreakoutRooms(trials=10000)


# run program
if __name__ == "__main__":
    main()
