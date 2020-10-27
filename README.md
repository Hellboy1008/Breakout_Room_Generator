# Breakout-Room-Generator

Generates breakout rooms with different conditions for reoccurring events with multiple breakout rooms over time. The algorithm maximizes gender balance and the number of different people you meet each time you create a breakout room.

## Additional required files that are not in the repository (create them yourselves!)

### master.txt

This file will contain the list of all previous participants or anticipated participants for the breakout room with their gender. The file format should look like the following:

```txt
FirstName LastName (M)
FirstName LastName (F)
FirstName LastName (F)
FirstName LastName (M)
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

FirstName LastName
FirstName LastName
FirstName LastName
FirstName LastName
...
```

### previous-rooms.txt

This file will contain data from any previous breakout rooms for any events. Adding (Y) to the end of an event name indicates that there were previous breakout rooms for that event. The file format should look like the following:

```txt
EVENT: Meeting 1 (Y)

FirstName LastName, FirstName LastName, FirstName LastName
FirstName LastName, FirstName LastName, FirstName LastName
FirstName LastName, FirstName LastName, FirstName LastName
FirstName LastName, FirstName LastName, FirstName LastName

FirstName LastName, FirstName LastName, FirstName LastName
FirstName LastName, FirstName LastName, FirstName LastName
FirstName LastName, FirstName LastName, FirstName LastName

EVENT: Meeting 2 (N)
```
