# Created by: 龍ONE
# Date Created: October 5, 2020
# Date Edited: May 10, 2021
# Purpose: Import breakout room data to excel file and create a text file for statistics.

# imports
import stats_helpers as helper


def main():
    # generate excel file
    helper.generateExcel()

# run program
if __name__ == "__main__":
    main()