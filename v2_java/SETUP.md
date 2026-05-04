# Setup Guide for Breakout Room Generator (Java v2)

## Quick Start

1. **Install Java and Maven**
   - Java 11 or higher: https://adoptopenjdk.net/
   - Maven 3.6 or higher: https://maven.apache.org/download.cgi

2. **Clone/Navigate to project**
   ```bash
   cd v2_java
   ```

3. **Build the project**
   ```bash
   mvn clean install
   ```

4. **Prepare input files**
   - Create a `files/` directory in `v2_java/`
   - Copy sample files from `sample_files/` and rename them:
     - `present (sample).txt` → `files/present.txt`
     - `master (sample).txt` → `files/master.txt`
     - `previous-rooms (sample).txt` → `files/previous-rooms.txt`

5. **Run the application**
   ```bash
   mvn exec:java -Dexec.mainClass="com.breakoutroom.Main"
   ```

## File Setup

### Directory Structure
```
v2_java/
├── files/                          # Create this directory
│   ├── present.txt                # Current event participants
│   ├── master.txt                 # Master list with gender/role
│   └── previous-rooms.txt         # Historical room assignments
├── pom.xml
├── README.md
└── src/
```

### File Formats

#### `files/present.txt`
```
Event Name: My Team Meeting
Desired number of ppl per room: 4
Premade groups: 0

PRESENT:
** List participants here **
Alice Johnson
Bob Smith (N)
Carol Williams
David Brown
```

**Notation:**
- `(N)` - Newcomer flag
- `(G1)`, `(G2)`, etc. - Premade group assignments

#### `files/master.txt`
```
Alice Johnson (F,L)
Bob Smith (M)
Carol Williams (F)
David Brown (M,L)
Eve Davis (F)
```

**Notation:**
- `(M)` - Male, `(F)` - Female (required)
- `(,L)` - Leader status (optional)

#### `files/previous-rooms.txt`
```
EVENT: My Team Meeting (Y)
Alice Johnson, Bob Smith, Carol Williams
David Brown, Eve Davis

Alice Johnson, David Brown
Bob Smith, Carol Williams
Eve Davis

EVENT: Other Meeting (N)
```

**Format:**
- `EVENT: Name (Y)` / `EVENT: Name (N)` - Event with/without previous meetings
- Blank lines separate different meeting sessions
- Participants separated by commas

## Building

### Full Build
```bash
mvn clean install
```

### Skip Tests
```bash
mvn clean install -DskipTests
```

### Create Executable JAR
```bash
mvn clean package
java -jar target/breakout-room-generator-2.0.0.jar
```

## Running

### Using Maven
```bash
# Generate breakout rooms
mvn exec:java -Dexec.mainClass="com.breakoutroom.Main"

# Generate statistics
mvn exec:java -Dexec.mainClass="com.breakoutroom.StatsMain"
```

### Using JAR
```bash
java -jar target/breakout-room-generator-2.0.0.jar
```

## IDE Setup

### IntelliJ IDEA
1. File → Open → Select `v2_java` folder
2. Maven → Enable Auto Import
3. Run → Edit Configurations
4. Add new Application configuration
5. Main class: `com.breakoutroom.Main`
6. Working directory: `$MODULE_DIR$`

### Eclipse
1. File → Import → Existing Maven Projects
2. Select `v2_java` folder
3. Right-click project → Run As → Maven clean
4. Right-click project → Run As → Maven install

### VS Code
1. Install Java Extension Pack
2. Open folder `v2_java`
3. Create `.vscode/launch.json`:
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "type": "java",
         "name": "Launch Main",
         "request": "launch",
         "mainClass": "com.breakoutroom.Main",
         "console": "integratedTerminal"
       }
     ]
   }
   ```

## Troubleshooting

### Issue: "Files not found"
**Solution:** Ensure `files/` directory exists in `v2_java/` root directory

### Issue: Maven build fails
**Solution:** 
```bash
mvn clean
rm -rf ~/.m2/repository
mvn install
```

### Issue: Class not found when running
**Solution:** Make sure to run from `v2_java` directory and use `-Dexec.mainClass` with full path

### Issue: User input not working
**Solution:** When running via IDE, check if "Run in terminal" is enabled

## Advanced Usage

### Configuration for Large Groups
Modify constants in `RoomGenerator.java`:
```java
private static final int GREEDY_TRIALS = 5000;        // Increase for better results
private static final int SIMULATED_ANNEALING_TRIALS = 2500;
```

### Testing
```bash
mvn test
```

### Code Quality
```bash
mvn spotbugs:check
mvn pmd:check
```

## Performance Tips

1. **Number of Trials:** More trials = better optimization but slower
   - Small groups (6-12): 5000 greedy + 2500 SA
   - Medium groups (12-30): 2500 greedy + 1000 SA
   - Large groups (30+): 1000 greedy + 500 SA

2. **File I/O:** Use consistent file paths (relative to `v2_java/`)

3. **Memory:** For very large groups, increase JVM heap:
   ```bash
   mvn exec:java -Dexec.mainClass="com.breakoutroom.Main" \
                 -Dexec.jvmArgs="-Xmx2G"
   ```

## Next Steps

1. Prepare your participant lists
2. Run the generator
3. Review suggested room assignments
4. Use interactive editing to make adjustments
5. Generate statistics for future reference

## Support

For issues or questions, refer to:
- `README.md` - Feature overview
- Source code comments - Line-by-line explanations
- Python version - `../v1 _python/` - Original logic


