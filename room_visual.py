import pandas as pd
import sys

# file for previous rooms
previous_rooms = open('previous-rooms.txt', 'r')

# ask for user input for event name
event_name = input("Enter the event name: ")

# check if event exists in text file
event_exists = False
add_names = False
rooms_lst = []
for line in previous_rooms:
    if 'EVENT: ' + event_name in line and '(Y)' in line:
        event_exists = True
        add_names = True
        continue
    elif 'EVENT: ' + event_name in line and '(N)' in line:
        break
    if event_exists == True:
        if 'EVENT: ' in line:
            break
        if len(line.strip()) != 0:
            rooms_lst.append(line.strip().split(','))
                    
# create tuple for all pairs
tuples_lst = []
for groups in rooms_lst:
    for index_one in range(len(groups)):
        for index_two in range(index_one + 1, len(groups)):
            tuples_lst.append((groups[index_one].strip(), groups[index_two].strip()))

# print error message
if event_exists == False or len(rooms_lst) == 0:
    print("Event was not found or there are no previous breakout rooms for the event.")
    sys.exit()
    
# create list of people
ppl_lst = []
for groups in rooms_lst:
    for person in groups:
        if person.strip() not in ppl_lst:
            ppl_lst.append(person.strip())
ppl_lst.sort()

# create dataframe
df = pd.DataFrame(0, index = ppl_lst, columns = ppl_lst ) 

# add pairs to dataframe
for tuple_pair in tuples_lst:
    df[tuple_pair[0]][tuple_pair[1]] += 1
    df[tuple_pair[1]][tuple_pair[0]] += 1

# export dataframe as excel file
df.to_excel("breakout_data.xlsx")