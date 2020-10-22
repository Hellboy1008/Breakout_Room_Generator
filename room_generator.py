# Created by: 龍ONE
# Date Created: October 1, 2020
# Date Edited: October 23, 2020
# Purpose: Generate breakout rooms for zoom call.

# import counter for finding duplicate tuples
from collections import Counter
# import copy for deepcopy list
import copy
# import random for shuffling list
import random
# import room_assigner file for function
import room_assigner

# create list for people present, and assign value for breakout rooms and event name
start_list = False
people_lst_all = []
present = open('present.txt', 'r')
for line in present:
    if 'Desired number of ppl per room:' in line:
        ppl_per_room = int(
            line[len('Desired number of ppl per room: '):].strip())
    elif 'Event Name:' in line:
        event_name = line[11:].strip()
    elif 'PRESENT:' in line:
        start_list = True
        continue
    if len(line.strip()) != 0 and start_list == True:
        people_lst_all.append(line.strip())

# look for previous groups
search_groups = False
past_groups_lst = []
previous_rooms = open('previous-rooms.txt', 'r')
for line in previous_rooms:
    if 'EVENT: ' + event_name in line and '(Y)' in line:
        search_groups = True
        continue
    if search_groups == True:
        if len(line.strip()) != 0:
            past_groups_lst.append(line.strip().split(','))

# add tuples for past pairs
past_pairs_lst = []
for groups in past_groups_lst:
    for index_one in range(len(groups)):
        for index_two in range(index_one + 1, len(groups)):
            current_pair = (groups[index_one].strip(),
                            groups[index_two].strip())
            past_pairs_lst.append(tuple(sorted(current_pair)))

# sort past pairs to account for duplicate tuples
past_pairs_dict = dict(Counter(pairs for pairs in past_pairs_lst))

# generate master list with all people and their genders
master_list = dict()
master = open('master.txt', 'r')
for line in master:
    if '(M)' in line:
        master_list[line.replace('(M)', '').strip()] = 'M'
    elif '(F)' in line:
        master_list[line.replace('(F)', '').strip()] = 'F'

# separate list of people to male and female
people_lst_m = []
people_lst_f = []
for name in people_lst_all:
    name_str = name.replace('(N)', '').replace('(L)', '').strip()
    if name_str in master_list:
        if master_list[name_str] == 'M':
            people_lst_m.append(name)
        elif master_list[name_str] == 'F':
            people_lst_f.append(name)
    else:
        user_input = ''
        while user_input != 'M' and user_input != 'F':
            user_input = input('Input the gender for: ' +
                               name_str + '\nType M for male, F for female\n')
            if user_input == 'M':
                people_lst_m.append(name)
            elif user_input == 'F':
                people_lst_f.append(name)

# randomize lists
random.shuffle(people_lst_m)
random.shuffle(people_lst_f)

# populate breakout room list
breakout_room = []
num_breakout_rooms = int(len(people_lst_all) / ppl_per_room)
for num in range(num_breakout_rooms):
    breakout_room.append([])

# generate breakout rooms
if len(past_pairs_lst) == 0:
    room_assigner.room_assigner(
        num_breakout_rooms, breakout_room, people_lst_m, people_lst_f, people_lst_all)
else:
    lowest_error_val = -1000000
    temp_breakout_room = copy.deepcopy(breakout_room)
    best_breakout_room = []
    lowest_error_val_lst = []
    for num in range(1000):
        error_val = 0
        error_val_lst = []
        breakout_room = copy.deepcopy(temp_breakout_room)
        random.shuffle(people_lst_m)
        random.shuffle(people_lst_f)
        room_assigner.room_assigner(
            num_breakout_rooms, breakout_room, people_lst_m, people_lst_f, people_lst_all)
        breakout_room = [[name.replace('(N)', '').replace(
            '(L)', '').strip() for name in groups] for groups in breakout_room]
        for groups in breakout_room:
            for key in past_pairs_dict:
                if key[0] in groups and key[1] in groups:
                    if past_pairs_dict[key] == 1:
                        error_val -= 1
                        error_val_lst.append(1)
                    else:
                        error_val -= 5 * (past_pairs_dict[key] - 1)
                        error_val_lst.append(5 * (past_pairs_dict[key] - 1))
        if error_val == 0:
            best_breakout_room = copy.deepcopy(breakout_room)
            break
        if error_val > lowest_error_val:
            lowest_error_val = error_val
            best_breakout_room = copy.deepcopy(breakout_room)
            lowest_error_val_lst = copy.deepcopy(error_val_lst)


# select the best breakout room if applicable
if len(past_pairs_lst) != 0:
    breakout_room = best_breakout_room

# print breakout rooms
b_room_num = 1
for groups in breakout_room:
    print('Breakout Room ' + str(b_room_num) + ': ' +
          ', '.join(groups))
    b_room_num += 1

# print error value if applicable
if len(past_pairs_lst) != 0:
    print('Error Val = ', lowest_error_val)

# print error value list if applicable
if error_val != 0:
    error_val_dict = dict(Counter(values for values in lowest_error_val_lst))
    for value in sorted(error_val_dict.keys()):
        if value == 1:
            print('Number of people that have shared 1 room together before:', error_val_dict[value])
        else:
            print('Number of people that have shared', int(value/5) + 1, 'rooms together before:', error_val_dict[value])
