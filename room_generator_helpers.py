# Created by: 龍ONE
# Date Created: November 25, 2020
# Date Edited: December 2, 2020
# Purpose: Contains helper functions for generating breakout rooms.

# imports
import copy
import random
import sys


def addExtraPerson(breakout_rooms, master_lst, past_groups):
    # new breakout rooms
    new_breakout_room = []

    # ask name for new person
    new_person_name = input(
        'Enter the name of the new person you would like to add.\n')
    new_person_name = new_person_name.strip()

    # check if person already exists in breakout room
    for group in breakout_rooms:
        for person in group:
            if new_person_name == person.replace('(N)', '').replace('(L)', '').strip():
                print('This person is already in a room!\n')
                return new_breakout_room

    # ask if new person is a leader or newcomer
    new_person_status = input(
        'Is this person a leader or newcomer? Type L for leader, N for newcomer, any other key if neither.\n')
    new_person_status = new_person_status.lower().strip()

    # ask for new person's gender if they are not in the master list
    if new_person_name not in master_lst.keys():
        # ask user for the person's gender
        gender = ''
        while gender != 'M' and gender != 'F':
            gender = input(
                'Input the gender for this person. Type M for male, F for female\n')
        # add to master list
        if gender == 'M':
            master_lst[new_person_name] = 'M'
        else:
            master_lst[new_person_name] = 'F'

    # add leader or newcomer status if applicable
    if new_person_status == 'l':
        new_person_name += ' (L)'
    elif new_person_status == 'n':
        new_person_name += ' (N)'

    # find best new breakout room
    new_breakout_room = bestNewBreakoutRoom(
        'add', breakout_rooms, master_lst, new_person_name, past_groups)

    return new_breakout_room


def bestBreakoutRoom(past_groups, ppl_lst_f, ppl_lst_m, ppl_per_room, trials):
    # best breakout room
    best_breakout_rooms = []
    # lowest error val
    lowest_error_val = float('inf')
    # list for lowest error val
    lowest_error_val_lst = []
    # temporary list for breakout room
    temp_breakout_rooms = []

    # run the trials
    count = 0
    while count < trials:
        random.shuffle(ppl_lst_f)
        random.shuffle(ppl_lst_m)
        temp_breakout_rooms = roomAssigner(ppl_lst_f, ppl_lst_m, ppl_per_room)
        error_val = calculateErrorVal(temp_breakout_rooms, past_groups)
        # check if error value is lower than current lowest error value
        if error_val[0] < lowest_error_val:
            lowest_error_val = error_val[0]
            lowest_error_val_lst = error_val[1]
            best_breakout_rooms = copy.deepcopy(temp_breakout_rooms)
        # if error value is 0, end trials
        if lowest_error_val == 0:
            break
        count += 1

    return best_breakout_rooms, lowest_error_val, lowest_error_val_lst


