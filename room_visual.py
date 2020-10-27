# Created by: 龍ONE
# Date Created: October 5, 2020
# Date Edited: October 28, 2020
# Purpose: Import breakout room data to excel file.

# import numpy for numpy arrays
import numpy as np
# import pandas for dataframe
import pandas as pd
# import from styleframe for excel output
from styleframe import StyleFrame, Styler, utils
# import sys for exiting program
import sys

# file for previous rooms
previous_rooms = open('previous-rooms.txt', 'r')

# ask for user input for event name
event_name = input('Enter the event name: ')

# check if event exists in text file
event_exists = False
add_names = False
rooms_lst = []
for line in previous_rooms:
    if 'EVENT: ' + event_name in line and '(Y)' in line:
        event_exists = True
        add_names = True
        event_name = line[6:].replace('(Y)', '').strip()
        continue
    elif 'EVENT: ' + event_name in line and '(N)' in line:
        break
    if event_exists == True:
        if len(line.strip()) != 0:
            rooms_lst.append(line.strip().split(','))

# create tuple for all pairs
tuples_lst = []
for groups in rooms_lst:
    for index_one in range(len(groups)):
        for index_two in range(index_one + 1, len(groups)):
            tuples_lst.append(
                (groups[index_one].strip(), groups[index_two].strip()))

# print error message
if event_exists == False or len(rooms_lst) == 0:
    print('Event was not found or there are no previous breakout rooms for the event.')
    sys.exit()

# create list of people
ppl_lst = []
for groups in rooms_lst:
    for person in groups:
        if person.strip() not in ppl_lst:
            ppl_lst.append(person.strip())
ppl_lst.sort()

# create dataframe
df = pd.DataFrame(0, index=ppl_lst, columns=ppl_lst)

# add pairs to dataframe
for tuple_pair in tuples_lst:
    df[tuple_pair[0]][tuple_pair[1]] += 1
    df[tuple_pair[1]][tuple_pair[0]] += 1

# add x to diagonals
for people in ppl_lst:
    df.loc[people, people] = 'X'

# change index to default integers
df.reset_index(inplace=True)
df = df.rename(columns={'index': ''})

# create np array that holds all values for pairs
pair_value_lst = []
for index, row in df.iterrows():
    for column in df.columns.tolist()[1:]:
        if (row[column] != 'X'):
            pair_value_lst.append(row[column])
pair_value_arr = np.array(pair_value_lst)

# creating styleframe object
sf = StyleFrame(df, styler_obj=Styler(font=utils.fonts.calibri, font_size=11))

# apply formatting such as font, font size, color
sf.apply_headers_style(styler_obj=Styler(
    font=utils.fonts.calibri, font_size=11, bold=True, wrap_text=False))
sf.apply_column_style(df.columns.tolist()[0], styler_obj=Styler(
    font=utils.fonts.calibri, font_size=11, bold=True, wrap_text=False))
sf.set_column_width(df.columns.tolist(), 11)
sf.add_color_scale_conditional_formatting(start_type='num', start_value=np.amin(pair_value_arr), start_color='F8696B',
                                          end_type='num', end_value=np.amax(pair_value_arr), end_color='63BE7B', mid_type='num', mid_value=np.percentile(pair_value_arr, 50), mid_color='FFEB84')

# add black background for diagonal
for column in df.columns.tolist()[1:]:
    sf.apply_style_by_indexes(sf[sf[column] == 'X'], cols_to_style=[column], styler_obj=Styler(
        bg_color=utils.colors.black, font=utils.fonts.calibri, font_size=11))

# create excel writer and covert to excel
excel_writer = StyleFrame.ExcelWriter('breakout_rooms_data.xlsx')
sf.to_excel(excel_writer=excel_writer, sheet_name=event_name)
excel_writer.save()

# create file for statistics
stats_file = open('statistics.txt', 'w+')

# create list of names and how many times they've been to large group
attendance = dict()
for rooms in rooms_lst:
    for name in rooms:
        if name.strip() in attendance.keys():
            attendance[name.strip()] += 1
        else:
            attendance[name.strip()] = 1

# calculate average value for each attendance value
attendance_weighted_avg = []
for index in range(1, max(attendance.values()) + 1):
    attendance_pair_value_lst = []
    for key in attendance.keys():
        if attendance[key] == index:
            attendance_pair_value_lst.extend(df[key].tolist())
    attendance_pair_value_lst = [
        value for value in attendance_pair_value_lst if value != 'X']
    attendance_weighted_avg.append(
        (len(attendance_pair_value_lst) - attendance_pair_value_lst.count(0)) / len(attendance_pair_value_lst))

# write statistics to file
everyone_avg = (len(pair_value_lst) - pair_value_lst.count(0)
                ) / len(pair_value_lst)
other_ppl_count = len(attendance.keys()) - 1
stats_file.write("Average people met by everyone: %d (%.2f%%)" %
                 (other_ppl_count * everyone_avg, everyone_avg * 100))
for index in range(1, max(attendance.values()) + 1):
    if index == 1:
        stats_file.write(
            "\nAverage people met by a person that has been 1 time:  %d (%.2f%%)" % (other_ppl_count * attendance_weighted_avg[0], attendance_weighted_avg[0] * 100))
    else:
        stats_file.write(
            "\nAverage people met by a person that has been %d times: %d (%.2f%%)" % (index, other_ppl_count * attendance_weighted_avg[index - 1], attendance_weighted_avg[index - 1] * 100))

# close statistics file
stats_file.close()
