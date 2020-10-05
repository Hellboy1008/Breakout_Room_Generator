# Created by: 龍ONE
# Date Created: October 1, 2020
# Date Edited: October 5, 2020
# Purpose: Pseudo-randomly assign people to breakout rooms.

import sys

def room_assigner(num_breakout_rooms, breakout_room, people_lst_m, people_lst_f, people_lst_all):
    ppl_in_room = []
    # assign guys to rooms
    room_num_newcomer_m = 0
    for person in people_lst_m:
        if '(N)' in person:
            breakout_room[room_num_newcomer_m].append(person)
            ppl_in_room.append(person)
            room_num_newcomer_m += 1
            if room_num_newcomer_m > num_breakout_rooms - 1:
                room_num_newcomer_m = 0
    people_lst_m = [ppl for ppl in people_lst_m if ppl not in ppl_in_room]
    room_num = room_num_newcomer_m
    for person in people_lst_m:
        breakout_room[room_num].append(person)
        ppl_in_room.append(person)
        room_num += 1
        if room_num > num_breakout_rooms - 1:
            room_num = 0
    # assign girls to rooms
    room_num_newcomer_f = room_num_newcomer_m
    for person in people_lst_f:
        if '(N)' in person:
            breakout_room[room_num_newcomer_f].append(person)
            ppl_in_room.append(person)
            room_num_newcomer_f += 1
            if room_num_newcomer_f > num_breakout_rooms - 1:
                room_num_newcomer_f = 0
    people_lst_f = [ppl for ppl in people_lst_f if ppl not in ppl_in_room]
    room_num = room_num_newcomer_f
    for person in people_lst_f:
        breakout_room[room_num].append(person)
        ppl_in_room.append(person)
        room_num += 1
        if room_num > num_breakout_rooms - 1:
            room_num = 0
    if len(ppl_in_room) != len(people_lst_all):
        print('SOMETHING WENT WRONG!')
        sys.exit()