def bestNewBreakoutRoom(action, breakout_rooms, master_lst, person, past_groups):
    # lowest error value for new rooms
    lowest_error_val = float('inf')
    # new breakout rooms
    new_breakout_rooms = []
    # temp breakout rooms 1 for simulations
    temp_breakout_rooms_1 = []
    # temp breakout rooms 2 for simulations
    temp_breakout_rooms_2 = []

    # check if we're adding or removing a person
    if action == 'add':
        # generate all possible breakout rooms with placing new person and moving at most 1 person
        for room_num_i in range(len(breakout_rooms)):
            temp_breakout_rooms_1 = copy.deepcopy(breakout_rooms)
            temp_breakout_rooms_1[room_num_i].append(person)
            for existing_person in breakout_rooms[room_num_i]:
                temp_breakout_rooms_2 = copy.deepcopy(temp_breakout_rooms_1)
                temp_breakout_rooms_2[room_num_i].remove(existing_person)
                for room_num_j in range(len(breakout_rooms)):
                    temp_breakout_rooms_2[room_num_j].append(existing_person)
                    error_val = calculateWeightedErrorVal(
                        temp_breakout_rooms_2, master_lst, past_groups)
                    # update new breakout rooms and error value if the room is ideal
                    if error_val < lowest_error_val:
                        lowest_error_val = error_val
                        new_breakout_rooms = copy.deepcopy(
                            temp_breakout_rooms_2)
                    temp_breakout_rooms_2[room_num_j].remove(existing_person)
    elif action == 'remove':
        temp_breakout_rooms_1 = copy.deepcopy(breakout_rooms)
        # remove person from breakout rooms
        for room_num in range(len(temp_breakout_rooms_1)):
            for person_i in temp_breakout_rooms_1[room_num]:
                if person_i.replace('(L)', '').replace('(N)', '').strip() == person:
                    temp_breakout_rooms_1[room_num].remove(person_i)
        # generate all possible breakout rooms by moving at most 1 person
        for room_num_i in range(len(temp_breakout_rooms_1)):
            for existing_person in temp_breakout_rooms_1[room_num_i]:
                temp_breakout_rooms_2 = copy.deepcopy(temp_breakout_rooms_1)
                temp_breakout_rooms_2[room_num_i].remove(existing_person)
                for room_num_j in range(len(temp_breakout_rooms_1)):
                    temp_breakout_rooms_2[room_num_j].append(existing_person)
                    error_val = calculateWeightedErrorVal(
                        temp_breakout_rooms_2, master_lst, past_groups)
                    # update new breakout rooms and error value if the room is ideal
                    if error_val < lowest_error_val:
                        lowest_error_val = error_val
                        new_breakout_rooms = copy.deepcopy(
                            temp_breakout_rooms_2)
                    temp_breakout_rooms_2[room_num_j].remove(existing_person)

    return new_breakout_rooms


def calculateErrorVal(breakout_rooms, past_groups):
    # error value for breakout room
    error_val = 0
    # list of all the error values
    error_val_lst = []

    # trim names with '(L)' or '(N)'
    breakout_rooms = [[name.replace('(N)', '').replace(
        '(L)', '').strip() for name in group] for group in breakout_rooms]

    # calculate error value using past groups
    for groups in breakout_rooms:
        for key in past_groups:
            if key[0] in groups and key[1] in groups:
                error_val += past_groups[key]
                error_val_lst.append(past_groups[key])

    return error_val, error_val_lst


def calculateWeightedErrorVal(breakout_rooms, master_lst, past_groups):
    # error value without considering room size, gender, status
    error_val = calculateErrorVal(breakout_rooms, past_groups)[0]

    # check room size and update error value
    largest_room_size = 0
    smallest_room_size = float('inf')
    for group in breakout_rooms:
        if len(group) < smallest_room_size:
            smallest_room_size = len(group)
        if len(group) > largest_room_size:
            largest_room_size = len(group)
    if largest_room_size - smallest_room_size >= 2:
        error_val += 10000 * (largest_room_size - smallest_room_size)

    # check gender balance in each group
    for group in breakout_rooms:
        num_males = 0
        num_females = 0
        for person in group:
            person = person.replace('(L)', '').replace('(N)', '').strip()
            if master_lst[person] == 'M':
                num_males += 1
            else:
                num_females += 1
        if abs(num_males - num_females) == 1:
            error_val += 1000
        elif abs(num_males - num_females) != 0:
            error_val += 3000 * abs(num_males - num_females)

    # check balance of leaders/newcomers in each group
    largest_leader_num = 0
    largest_newcomer_num = 0
    smallest_leader_num = float('inf')
    smallest_newcomer_num = float('inf')
    for group in breakout_rooms:
        leader_num = 0
        newcomer_num = 0
        for person in group:
            if '(L)' in person:
                leader_num += 1
            elif '(N)' in person:
                newcomer_num += 1
        # update smallest and largest values
        if leader_num > largest_leader_num:
            largest_leader_num = leader_num
        if leader_num < smallest_leader_num:
            smallest_leader_num = leader_num
        if newcomer_num > largest_newcomer_num:
            largest_newcomer_num = newcomer_num
        if newcomer_num < smallest_newcomer_num:
            smallest_newcomer_num = newcomer_num
    if largest_leader_num - smallest_leader_num >= 2:
        error_val += 5000
    if largest_newcomer_num - smallest_newcomer_num >= 2:
        error_val += 5000

    return error_val


