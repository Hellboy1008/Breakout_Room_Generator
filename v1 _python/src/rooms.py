# Created by: 龍ONE
# Date Created: January 25, 2021
# Date Edited: February 9, 2021
# Purpose: BreakoutRooms object used for the collective breakout rooms.

# imports
import copy
import person
import pplList
import random


class BreakoutRooms:
    def __init__(self, past_groups, ppl_per_room, ppl_present, ppl_present_f, ppl_present_m, premade_groups=None):
        # assign past groups
        self.past_groups = past_groups
        # premade groups count
        if not premade_groups:
            self.premade_groups_count = 0
        else:
            self.premade_groups_count = len(premade_groups)
        # create empty rooms
        self.rooms = [pplList.pplList() for room in range(
            int(len(ppl_present.list) / ppl_per_room) + self.premade_groups_count)]
        self.ppl_per_room = ppl_per_room
        self.ppl_present = ppl_present
        # add premade groups
        if premade_groups:
            for index, rooms in enumerate(premade_groups):
                self.rooms[-1 * (index + 1)] = rooms
                self.rooms[-1 * (index + 1)].premade = True
        # fill rooms
        self.fillRooms(ppl_present_f, ppl_present_m)

    def addPerson(self, person):
        # the case for no past groups
        if not self.past_groups:
            room_num = random.randint(
                0, len(self.rooms) - 1 - self.premade_groups_count)
            while len(self.rooms[room_num].list) != self.ppl_per_room:
                room_num = random.randint(
                    0, len(self.rooms) - 1 - self.premade_groups_count)
            self.rooms[room_num].add(person)
            self.ppl_present.add(person)
            # tell user which room the person was added to
            print(person, 'was added to Room', room_num + 1)
        else:
            room_sizes = self.getRoomSizes()
            best_room = -1
            temp_rooms = self.copy()
            lowest_ev = float('inf')
            for index, room in enumerate(temp_rooms.rooms):
                if room_sizes[index] > self.ppl_per_room:
                    continue
                temp_rooms.rooms[index].add(person)
                ev = temp_rooms.errorVal()
                if ev < lowest_ev:
                    best_room = index
                    lowest_ev = ev
            self.rooms[best_room].add(person)
            self.ppl_present.add(person)
            # tell user which room the person was added to
            print(person, 'was added to Room', best_room + 1)

        # print new rooms
        self.printRooms()

    def balanceRooms(self, output):
        # check for unbalanced rooms
        room_sizes = self.getRoomSizes()
        while (self.ppl_per_room + 1) in room_sizes and (self.ppl_per_room - 1) in room_sizes:
            # fill list of potential people to move
            move_lst = []
            for index, room in enumerate(self.rooms):
                if len(room.list) == self.ppl_per_room + 1:
                    for person in room.list:
                        if not person.leader and not person.newcomer:
                            move_lst.append((index, person))
            # get list of rooms that need people
            fill_room = []
            for index, room in enumerate(self.rooms):
                if len(room.list) == self.ppl_per_room - 1 and not room.premade:
                    fill_room.append(index)
            # move people to room
            self.moveToRooms(fill_room, move_lst, output)
            room_sizes = self.getRoomSizes()

    def copy(self):
        return copy.deepcopy(self)

    def editRooms(self):
        # ask user if they would like to edit rooms
        print('Would you like the option to edit this breakout room?')
        user_response = ''
        while user_response.lower() != 'y' and user_response.lower() != 'n':
            user_response = input('Enter Y for yes, N for no\n')
        # if user doesn't want to edit rooms, end program
        if user_response.lower() == 'n':
            return
        # give user options for editing rooms
        user_response = ''
        while user_response != '3':
            user_response = input(
                'Enter one of the following numbers to edit rooms:\n1. Add new person\n2. Remove existing person\n3. End program\n')
            # get name of person
            if user_response == '1' or user_response == '2':
                name = input('Enter the name of the person\n')
            # add or remove person to rooms
            if user_response == '1':
                name = person.Person(name)
                self.addPerson(name)
            elif user_response == '2':
                self.removePerson(name)

    def errorVal(self):
        # check if there were past groups
        if not self.past_groups:
            return 0.0
        # check if there are premade groups
        if self.premade_groups_count != 0:
            rooms = self.rooms[:-1 * self.premade_groups_count]
        else:
            rooms = self.rooms
        # calculate error val
        ev = 0.0
        self.old_pairs = 0
        self.total_pairs = 0
        for room in rooms:
            for p1 in range(len(room.list)):
                for p2 in range(p1 + 1, len(room.list)):
                    if (room.list[p1].name, room.list[p2].name) in self.past_groups:
                        ev += self.past_groups[(room.list[p1].name,
                                                room.list[p2].name)]
                        self.old_pairs += 1
                    elif (room.list[p2].name, room.list[p1].name) in self.past_groups:
                        ev += self.past_groups[(room.list[p2].name,
                                                room.list[p1].name)]
                        self.old_pairs += 1
                    self.total_pairs += 1
        ev *= (1 - (1 - self.old_pairs / self.total_pairs))
        return ev

    def fillRooms(self, ppl_present_f, ppl_present_m):
        # tracks room number for females
        room_num_f = 0
        # tracks room number for males
        room_num_m = -1

        # randomize lists for filling rooms
        ppl_present_f.randomize()
        ppl_present_m.randomize()

        # place female leaders in rooms
        room_num_f = self.placeInRooms(
            [person for person in ppl_present_f.list if person.leader], room_num_f)
        # place male leaders in rooms
        room_num_m = self.placeInRooms(
            [person for person in ppl_present_m.list if person.leader], room_num_f)

        # push newcomers
        ppl_present_f.pushNewcomers()
        ppl_present_m.pushNewcomers()

        # place remaining females in rooms
        room_num_f = self.placeInRooms(
            [person for person in ppl_present_f.list if not person.leader], room_num_f)
        # place remaining males in rooms
        if room_num_m == -1:
            room_num_m = room_num_f
        room_num_m = self.placeInRooms(
            [person for person in ppl_present_m.list if not person.leader], room_num_m)

        # balance rooms if no past groups exist
        if not self.past_groups:
            self.balanceRooms(False)

    def getRoomNum(self, name):
        # find room number of person
        room_num = -1
        for index, room in enumerate(self.rooms):
            for person in room.list:
                if person.name == name:
                    room_num = index
        return room_num

    def getRoomSizes(self):
        # get room size for all rooms
        room_sizes = []
        for room in self.rooms:
            room_sizes.append(len(room.list))
        # remove room sizes for premade groups
        for count in range(self.premade_groups_count):
            room_sizes.pop()
        return room_sizes

    def moveToRooms(self, fill_rooms, move_lst, output):
        # the case for no previous groups
        if not self.past_groups:
            random.shuffle(move_lst)
            for room_num in fill_rooms:
                p_tuple = move_lst.pop()
                self.rooms[room_num].add(p_tuple[1])
                self.rooms[p_tuple[0]].remove(p_tuple[1].name)
                # print movement if required
                if output:
                    print(p_tuple[1], 'was moved from Room',
                          p_tuple[0] + 1, 'to Room', room_num + 1)
        else:
            # case for previous groups
            for room_num in fill_rooms:
                lowest_ev = float('inf')
                # find the best person to move
                for person in move_lst:
                    temp_room = self.copy()
                    temp_room.rooms[room_num].add(person[1])
                    temp_room.rooms[person[0]].remove(person[1].name)
                    if temp_room.errorVal() < lowest_ev:
                        best_person = person
                # move best person
                self.rooms[room_num].add(best_person[1])
                self.rooms[best_person[0]].remove(best_person[1].name)
                move_lst.remove(best_person)
                # print movement if required
                if output:
                    print(best_person[1], 'was moved from Room',
                          best_person[0] + 1, 'to Room', room_num + 1)

    def placeInRooms(self, ppl_list, room_num):
        for person in ppl_list:
            self.rooms[room_num].add(person)
            room_num += 1
            # check if we need to loop back to start
            if room_num > len(self.rooms) - 1 - self.premade_groups_count:
                room_num = 0
        return room_num

    def printRooms(self):
        # sort names in alphabetical order
        for room in self.rooms:
            room.list.sort(key=lambda person: person.name)
        # loop through the rooms
        for index, room in enumerate(self.rooms):
            print('Breakout Room', str(index + 1) +
                  ':', ', '.join(map(str, room.list)))
        # print error val
        error_val = self.errorVal()
        print('Error Val: %.2f' % error_val)
        # print number of new pairs if there were past groups
        if self.past_groups:
            print('New pairs:', self.total_pairs - self.old_pairs,
                  'out of', self.total_pairs, '(%.2f%%)\n' % ((1-self.old_pairs/self.total_pairs) * 100))

    def removePerson(self, name):
        room_num = self.getRoomNum(name)
        # check if person is valid
        if room_num == -1:
            print(name, 'is not currently in a breakout room')
            return
        # remove person from room
        self.rooms[room_num].remove(name)
        self.ppl_present.remove(name)
        # balance rooms
        self.balanceRooms(True)
        # tell user which room the person was removed from
        print(name, 'was removed from Room', room_num + 1)

        # print new rooms
        self.printRooms()

    def swap(self, p1, p2):
        room_num_1 = self.getRoomNum(p1.name)
        room_num_2 = self.getRoomNum(p2.name)
        # swap the two people
        self.rooms[room_num_1].remove(p1.name)
        self.rooms[room_num_1].add(p2)
        self.rooms[room_num_2].remove(p2.name)
        self.rooms[room_num_2].add(p1)
