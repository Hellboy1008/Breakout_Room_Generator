# Created by: 龍ONE
# Date Created: February 1, 2021
# Date Edited: February 9, 2021
# Purpose: Person object used to create breakout rooms.

# imports
import os

# global variables
curr_dir = os.getcwd()  # current directory


class Person:
    def __init__(self, name):
        # check if person is a newcomer or in a premade group
        if '(N)' in name:
            self.group = 0
            self.newcomer = True
        elif '(G' in name:
            self.group = int(name[name.index('(G') + 2: name.index('(G') + 3])
            self.newcomer = False
        else:
            self.group = 0
            self.newcomer = False
        # remove special notations
        if '(' in name:
            self.name = name[0:name.index('(')].strip()
        else:
            self.name = name
        # add gender for person
        self.addGender()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def addGender(self):
        # get the gender and leader status for the person from master file
        self.gender = None
        master = open(curr_dir + '/files/master.txt', 'r')
        for line in master:
            if self.name in line:
                if '(M' in line:
                    self.gender = 'M'
                else:
                    self.gender = 'F'
                if ',L)' in line:
                    self.leader = True
                else:
                    self.leader = False 
        # if the person was not part of the master file
        if self.gender == None:
            self.leader = False
            # ask user for the person's gender
            gender = ''
            while gender.lower() != 'm' and gender.lower() != 'f':
                gender = input('Input the gender for: ' +
                                self.name + '\nType M for male, F for female\n')
            if gender.lower() == 'm':
                self.gender = 'M'
            else:
                self.gender = 'F'