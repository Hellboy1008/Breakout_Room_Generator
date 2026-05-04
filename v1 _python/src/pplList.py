# Created by: 龍ONE
# Date Created: January 25, 2021
# Date Edited: February 9, 2021
# Purpose: List object used to create breakout rooms.

# imports
import random


class pplList:
    def __init__(self):
        self.list = []
        self.premade = False

    def __repr__(self):
        return str(self.list)

    def __str__(self):
        return str(self.list)

    def add(self, person):
        self.list.append(person)
        
    def names(self):
        names = []
        for person in self.list:
            names.append(person.name)
        return names

    def pop(self):
        person = self.list[0]
        self.list.remove(self.list[0])
        return person

    def pushNewcomers(self):
        newcomers = [person for person in self.list if person.newcomer]
        self.list = [person for person in self.list if not person.newcomer]
        # add newcomes to the front of the list
        for person in newcomers:
            self.list.insert(0, person)

    def randomize(self):
        random.shuffle(self.list)

    def remove(self, person_name):
        for person in self.list:
            if person.name == person_name:
                self.list.remove(person)
