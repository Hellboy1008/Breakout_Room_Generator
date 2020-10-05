# Created by: 龍ONE
# Date Created: October 1, 2020
# Date Edited: October 6, 2020
# Purpose: Generate breakout rooms for zoom call.

# import copy for deepcopy list
import copy
# import random for shuffling list
import random
# import room_assigner file for function
import room_assigner

# create list for people present, and assign value for breakout rooms and event name
num_new_ppl = 0
people_lst_f = []
people_lst_m = []
present = open('present.txt', 'r')
start_list_f = False
start_list_m = False
for line in present:
    if 'Desired number of ppl per room:' in line:
        ppl_per_room = int(
            line[len('Desired number of ppl per room: '):].strip())
    elif 'Event Name:' in line:
        event_name = line[11:].strip()
    elif 'FEMALES:' in line:
        start_list_f = True
        start_list_m = False
    elif 'MALES:' in line:
        start_list_m = True
    if len(line.strip()) != 0:
        if '(N)' in line.strip() and '**' not in line.strip():
            num_new_ppl += 1
        if start_list_m == True:
            people_lst_m.append(line.strip())
        if start_list_f == True:
            people_lst_f.append(line.strip())

# look for previous groups and add tuples if applicable
groups_lst = []
previous_rooms = open('previous-rooms.txt', 'r')
search_groups = False
tuples_lst = []
for line in previous_rooms:
    if 'EVENT: ' + event_name in line and '(Y)' in line:
        search_groups = True
        continue
    if search_groups == True:
        if 'EVENT: ' in line:
            break
        if len(line.strip()) != 0:
            groups_lst.append(line.strip().split(','))
for groups in groups_lst:
    for index_one in range(len(groups)):
        for index_two in range(index_one + 1, len(groups)):
            tuples_lst.append(
                (groups[index_one].strip(), groups[index_two].strip()))

# create list of all people
people_lst_all = []
people_lst_m = people_lst_m[1:]
people_lst_f = people_lst_f[1:]
people_lst_all.extend(people_lst_m)
people_lst_all.extend(people_lst_f)

# randomize lists
random.shuffle(people_lst_m)
random.shuffle(people_lst_f)

# populate breakout room list
breakout_room = []
num_breakout_rooms = int(len(people_lst_all) / ppl_per_room)
for num in range(num_breakout_rooms):
    breakout_room.append([])

# generate breakout rooms
if len(tuples_lst) == 0:
    room_assigner.room_assigner(
        num_breakout_rooms, breakout_room, people_lst_m, people_lst_f, people_lst_all)
else:
    lowest_error_val = -1000000
    temp_breakout_room = copy.deepcopy(breakout_room)
    best_breakout_room = []
    for num in range(1000):
        error_val = 0
        breakout_room = copy.deepcopy(temp_breakout_room)
        random.shuffle(people_lst_m)
        random.shuffle(people_lst_f)
        room_assigner.room_assigner(
            num_breakout_rooms, breakout_room, people_lst_m, people_lst_f, people_lst_all)
        for groups in breakout_room:
            for tuple_pair in tuples_lst:
                if tuple_pair[0] in groups and tuple_pair[1] in groups:
                    error_val -= 1
        if error_val == 0:
            best_breakout_room = copy.deepcopy(breakout_room)
            break
        if error_val > lowest_error_val:
            lowest_error_val = error_val
            best_breakout_room = copy.deepcopy(breakout_room)

# select the best breakout room if applicable
if len(tuples_lst) != 0:
    breakout_room = best_breakout_room

# print breakout rooms
b_room_num = 1
for groups in breakout_room:
    print(('Breakout Room ' + str(b_room_num) + ': ' +
           ', '.join(groups)).replace(' (N)', ''))
    b_room_num += 1

# print error value if applicable
if len(tuples_lst) != 0:
    print('Error Val = ', error_val)