def editingRooms(breakout_rooms, master_lst, past_groups=None):
    # previous breakout rooms
    prev_breakout_rooms = []
    # new breakout rooms
    new_breakout_rooms = []
    # option chosen by user
    user_option = 1

    # run while user wants to edit rooms
    while True:
        user_option = input(
            '\nWhat would you like to do? Enter the number that applies.\n1. Adding a new person\n2. Removing an existing person\n3. Undo previous edit\n')
        # check if user wants to edit rooms
        if user_option != '1' and user_option != '2' and user_option != '3':
            break

        # run respective functions
        if user_option == '1':
            new_breakout_rooms = addExtraPerson(
                breakout_rooms, master_lst, past_groups)
            if len(new_breakout_rooms) != 0:
                prev_breakout_rooms.append(breakout_rooms)
        elif user_option == '2':
            new_breakout_rooms = removeExistingPerson(breakout_rooms, master_lst, past_groups)
            if len(new_breakout_rooms) != 0:
                prev_breakout_rooms.append(breakout_rooms)
        else:
            if prev_breakout_rooms == []:
                print('There were no previous rooms!\n')
                continue
            else:
                new_breakout_rooms = copy.deepcopy(prev_breakout_rooms[-1])
                prev_breakout_rooms.pop()

        # check if user actually made new breakout rooms
        if len(new_breakout_rooms) == 0:
            continue
        
        # print the rooms that changed
        changed_rooms = []
        for room_num in range(len(breakout_rooms)):
            if breakout_rooms[room_num] != new_breakout_rooms[room_num]:
                changed_rooms.append(room_num + 1)
        print('Rooms that changed:', changed_rooms)

        # print new breakout rooms
        errorValCalc = calculateErrorVal(new_breakout_rooms, past_groups)
        printBreakoutRooms(new_breakout_rooms, True,
                           errorValCalc[0], errorValCalc[1])
        breakout_rooms = copy.deepcopy(new_breakout_rooms)


def generateBreakoutRooms(trials):
    # tuple of event details from present.txt
    event_details = getEventDetails()

    # tuple of previous groups details for the event
    past_groups = searchPastGroups(event_details[0])

    # tuple containing the list of participants separated by gender
    ppl_lst_gendered = separateGender(event_details[1])

    # check if there were previous groups and print rooms
    if not past_groups[1]:
        breakout_rooms = roomAssigner(
            ppl_lst_gendered[0], ppl_lst_gendered[1], event_details[2])
        printBreakoutRooms(breakout_rooms, past_groups[1])
    else:
        print('Generating breakout rooms...')
        breakout_rooms = bestBreakoutRoom(
            past_groups[0], ppl_lst_gendered[0], ppl_lst_gendered[1], event_details[2], trials)
        printBreakoutRooms(
            breakout_rooms[0], past_groups[1], breakout_rooms[1], breakout_rooms[2])

    # option for editing breakout rooms
    edit_rooms = input(
        '\nWould you like the option to edit breakout rooms? Enter Y if yes, any other key if no.\n')
    if edit_rooms.lower() == 'y':
        if past_groups[1]:
            editingRooms(breakout_rooms[0],
                         ppl_lst_gendered[2], past_groups[0])
        else:
            editingRooms(breakout_rooms, ppl_lst_gendered[2])


def getEventDetails():
    # event name
    event_name = ''
    # list of people present
    ppl_lst_all = []
    # desired number of people per room
    ppl_per_room = 0

    # read present.txt
    present = open('present.txt', 'r')
    for line in present:
        line = line.strip()
        if 'Desired number of ppl per room:' in line:
            ppl_per_room = int(line[31:])
        elif 'Event Name:' in line:
            event_name = line[11:].strip()
        elif '**' not in line and 'PRESENT:' not in line and len(line) != 0:
            ppl_lst_all.append(line)

    return event_name, ppl_lst_all, ppl_per_room


