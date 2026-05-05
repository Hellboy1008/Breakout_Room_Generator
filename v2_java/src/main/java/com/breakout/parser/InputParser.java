package com.breakout.parser;

import com.breakout.models.Person;
import com.breakout.models.PeopleList;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Parses input files and extracts event data including people, groups, and past pairings.
 */
public class InputParser {
    private String eventName;
    private int peoplePerRoom;
    private PeopleList peoplePresent;
    private Map<String, Double> pastGroups;
    private int premadeGroupsCount;

    public InputParser() {
        this.peoplePresent = new PeopleList();
        this.pastGroups = new HashMap<>();
        this.premadeGroupsCount = 0;
    }

    /**
     * Parse event details from present.txt file.
     */
    public void parseEventDetails() throws IOException {
        File presentFile = new File("files/present.txt");
        try (BufferedReader reader = new BufferedReader(new FileReader(presentFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.strip();

                if (line.contains("Desired number of ppl per room:")) {
                    this.peoplePerRoom = Integer.parseInt(line.substring(31).strip());
                } else if (line.contains("Event Name:")) {
                    this.eventName = line.substring(11).strip();
                } else if (line.contains("Premade groups:")) {
                    this.premadeGroupsCount = Integer.parseInt(line.substring(15).strip());
                } else if (!line.contains("**") && !line.contains("PRESENT:") && !line.isEmpty()) {
                    this.peoplePresent.add(new Person(line));
                }
            }
        }
    }

    /**
     * Parse past groups from previous-rooms.txt file.
     */
    public void parsePastGroups() throws IOException {
        File previousRoomsFile = new File("files/previous-rooms.txt");
        java.util.List<String[]> pastGroupsList = new java.util.ArrayList<>();
        boolean prevGroups = false;
        int numPastGroups = 0;

        try (BufferedReader reader = new BufferedReader(new FileReader(previousRoomsFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.strip();

                if (line.contains("EVENT: " + this.eventName) && line.contains("(Y)")) {
                    prevGroups = true;
                } else if (prevGroups && line.contains("EVENT:")) {
                    break;
                } else if (prevGroups && !line.isEmpty()) {
                    String[] group = (line + "," + numPastGroups).split(",");
                    pastGroupsList.add(group);
                } else if (prevGroups && line.isEmpty()) {
                    numPastGroups++;
                }
            }
        } catch (IOException e) {
            // File not found, no past groups
            return;
        }

        // Process past groups if they exist
        if (prevGroups) {
            java.util.List<String[]> pastPairsList = new java.util.ArrayList<>();

            for (String[] group : pastGroupsList) {
                for (int p1 = 0; p1 < group.length - 1; p1++) {
                    for (int p2 = p1 + 1; p2 < group.length - 1; p2++) {
                        String[] pair = {group[p1].strip(), group[p2].strip(), group[group.length - 1]};
                        java.util.Arrays.sort(pair, 0, 2);
                        pastPairsList.add(pair);
                    }
                }
            }

            // Create map of past pairs with weights
            for (String[] pair : pastPairsList) {
                String key = pair[0] + "," + pair[1];
                double weight = Integer.parseInt(pair[0]) * (1.0 / numPastGroups);

                if (!this.pastGroups.containsKey(key)) {
                    this.pastGroups.put(key, weight);
                } else {
                    double current = this.pastGroups.get(key);
                    current += 10;
                    current = (int) current + weight;
                    this.pastGroups.put(key, current);
                }
            }
        }
    }

    // Getters
    public String getEventName() {
        return eventName;
    }

    public int getPeoplePerRoom() {
        return peoplePerRoom;
    }

    public PeopleList getPeoplePresent() {
        return peoplePresent;
    }

    public Map<String, Double> getPastGroups() {
        return pastGroups;
    }

    public int getPremadeGroupsCount() {
        return premadeGroupsCount;
    }
}

