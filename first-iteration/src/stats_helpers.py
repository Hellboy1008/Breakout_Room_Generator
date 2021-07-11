# Created by: 龍ONE
# Date Created: November 26, 2020
# Date Edited: May 10, 2021
# Purpose: Contains helper functions for generating visuals for breakout rooms.

# imports
import numpy as np
import os
import pandas as pd
import sys

# global variables
curr_dir = os.getcwd()  # current directory
event_name = ''  # name of the event
longest_name = 0  # longest name in the list of participants
past_groups = []  # past groups for the event
past_pairs = []  # past pairs for the event


def checkEventName():
    global past_groups, past_pairs
    event_exists = False  # checks if event exists
    past_rooms = False  # checks if past rooms exist for event
    group_num = 0  # the number of past groups

    # check file with previous rooms
    previous_rooms = open(curr_dir + '/files/previous-rooms.txt', 'r')
    for line in previous_rooms:
        line = line.strip()
        if line[:-4] == 'EVENT: ' + event_name:
            event_exists = True
            if 'Y' in line[-4:]:
                past_rooms = True
                continue
        if past_rooms and 'EVENT' in line:
            break
        elif past_rooms and len(line) != 0:
            past_groups.append(line.split(', '))
        elif past_rooms and len(line) == 0:
            past_groups.append(group_num)
            group_num += 1

    # if event doesn't exist or if there are no previous rooms, end program
    if not event_exists or not past_rooms:
        print('Event was not found or event was found but there were no previous rooms.')
        sys.exit()

    # create list of all previous pairs
    for group in past_groups:
        if type(group) is not int:
            for p1 in range(len(group)):
                for p2 in range(p1 + 1, len(group)):
                    past_pairs.append((group[p1], group[p2]))


def generateDataFrame():
    global longest_name
    # get a list of participants
    ppl = []
    for group in past_groups:
        if type(group) is not int:
            for person in group:
                if person not in ppl:
                    ppl.append(person)
    ppl = sorted(ppl)

    # create and fill dataframe
    df = pd.DataFrame(0, index=ppl, columns=ppl)
    for pairs in past_pairs:
        df[pairs[0]][pairs[1]] += 1
        df[pairs[1]][pairs[0]] += 1

    # set diagonals to -1
    for person in ppl:
        df.loc[person, person] = 'X'

    # get longest name in people list
    longest_name = max([len(x) for x in ppl])

    return df


def generateExcel():
    global event_name
    # get name of the event
    event_name = input('Enter the event name: ')
    # check if event exists and find past groups if applicable
    checkEventName()
    # generate data frame for past groups
    df = generateDataFrame()
    # write data to excel
    writer = pd.ExcelWriter(
        curr_dir + './files/breakout_rooms_data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=event_name)

    # format excel
    workbook = writer.book
    worksheet = writer.sheets[event_name]
    excel_format = workbook.add_format({'align': 'center'})
    black_fill = workbook.add_format({'bg_color': '#000000'})
    worksheet.conditional_format('A1:XFD1048576', {'type': '3_color_scale'})
    worksheet.conditional_format('A1:XFD1048576', {
                                 'type': 'cell', 'criteria': 'equal to', 'value': '"X"', 'format': black_fill})
    worksheet.set_column('A1:XFD1048576', None, excel_format)
    worksheet.set_column('A1:XFD1048576', longest_name)

    # save and export excel
    writer.save()
