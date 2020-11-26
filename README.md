# Breakout-Room-Generator

Generates breakout rooms with the following conditions:

1. Gender is balanced as much as possible. If there is a significant amount of males/females compared to the other gender, the groups might not be balanced.
2. Maximizes the number of new people met by each participant. This will depend on the frequency of each participant showing up to the event and how many previous iterations of the event there were.

## Running the program

In order to run the program, you will need to have python installed in your local system or run it online using a python compiler. The only files you need to run is `room_generator.py` and `room_visual.py`. The room generator file creates a breakout room for your event while the room visual is for creating excel and text files that reflect your breakout room diversity. As mentioned below, you will need to create additional text files before running the program.

## Additional required files that are not in the repository (please note that the formatting of the file is crucial in the program running as expected!)

### master.txt

This file will contain the list of all previous participants or anticipated participants for the breakout room with their gender. The file format should look like the following:

```txt
FirstName LastNameInitial (M)
FirstName LastNameInitial (F)
FirstName LastNameInitial (F)
FirstName LastNameInitial (M)
...
```

### present.txt

This file will contain all the people that are present at the event, alongside the event name and the desired number of people per room. The file format should look like the following:

```txt
** Note: Add the following letters after the names if applicable **
** FirstName LastNameInitial (N) -> for newcomer **
** FirstName LastNameInitial (L) -> for leaders **

Desired number of ppl per room: 5
Event Name: Meeting 1

PRESENT:

FirstName LastNameInitial
FirstName LastNameInitial
FirstName LastNameInitial (L)
FirstName LastNameInitial (N)
...
```

### previous-rooms.txt

This file will contain data from any previous breakout rooms for any events. Adding (Y) to the end of an event name indicates that there were previous breakout rooms for that event. The file format should look like the following:

```txt
EVENT: Meeting 1 (Y)

FirstName LastNameInitial, FirstName LastNameInitial, FirstName LastNameInitial
FirstName LastNameInitial, FirstName LastNameInitial, FirstName LastNameInitial
FirstName LastNameInitial, FirstName LastNameInitial, FirstName LastNameInitial
FirstName LastNameInitial, FirstName LastNameInitial, FirstName LastNameInitial

FirstName LastNameInitial, FirstName LastNameInitial, FirstName LastNameInitial
FirstName LastNameInitial, FirstName LastNameInitial, FirstName LastNameInitial
FirstName LastNameInitial, FirstName LastNameInitial, FirstName LastNameInitial

EVENT: Meeting 2 (N)
```

## Interpreting the error value

If your event has previous breakout rooms, there will be an error value that is printed after running the program to generating new breakout rooms.

The total error value displayed when you run the program is a addition of individual error values from each recurring pair. The program also displays the number of pairs that have shared `x` number of rooms together and how many pairs shared a room in the previous set of breakout rooms for your reference.

### How the error value is calculated

Let's suppose you have `n` previous sets of breakout rooms.

Each time the program finds a pair that have shared a breakout room in the past, it will add `m * 1/n` to the error value, where m is how long ago the previous breakout room was. For example, if you had 5 previous sets of breakout rooms and the pair previously met at the first set of breakout rooms, it will add the value `1 * 1/5 = 0.2`. On the other hand, if the pair previously met at the most recent set of breakout rooms, it will add the value `5 * 1/5 = 1.0`. This way, a pair that has met more recently is weighted more than a pair that haven't met in a while.

Additionally, each time the program finds a pair that has met more than once in previous sets of breakout rooms, it adds 5 to the error value, while still accounting for the last time they met. For example, let's say you have 5 previous sets of breakout rooms and the pair previously met at the first set of breakout rooms. The program then finds out that the pair also met at the most recent set of breakout rooms. The error value changes from 0.2 to 6.0, where 6 is derived from 1, the value calculated from meeting at the most recent set of breakout rooms, plus 5.

\
**If you are familiar with python, feel free to edit the program to better suite your needs! If there are any bugs/issues with the current program, please report the issue on Github and I will try my best to look into them.**
