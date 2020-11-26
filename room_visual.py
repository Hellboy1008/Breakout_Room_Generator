# Created by: 龍ONE
# Date Created: October 5, 2020
# Date Edited: November 26, 2020
# Purpose: Import breakout room data to excel file and create a text file for statistics.

# imports
import room_visual_helpers as helper


def main():
    # ask user for event name
    event_name = input('Enter the event name: ')
    
    # check if event name exists
    helper.checkEventName(event_name)
    
    # generate excel file using breakout room data
    excel_data = helper.generateExcelFile(event_name)
    
    # genereate text file with statistics using breakout room data
    helper.generateStatisticsFile(excel_data[0], excel_data[1], excel_data[2])

# run program
if __name__ == "__main__":
    main()