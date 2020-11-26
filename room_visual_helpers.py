# Created by: 龍ONE
# Date Created: November 26, 2020
# Date Edited: November 26, 2020
# Purpose: Contains helper functions for generating visuals for breakout rooms.

# imports
import numpy as np
import pandas as pd
from styleframe import StyleFrame, Styler, utils
import sys


def calculateAvgMet(attendance, df, pair_values_arr):
    # average people met based on attendance
    avg_met = []

    # calculate averages for each attendance value
    for count in range(1, max(attendance.values()) + 1):
        total_met = []
        for key in attendance.keys():
            if attendance[key] == count:
                total_met.extend(df[key].tolist())
        total_met = [val for val in total_met if val != 'X']
        avg_met.append((len(total_met) - total_met.count(0)) / len(total_met))

    return avg_met


def checkEventName(event_name):
    # checks if event exists
    event_exists = False
    # checks if past rooms exist for event
    past_rooms = False

    # open file for previous rooms
    previous_rooms = open('previous-rooms.txt', 'r')

    # read previous-rooms.txt
    for line in previous_rooms:
        if line[:-4].strip() == 'EVENT: ' + event_name:
            event_exists = True
            if 'Y' in line[-4:]:
                past_rooms = True

    # if event doesn't exist or if there are no previous rooms, end program
    if not event_exists:
        print('Event was not found.')
        sys.exit()
    elif not past_rooms:
        print('Event was found but there were no previous rooms.')
        sys.exit()


def generateBreakoutRoomData(event_name):
    # list for all previous pairs
    pairs_lst = []
    # list of all previous participants
    ppl_lst = []
    # open file for previous rooms
    previous_rooms = open('previous-rooms.txt', 'r')
    # when we should start reading names
    read_names = False
    # list of past rooms for the event
    rooms_lst = []

    # read previous-rooms.txt
    for line in previous_rooms:
        if line[:-4].strip() == 'EVENT: ' + event_name:
            read_names = True
            continue
        if 'EVENT' in line:
            break
        if read_names and len(line.strip()) != 0:
            rooms_lst.append(line.strip().split(','))

    # fill list of all pairs
    for groups in rooms_lst:
        for p1 in range(len(groups)):
            for p2 in range(p1 + 1, len(groups)):
                pairs_lst.append((groups[p1].strip(), groups[p2].strip()))

    # get all participants
    for groups in rooms_lst:
        for person in groups:
            if person.strip() not in ppl_lst:
                ppl_lst.append(person.strip())
    ppl_lst.sort()

    return pairs_lst, ppl_lst, rooms_lst


def generateExcelFile(event_name):
    # generate breakout room data for excel file
    breakout_room_data = generateBreakoutRoomData(event_name)

    # generate the dataframe for the excel file
    dataframe_data = generateDataFrame(
        breakout_room_data[0], breakout_room_data[1])
    df = dataframe_data[0]

    # style dataframe data
    sf = styleDataFrame(df, dataframe_data[1])

    # write to excel file
    excel_writer = StyleFrame.ExcelWriter('breakout_rooms_data.xlsx')
    sf.to_excel(excel_writer=excel_writer, sheet_name=event_name)
    excel_writer.save()

    return df, breakout_room_data[2], dataframe_data[1]


def generateDataFrame(pairs_lst, ppl_lst):
    # create dataframe
    df = pd.DataFrame(0, index=ppl_lst, columns=ppl_lst)

    # add pairs to dataframe
    for pair in pairs_lst:
        df[pair[0]][pair[1]] += 1
        df[pair[1]][pair[0]] += 1

    # add x to diagonals
    for people in ppl_lst:
        df.loc[people, people] = 'X'

    # change index to default integers
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': ''})

    # create np array that holds number of times met for all pairs
    pair_values = []
    for index, row in df.iterrows():
        for column in df.columns.tolist()[1:]:
            if (row[column] != 'X'):
                pair_values.append(row[column])
    pair_values_arr = np.array(pair_values)

    return df, pair_values_arr


def generateStatisticsFile(df, rooms_lst, pair_values_arr):
    # total attendance record for each participant
    attendance = dict()
    # average people met based on attendance
    avg_met = []
    # total number of people excluding the person themselves
    total_others = 0

    # create the file statistics.txt
    stats_file = open('statistics.txt', 'w+')

    # create dictionary of names and how many times people have been to the event
    for rooms in rooms_lst:
        for name in rooms:
            name = name.strip()
            if name in attendance.keys():
                attendance[name] += 1
            else:
                attendance[name] = 1

    # calculate average number of people met for each attendance value
    avg_met = calculateAvgMet(attendance, df, pair_values_arr)

    # average people met by all previous participants
    total_avg = (len(pair_values_arr) - np.sum(pair_values_arr == 0)
                 ) / len(pair_values_arr)
    total_others = len(attendance.keys()) - 1
    stats_file.write("Average people met by everyone: %d (%.2f%%)\n" %
                     (total_others * total_avg, total_avg * 100))

    # average people met based on number of attendance
    for index in range(1, max(attendance.values()) + 1):
        if index == 1:
            stats_file.write("Average people met by a person that has been 1 time:  %d (%.2f%%)\n" % (
                total_others * avg_met[0], avg_met[0] * 100))
        else:
            stats_file.write("Average people met by a person that has been %d times: %d (%.2f%%)\n" % (
                index, total_others * avg_met[index - 1], avg_met[index - 1] * 100))

    # close statistics.txt
    stats_file.close()


def styleDataFrame(df, pair_values_arr):
     # styleframe object for excel file
    sf = StyleFrame(df, styler_obj=Styler(
        font=utils.fonts.calibri, font_size=11))

    # apply formatting for excel file
    sf.apply_headers_style(styler_obj=Styler(
        font=utils.fonts.calibri, font_size=11, bold=True, wrap_text=False))
    sf.apply_column_style(df.columns.tolist()[0], styler_obj=Styler(
        font=utils.fonts.calibri, font_size=11, bold=True, wrap_text=False))
    sf.set_column_width(df.columns.tolist(), 11)
    sf.add_color_scale_conditional_formatting(start_type='num', start_value=np.amin(pair_values_arr), start_color='F8696B',
                                              end_type='num', end_value=np.amax(pair_values_arr), end_color='63BE7B', mid_type='num', mid_value=np.percentile(pair_values_arr, 50), mid_color='FFEB84')

    # add black background for diagonal
    for column in df.columns.tolist()[1:]:
        sf.apply_style_by_indexes(sf[sf[column] == 'X'], cols_to_style=[column], styler_obj=Styler(
            bg_color=utils.colors.black, font=utils.fonts.calibri, font_size=11))

    return sf
