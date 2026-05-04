# Breakout Room Generator - Java Version (v2)

This is a Java port of the Python Breakout Room Generator. It generates optimized breakout rooms for Zoom meetings using advanced algorithms.

## Project Structure

```
v2_java/
├── pom.xml                                              # Maven configuration file
├── README.md                                            # This file
├── src/
│   ├── main/
│   │   ├── java/com/breakoutroom/
│   │   │   ├── Main.java                               # Entry point for room generation
│   │   │   ├── StatsMain.java                          # Entry point for statistics
│   │   │   ├── model/
│   │   │   │   ├── Person.java                         # Represents a participant
│   │   │   │   ├── PeopleList.java                     # Collection of people
│   │   │   │   └── BreakoutRooms.java                  # Manages breakout rooms
│   │   │   └── service/
│   │   │       ├── RoomGenerator.java                  # Main algorithm and logic
│   │   │       └── StatsGenerator.java                 # Excel statistics generation
│   │   └── resources/                                  # Configuration and resources
│   └── test/                                           # Unit tests
└── target/                                             # Compiled classes (generated)
```

## Features

### 1. **Person Model** (`Person.java`)
- Represents individual participants
- Parses special notations:
  - `(N)` for newcomers
  - `(G#)` for premade groups (where # is group number)
- Reads gender and leader status from `master.txt` file
- Prompts user for missing information

### 2. **PeopleList** (`PeopleList.java`)
- Collection of people with utility methods
- Methods:
  - `add()` - Add a person
  - `pop()` - Remove and return first person
  - `pushNewcomers()` - Move newcomers to front
  - `randomize()` - Shuffle the list
  - `remove()` - Remove by name
  - `getNames()` - Get all names

### 3. **BreakoutRooms** (`BreakoutRooms.java`)
- Manages room creation and assignment
- Features:
  - Balances gender distribution
  - Ensures leader representation in each room
  - Prioritizes newcomer placement
  - Minimizes people paired with previous group members
  - Supports premade groups
- Key methods:
  - `fillRooms()` - Distribute people across rooms
  - `balanceRooms()` - Adjust room sizes
  - `errorVal()` - Calculate optimization metric
  - `printRooms()` - Display room assignments
  - `editRooms()` - Interactive room modification

### 4. **RoomGenerator** (`RoomGenerator.java`)
- Main service for room generation
- Implements two optimization algorithms:
  1. **Greedy Algorithm** (5000 trials)
  2. **Simulated Annealing** (2500 trials)
- Methods:
  - `generateBreakoutRooms()` - Main entry point
  - `getEventDetails()` - Read from `present.txt`
  - `searchPastGroups()` - Load history from `previous-rooms.txt`
  - `separatePremadeGroups()` - Extract predefined groups
  - `separateGender()` - Sort by gender

### 5. **StatsGenerator** (`StatsGenerator.java`)
- Generates Excel statistics files
- Creates matrix showing pair frequencies
- Features:
  - Color-coded heatmap in Excel
  - Handles previous room data
  - Formats for readability

## Input File Format

### `files/present.txt`
```
Event Name: My Event
Desired number of ppl per room: 4
Premade groups: 0

PRESENT:
** List of participants below **
John Doe
Jane Smith (N)
Bob Johnson (G1)
...
```

### `files/master.txt`
```
John Doe (M)
Jane Smith (F,L)
Bob Johnson (M,L)
...
```
- `(M)` / `(F)` = Male/Female
- `(,L)` = Leader

### `files/previous-rooms.txt`
```
EVENT: My Event (Y)
John Doe, Jane Smith
Bob Johnson, Alice Brown

John Doe, Bob Johnson
Jane Smith, Charlie Davis

EVENT: Other Event (N)
...
```

## Building and Running

### Prerequisites
- Java 11 or higher
- Maven 3.6 or higher

### Build
```bash
cd v2_java
mvn clean install
```

### Run Room Generator
```bash
mvn exec:java -Dexec.mainClass="com.breakoutroom.Main"
```

### Run Statistics Generator
```bash
mvn exec:java -Dexec.mainClass="com.breakoutroom.StatsMain"
```

### Create Executable JAR
```bash
mvn package
java -jar target/breakout-room-generator-2.0.0.jar
```

## Algorithm Details

### Greedy Algorithm
- Creates multiple random room configurations
- Evaluates each based on error value (penalty for past pairings)
- Keeps the best configuration
- Runs for 5000 iterations

### Simulated Annealing
- Starts with best greedy result
- Makes random swaps between valid pairs
- Accepts swaps that improve error value
- Continues for 2500 iterations
- Escapes local optima

### Error Value Calculation
- Penalizes people who have been in same room before
- Formula: `error = sum of past pair penalties * (1 - new_pair_ratio)`
- Goal: Maximize new pair creation while minimizing room size variance

## Implementation Notes

### Differences from Python Version
1. **Type Safety**: Strongly typed with generics
2. **Excel**: Uses Apache POI library instead of xlsxwriter
3. **File I/O**: Java BufferedReader for file handling
4. **Collections**: ArrayList and HashMap instead of Python lists/dicts
5. **Randomization**: Java Random class for reproducibility options

### Key Classes and Methods
- `Person.parseNameAndGroup()` - Parse special notation from names
- `BreakoutRooms.fillRooms()` - Core room assignment logic
- `BreakoutRooms.errorVal()` - Optimization metric
- `RoomGenerator.createBestBreakoutRooms()` - Dual algorithm optimization

## Dependencies
- **Apache POI 5.2.3** - Excel file creation
- **JUnit 4.13.2** - Unit testing

## Future Enhancements
- [ ] Unit tests for all classes
- [ ] Support for XLSX file input/output
- [ ] GUI interface
- [ ] Configuration file support
- [ ] Performance optimization for large groups
- [ ] Additional optimization algorithms

## Original Author
龍ONE

## Ported to Java
May 3, 2026

## License
See LICENSE file in root directory