def placeInRoom(breakout_rooms, ppl_lst, room_num, identifier=''):
    # people that have been added to rooms
    ppl_added = []

    # place people in rooms
    for person in ppl_lst:
        if identifier == '(L)' and identifier not in person:
            continue
        breakout_rooms[room_num].append(person)
        ppl_added.append(person)
        room_num += 1
        # point back to first breakout room if needed
        if room_num > len(breakout_rooms) - 1:
            room_num = 0

    # remove people that have been assigned from list
    ppl_lst = [ppl for ppl in ppl_lst if ppl not in ppl_added]

    return room_num, ppl_lst


def printBreakoutRooms(breakout_rooms, past_groups, error_val=0, error_val_lst=[]):
    # breakout room number
    breakout_room_num = 1

    # trim names with '(L)' or '(N)'
    breakout_rooms = [[name.replace('(N)', '').replace(
        '(L)', '').strip() for name in group] for group in breakout_rooms]

    # print breakout rooms
    print()
    for room in breakout_rooms:
        print('Breakout Room', str(breakout_room_num) + ':', ', '.join(room))
        breakout_room_num += 1

    # print error value if there were past groups
    if past_groups:
        print('Error Value = %.2f' % error_val)
        printErrorValueDetails(error_val_lst)


def printErrorValueDetails(error_val_lst):
    # number of most recent shared room in the past for all recurring pairs
    recent_shared_room = 0
    # number of shared rooms in the past per recurring pair
    shared_rooms = dict()

    # convert error values to find out how many times a pair has met in the past
    error_val_lst.sort()
    for index, error_val in enumerate(error_val_lst):
        if error_val == int(error_val):
            recent_shared_room += 1
        error_val_lst[index] = 10 * round(error_val / 10)

    # fill shared rooms dictionary with count values
    for error_val in error_val_lst:
        if error_val not in shared_rooms.keys():
            shared_rooms[error_val] = 1
        else:
            shared_rooms[error_val] += 1

    # print number of shared rooms in the past
    for shared_room_num in sorted(shared_rooms.keys()):
        if shared_room_num == 0:
            print('Number of pairs that have shared 1 room together before:',
                  shared_rooms[shared_room_num])
        else:
            print('Number of pairs that have shared',
                  int(shared_room_num / 10) + 1, 'rooms together before:', shared_rooms[shared_room_num])

    # print number of most recent shared rooms
    print('Number of pairs who shared a room in the previous meeting:',
          recent_shared_room)


def pushNewcomers(ppl_lst):
    # push newcomers to start of list
    for index in range(len(ppl_lst)):
        if '(N)' in ppl_lst[index]:
            ppl_lst = [ppl_lst[index]] + \
                ppl_lst[:index] + ppl_lst[index + 1:]

    return ppl_lst


def removeExistingPerson(breakout_rooms, master_lst, past_groups):
    # new breakout rooms
    new_breakout_room = []

    # ask name for person to remove
    person_remove_name = input(
        'Enter the name of the new person you would like to remove.\n')
    person_remove_name = person_remove_name.strip()

    # check if person exists in breakout room
    person_exists = False
    for group in breakout_rooms:
        for person in group:
            if person_remove_name == person.replace('(N)', '').replace('(L)', '').strip():
                person_exists = True
    if not person_exists:
        print('This person does not exist in the breakout rooms!\n')
        return new_breakout_room

    # find best new breakout room
    new_breakout_room = bestNewBreakoutRoom(
        'remove', breakout_rooms, master_lst, person_remove_name, past_groups)

    return new_breakout_room


