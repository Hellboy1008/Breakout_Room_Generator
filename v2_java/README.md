# Breakout Room Generator - Java Edition

A robust Java application for generating optimized breakout room assignments for Zoom meetings while balancing various constraints including gender distribution, leader placement, newcomer prioritization, and past pairing avoidance.

## Project Structure

```
breakout-room-generator/
├── pom.xml
├── README.md
├── SETUP.md
├── sample_files/
│   ├── present (sample).txt
│   ├── master (sample).txt
│   └── previous-rooms (sample).txt
└── src/
    ├── main/
    │   ├── java/com/breakout/
    │   │   ├── Main.java                        # Entry point for room generation
    │   │   ├── StatsMain.java                   # Entry point for statistics
    │   │   ├── models/
    │   │   │   ├── Person.java                  # Individual participant model
    │   │   │   ├── PeopleList.java              # Collection of participants
    │   │   │   ├── Room.java                    # Breakout room configuration
    │   │   │   └── Event.java                   # Event metadata
    │   │   ├── parser/
    │   │   │   ├── InputParser.java             # Parses input files
    │   │   │   └── DataValidator.java           # Validates data integrity
    │   │   ├── generator/
    │   │   │   ├── RoomGenerator.java           # Main orchestrator
    │   │   │   └── ScoringEngine.java           # Optimization algorithms
    │   │   └── output/
    │   │       ├── ExcelExporter.java           # Excel export
    │   │       └── TextExporter.java            # Text export
    │   └── resources/
    │       ├── master.csv                       # Participant metadata
    │       ├── present.csv                      # Event attendees
    │       └── previous-rooms.json              # Historical assignments
    └── test/
        └── java/com/breakout/
            ├── RoomGeneratorTest.java
            └── ScoringEngineTest.java
```

## Architecture & Design

### Clean Separation of Concerns

**Models** - Core data representations
- `Person`: Individual participant with metadata
- `PeopleList`: Collection wrapper with utility methods
- `Room`: Breakout room configuration and management
- `Event`: Event metadata and configuration

**Parser** - Input handling
- `InputParser`: Parses `present.txt` and `previous-rooms.txt`
- `DataValidator`: Validates input data and file integrity

**Generator** - Room generation logic
- `RoomGenerator`: Main orchestrator, coordinates parsing and generation
- `ScoringEngine`: Optimization algorithms (Greedy + Simulated Annealing)

**Output** - Export functionality
- `ExcelExporter`: Creates Excel statistics files
- `TextExporter`: Generates text reports

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
mvn exec:java -Dexec.mainClass="com.breakout.Main"
```

### Run Statistics Generator
```bash
mvn exec:java -Dexec.mainClass="com.breakout.StatsMain"
```

### Create Executable JAR
```bash
mvn package
java -jar target/breakout-room-generator-2.0.0.jar
```

### Run Tests
```bash
mvn test
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

## Implementation Details

### Package Organization

| Package | Purpose | Classes |
|---------|---------|---------|
| `com.breakout` | Entry points | `Main`, `StatsMain` |
| `com.breakout.models` | Data models | `Person`, `PeopleList`, `Room`, `Event` |
| `com.breakout.parser` | Input parsing | `InputParser`, `DataValidator` |
| `com.breakout.generator` | Room generation | `RoomGenerator`, `ScoringEngine` |
| `com.breakout.output` | Export functionality | `ExcelExporter`, `TextExporter` |

### Key Design Patterns

1. **Separation of Concerns**: Input parsing, generation, and output are separate
2. **Single Responsibility**: Each class has one primary purpose
3. **Validation**: Data is validated at input boundaries
4. **Testability**: Classes can be unit tested independently

### Dependencies
- **Apache POI 5.2.3** - Excel file creation
- **JUnit 4.13.2** - Unit testing

## Future Enhancements
- [ ] REST API endpoints
- [ ] Graphical user interface
- [ ] Advanced scoring options  
- [ ] Room size constraints
- [ ] Skill-based assignment
- [ ] Event history visualization

## Original Author
Created by: 龍ONE

## Ported to Java
May 3, 2026

## License
See LICENSE file in root directory

