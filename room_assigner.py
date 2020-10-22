# Created by: 龍ONE
# Date Created: October 1, 2020
# Date Edited: October 23, 2020
# Purpose: Pseudo-randomly assign people to breakout rooms.

# import sys for exiting file
import sys


def room_assigner(num_breakout_rooms, breakout_room, people_lst_m, people_lst_f, people_lst_all):
    # pseudo-randomly assign people to rooms
    ppl_in_room = []
    # assign male leaders to rooms
    room_num_leader_m = 0
    for person in people_lst_m:
        if '(L)' in person:
            breakout_room[room_num_leader_m].append(person)
            ppl_in_room.append(person)
            room_num_leader_m += 1
            if room_num_leader_m > num_breakout_rooms - 1:
                room_num_leader_m = 0
    people_lst_m = [ppl for ppl in people_lst_m if ppl not in ppl_in_room]
    # push all male newcomers to front of list
    newcomers_m = False
    people_lst_m_temp = []
    for person in people_lst_m:
        if ('(N)') in person:
            people_lst_m_temp.append(person)
            newcomers_m = True
    for person in people_lst_m:
        if ('(N)') not in person:
            people_lst_m_temp.append(person)
    if newcomers_m == True:
        people_lst_m = people_lst_m_temp
    # assign rest of males to rooms
    room_num = room_num_leader_m
    for person in people_lst_m:
        breakout_room[room_num].append(person)
        ppl_in_room.append(person)
        room_num += 1
        if room_num > num_breakout_rooms - 1:
            room_num = 0
    people_lst_m = [ppl for ppl in people_lst_m if ppl not in ppl_in_room]
    # assign female leaders to rooms
    leaders_f = False
    room_num_leader_f = room_num_leader_m
    for person in people_lst_f:
        if '(L)' in person:
            breakout_room[room_num_leader_f].append(person)
            ppl_in_room.append(person)
            room_num_leader_f += 1
            if room_num_leader_f > num_breakout_rooms - 1:
                room_num_leader_f = 0
            leaders_f = True
    people_lst_f = [ppl for ppl in people_lst_f if ppl not in ppl_in_room]
    # push all female newcomers to front of list
    newcomers_f = False
    people_lst_f_temp = []
    for person in people_lst_f:
        if ('(N)') in person:
            people_lst_f_temp.append(person)
            newcomers_f = True
    for person in people_lst_f:
        if ('(N)') not in person:
            people_lst_f_temp.append(person)
    if newcomers_f == True:
        people_lst_f = people_lst_f_temp
    # assign rest of females to rooms
    if leaders_f == True:
        room_num = room_num_leader_f
    for person in people_lst_f:
        breakout_room[room_num].append(person)
        ppl_in_room.append(person)
        room_num += 1
        if room_num > num_breakout_rooms - 1:
            room_num = 0
    people_lst_f = [ppl for ppl in people_lst_f if ppl not in ppl_in_room]
    # check if number of people in the room match total list of people
    if len(ppl_in_room) != len(people_lst_all):
        print('SOMETHING WENT WRONG!')
        sys.exit()
