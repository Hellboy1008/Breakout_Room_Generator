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
sf.add_color_scale_conditional_formatting(start_type='num', start_value=0, start_color='F8696B',
                                          end_type='num', end_value=3, end_color='63BE7B', mid_type='num', mid_value=0, mid_color='FFEB84')

# add black background for diagonal
for column in df.columns.tolist()[1:]:
    sf.apply_style_by_indexes(sf[sf[column] == 'X'], cols_to_style=[column], styler_obj=Styler(
        bg_color=utils.colors.black, font=utils.fonts.calibri, font_size=11))

# create excel writer and covert to excel
excel_writer = StyleFrame.ExcelWriter('breakout_data.xlsx')
sf.to_excel(excel_writer=excel_writer, sheet_name=event_name)
excel_writer.save()