def roomAssigner(ppl_lst_f, ppl_lst_m, ppl_per_room):
    # list representing breakout rooms
    breakout_rooms = []
    # number of breakout rooms
    num_breakout_rooms = int((len(ppl_lst_m) + len(ppl_lst_f)) / ppl_per_room)
    # tracks room number for males
    room_num_m = 0
    # tracks room number for females
    room_num_f = -1

    # initialize breakout room list
    breakout_rooms = [[] for room in range(num_breakout_rooms)]

    # assign male leaders to rooms
    room_details = placeInRoom(breakout_rooms, ppl_lst_m, room_num_m, '(L)')
    room_num_m = room_details[0]
    ppl_lst_m = room_details[1]

    # assign female leaders to rooms
    room_details = placeInRoom(breakout_rooms, ppl_lst_f, room_num_m, '(L)')
    room_num_f = room_details[0]
    ppl_lst_f = room_details[1]

    # push male newcomers to front of list
    ppl_lst_m = pushNewcomers(ppl_lst_m)

    # assign remaining males to rooms
    room_details = placeInRoom(breakout_rooms, ppl_lst_m, room_num_m)
    room_num_m = room_details[0]
    ppl_lst_m = room_details[1]

    # push female newcomers to front of list
    ppl_lst_f = pushNewcomers(ppl_lst_f)

    # assign remaining females to room
    if room_num_f == -1:
        room_num_f = room_num_m
    ppl_lst_f = placeInRoom(breakout_rooms, ppl_lst_f, room_num_f)[1]

    # check that all participants have been assigned
    if len(ppl_lst_m) != 0 or len(ppl_lst_f) != 0:
        print("Something went wrong with the program! Not all participants were assigned to a breakout room")
        sys.exit()

    return breakout_rooms


def searchPastGroups(event_name):
    # true if there were previous groups for an event
    prev_groups = False
    # list containing all past groups for an event
    past_groups = []
    # dictionary containing all previous pairs with count for each pair
    past_groups_dict = dict()
    # list containing all previous pairs for an event as tuples
    past_pairs_tuple = []
    # number of past groups for an event
    num_past_groups = 0

    # read previous-rooms.txt
    previous_rooms = open('previous-rooms.txt', 'r')
    for line in previous_rooms:
        line = line.strip()
        if event_name in line and '(Y)' in line:
            prev_groups = True
        elif prev_groups and 'EVENT:' in line:
            break
        elif prev_groups and len(line) != 0:
            line += ',' + str(num_past_groups)
            past_groups.append(line.split(','))
        elif prev_groups and len(line) == 0:
            num_past_groups += 1

    # run only if there were previous groups
    if prev_groups:
        # create list with all previous pairs as tuples
        for groups in past_groups:
            for p1 in range(len(groups) - 1):
                for p2 in range(p1 + 1, len(groups) - 1):
                    pair = (groups[p1].strip(), groups[p2].strip(), groups[-1])
                    past_pairs_tuple.append(tuple(sorted(pair)))

        # create dictionary with counts for each previous pair
        for pair in past_pairs_tuple:
            ppl = (pair[1], pair[2])
            if ppl not in past_groups_dict:
                past_groups_dict[ppl] = int(pair[0]) * (1.0 / num_past_groups)
            else:
                past_groups_dict[ppl] += 10
                past_groups_dict[ppl] = int(past_groups_dict[ppl])
                past_groups_dict[ppl] += int(pair[0]) * (1.0 / num_past_groups)

    return past_groups_dict, prev_groups


def separateGender(ppl_lst_all):
    # master list with all expected participants and their genders
    master_lst = dict()
    # list of all female participants
    ppl_lst_f = []
    # list of all male participants
    ppl_lst_m = []

    # generate master list from master.txt
    master = open('master.txt', 'r')
    for line in master:
        line = line.strip()
        if '(F)' in line:
            master_lst[line[:-3].strip()] = 'F'
        else:
            master_lst[line[:-3].strip()] = 'M'

    # make separate lists for each gender
    for name in ppl_lst_all:
        name_str = name.replace('(N)', '').replace('(L)', '').strip()
        if name_str in master_lst and master_lst[name_str] == 'M':
            ppl_lst_m.append(name)
        elif name_str in master_lst:
            ppl_lst_f.append(name)
        else:
            # ask user for the person's gender
            gender = ''
            while gender != 'M' and gender != 'F':
                gender = input('Input the gender for: ' +
                               name_str + '\nType M for male, F for female\n')
            if gender == 'M':
                ppl_lst_m.append(name)
                master_lst[name] = 'M'
            else:
                ppl_lst_f.append(name)
                master_lst[name] = 'F'

    # randomize lists
    random.shuffle(ppl_lst_m)
    random.shuffle(ppl_lst_f)

    return ppl_lst_f, ppl_lst_m, master_lst
