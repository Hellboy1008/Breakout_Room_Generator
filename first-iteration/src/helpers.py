# Created by: 龍ONE
# Date Created: January 25, 2021
# Date Edited: February 9, 2021
# Purpose: Helper functions for generating breakout rooms

# imports
import os
import person
import pplList
import random
import rooms

# global variables
curr_dir = os.getcwd()  # current directory
event_name = ''  # event name
greedy_trials = 5000  # number of trials for greedy algorithm
past_groups = dict()  # contains all previous pairs if past groups exist
ppl_per_room = 0  # desired number of people per room
ppl_present = pplList.pplList()  # list of all participants
ppl_present_f = pplList.pplList()  # list of all female participants
ppl_present_m = pplList.pplList()  # list of all male participants
premade_groups_count = 0  # number of premade groups for event
premade_groups = []  # premade groups for event
sm_trials = 2500  # number of trials for simulated annealing


def createBestBreakoutRooms():
    best_breakout_room = []
    lowest_ev = float('inf')
    # greedy algorithm
    for count in range(greedy_trials):
        print('Applying algorithm 1...', str(count + 1) +
              '/' + str(greedy_trials), end='\r')
        breakout_rooms = rooms.BreakoutRooms(
            past_groups, ppl_per_room, ppl_present, ppl_present_f, ppl_present_m, premade_groups)
        ev = breakout_rooms.errorVal()
        if ev < lowest_ev:
            best_breakout_room = breakout_rooms.copy()
            lowest_ev = ev
        if lowest_ev == 0:
            break
    best_breakout_room.balanceRooms(False)
    print('\nAlgorithm 1 completed')
    # simulated annealing
    for count in range(sm_trials):
        print('Applying algorithm 2...', str(
            count + 1) + '/' + str(sm_trials), end='\r')
        valid_pair = False
        # find a valid pair to switch out
        while not valid_pair:
            if random.randint(0,1) == 0:
                ppl_present_f.randomize()
                p1 = ppl_present_f.list[0]
                p2 = ppl_present_f.list[1]
            else:
                ppl_present_m.randomize()
                p1 = ppl_present_m.list[0]
                p2 = ppl_present_m.list[1]
            if p1.leader == p2.leader and p1.newcomer == p2.newcomer and best_breakout_room.getRoomNum(p1.name) != best_breakout_room.getRoomNum(p2.name):
                valid_pair = True
        temp_rooms = best_breakout_room.copy()
        temp_rooms.swap(p1, p2)
        ev = temp_rooms.errorVal()
        if ev < lowest_ev:
            best_breakout_room = temp_rooms.copy()
            lowest_ev = ev
        if lowest_ev == 0:
            break
    print('\nAlgorithm 2 completed')
    return best_breakout_room


def generateBreakoutRooms():
    # get event details from present.txt
    getEventDetails()
    # get previous groups for the event (if they exist)
    searchPastGroups()
    # separate premade groups if applicable
    if premade_groups_count:
        separatePremadeGroups()
    # fill the gendered lists for participants
    separateGender()
    # creating rooms for event based on whether the event has past groups
    if not past_groups:
        breakout_rooms = rooms.BreakoutRooms(
            past_groups, ppl_per_room, ppl_present, ppl_present_f, ppl_present_m, premade_groups)
    else:
        breakout_rooms = createBestBreakoutRooms()
    # print breakout rooms
    breakout_rooms.printRooms()
    # give user option to edit breakout rooms
    breakout_rooms.editRooms()


def getEventDetails():
    global event_name, ppl_per_room, ppl_present, premade_groups_count

    # read file
    present = open(curr_dir + '/files/present.txt', 'r')
    for line in present:
        line = line.strip()
        if 'Desired number of ppl per room:' in line:
            ppl_per_room = int(line[31:])
        elif 'Event Name:' in line:
            event_name = line[11:].strip()
        elif 'Premade groups:' in line:
            premade_groups_count = int(line[15:])
        elif '**' not in line and 'PRESENT:' not in line and len(line) != 0:
            ppl_present.add(person.Person(line))


def searchPastGroups():
    global past_groups
    num_past_groups = 0  # number of past groups for an event
    past_groups_lst = []  # list containing all past groups for an event
    past_pairs_tuple = []  # list containing all previous pairs for an event as tuples
    prev_groups = False  # true if there were previous groups for an event

    # read file
    previous_rooms = open(curr_dir + '/files/previous-rooms.txt', 'r')
    for line in previous_rooms:
        line = line.strip()
        if event_name in line and '(Y)' in line:
            prev_groups = True
        elif prev_groups and 'EVENT:' in line:
            break
        elif prev_groups and len(line) != 0:
            line += ',' + str(num_past_groups)
            past_groups_lst.append(line.split(','))
        elif prev_groups:
            num_past_groups += 1

    # run only if there were previous groups
    if prev_groups:
        # create list with all previous pairs as tuples
        for groups in past_groups_lst:
            for p1 in range(len(groups) - 1):
                for p2 in range(p1 + 1, len(groups) - 1):
                    pair = groups[p1].strip(), groups[p2].strip(), groups[-1]
                    past_pairs_tuple.append(tuple(sorted(pair)))
        # create dictionary with counts for each previous pair
        for pair in past_pairs_tuple:
            ppl = (pair[1], pair[2])
            if ppl not in past_groups:
                past_groups[ppl] = int(pair[0]) * (1.0 / num_past_groups)
            else:
                past_groups[ppl] += 10
                past_groups[ppl] = int(past_groups[ppl])
                past_groups[ppl] += int(pair[0]) * (1.0 / num_past_groups)


def separatePremadeGroups():
    global ppl_present, premade_groups

    # move people with premade groups to list
    for count in range(premade_groups_count):
        premade_groups.append(pplList.pplList())
        for person in ppl_present.list:
            if person.group == (count + 1):
                premade_groups[count].add(person)

    # remove people with premade groups from participants
    for room in premade_groups:
        for person in room.list:
            ppl_present.remove(person.name)


def separateGender():
    global ppl_present_m, ppl_present_f

    # make separate lists for each gender
    for person in ppl_present.list:
        if person.gender == 'M':
            ppl_present_m.add(person)
        else:
            ppl_present_f.add(person)
