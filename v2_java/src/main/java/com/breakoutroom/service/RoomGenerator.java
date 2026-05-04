package com.breakoutroom.service;

import com.breakoutroom.model.BreakoutRooms;
import com.breakoutroom.model.Person;
import com.breakoutroom.model.PeopleList;

import java.io.*;
import java.util.*;

/**
 * Helper functions for generating breakout rooms.
 *
 * Created by: 龍ONE
 * Date Created: January 25, 2021
 * Date Ported to Java: May 3, 2026
 */
public class RoomGenerator {
    private static final int GREEDY_TRIALS = 5000;
    private static final int SIMULATED_ANNEALING_TRIALS = 2500;

    private String eventName;
    private int peoplePerRoom;
    private PeopleList peoplePresent;
    private PeopleList peoplePresentF;
    private PeopleList peoplePresentM;
    private Map<String, Double> pastGroups;
    private List<PeopleList> premadeGroups;
    private int premadeGroupsCount;

    public RoomGenerator() {
        this.peoplePresent = new PeopleList();
        this.peoplePresentF = new PeopleList();
        this.peoplePresentM = new PeopleList();
        this.pastGroups = new HashMap<>();
        this.premadeGroups = new ArrayList<>();
        this.premadeGroupsCount = 0;
    }

    /**
     * Generate optimal breakout rooms.
     */
    public BreakoutRooms generateBreakoutRooms() throws IOException {
        // Get event details from present.txt
        getEventDetails();

        // Get previous groups for the event
        searchPastGroups();

        // Separate premade groups if applicable
        if (this.premadeGroupsCount > 0) {
            separatePremadeGroups();
        }

        // Fill gendered lists for participants
        separateGender();

        // Create rooms based on whether past groups exist
        BreakoutRooms breakoutRooms;
        if (this.pastGroups.isEmpty()) {
            breakoutRooms = new BreakoutRooms(
                this.pastGroups,
                this.peoplePerRoom,
                this.peoplePresent,
                this.peoplePresentF,
                this.peoplePresentM,
                this.premadeGroups
            );
        } else {
            breakoutRooms = createBestBreakoutRooms();
        }

        // Print and return rooms
        breakoutRooms.printRooms();
        breakoutRooms.editRooms();

        return breakoutRooms;
    }

    /**
     * Create the best breakout rooms using greedy and simulated annealing algorithms.
     */
    private BreakoutRooms createBestBreakoutRooms() {
        BreakoutRooms bestBreakoutRoom = null;
        double lowestEv = Double.POSITIVE_INFINITY;

        // Greedy algorithm
        for (int count = 0; count < GREEDY_TRIALS; count++) {
            System.out.print("Applying algorithm 1... " + (count + 1) + "/" + GREEDY_TRIALS + "\r");

            BreakoutRooms breakoutRooms = new BreakoutRooms(
                this.pastGroups,
                this.peoplePerRoom,
                this.peoplePresent,
                this.peoplePresentF,
                this.peoplePresentM,
                this.premadeGroups
            );

            double ev = breakoutRooms.errorVal();
            if (ev < lowestEv) {
                bestBreakoutRoom = breakoutRooms.copy();
                lowestEv = ev;
            }

            if (lowestEv == 0) {
                break;
            }
        }

        if (bestBreakoutRoom != null) {
            bestBreakoutRoom.balanceRooms(false);
        }
        System.out.println("\nAlgorithm 1 completed");

        // Simulated annealing
        for (int count = 0; count < SIMULATED_ANNEALING_TRIALS; count++) {
            System.out.print("Applying algorithm 2... " + (count + 1) + "/" + SIMULATED_ANNEALING_TRIALS + "\r");

            boolean validPair = false;
            Person p1 = null, p2 = null;

            // Find a valid pair to switch
            while (!validPair) {
                Random rand = new Random();
                PeopleList selectedList;
                if (rand.nextInt(2) == 0) {
                    this.peoplePresentF.randomize();
                    selectedList = this.peoplePresentF;
                } else {
                    this.peoplePresentM.randomize();
                    selectedList = this.peoplePresentM;
                }

                p1 = selectedList.get(0);
                p2 = selectedList.get(1);

                if (p1.isLeader() == p2.isLeader() &&
                    p1.isNewcomer() == p2.isNewcomer() &&
                    bestBreakoutRoom.getRoomNum(p1.getName()) != bestBreakoutRoom.getRoomNum(p2.getName())) {
                    validPair = true;
                }
            }

            BreakoutRooms tempRooms = bestBreakoutRoom.copy();
            tempRooms.swap(p1, p2);
            double ev = tempRooms.errorVal();

            if (ev < lowestEv) {
                bestBreakoutRoom = tempRooms.copy();
                lowestEv = ev;
            }

            if (lowestEv == 0) {
                break;
            }
        }

        System.out.println("\nAlgorithm 2 completed");
        return bestBreakoutRoom;
    }

    /**
     * Read event details from present.txt file.
     */
    private void getEventDetails() throws IOException {
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
     * Search for and load past groups from previous-rooms.txt file.
     */
    private void searchPastGroups() throws IOException {
        File previousRoomsFile = new File("files/previous-rooms.txt");
        List<String[]> pastGroupsList = new ArrayList<>();
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
            List<String[]> pastPairsList = new ArrayList<>();

            for (String[] group : pastGroupsList) {
                for (int p1 = 0; p1 < group.length - 1; p1++) {
                    for (int p2 = p1 + 1; p2 < group.length - 1; p2++) {
                        String[] pair = {group[p1].strip(), group[p2].strip(), group[group.length - 1]};
                        Arrays.sort(pair, 0, 2);
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

    /**
     * Separate premade groups from the general population.
     */
    private void separatePremadeGroups() {
        for (int count = 0; count < this.premadeGroupsCount; count++) {
            PeopleList group = new PeopleList();
            int groupNum = count + 1;

            for (Person person : this.peoplePresent.getList()) {
                if (person.getGroup() == groupNum) {
                    group.add(person);
                }
            }

            this.premadeGroups.add(group);
        }

        // Remove premade group members from general population
        for (PeopleList group : this.premadeGroups) {
            for (Person person : group.getList()) {
                this.peoplePresent.remove(person.getName());
            }
        }
    }

    /**
     * Separate participants by gender.
     */
    private void separateGender() {
        for (Person person : this.peoplePresent.getList()) {
            if ("M".equals(person.getGender())) {
                this.peoplePresentM.add(person);
            } else {
                this.peoplePresentF.add(person);
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

    public PeopleList getPeoplePresentF() {
        return peoplePresentF;
    }

    public PeopleList getPeoplePresentM() {
        return peoplePresentM;
    }

    public Map<String, Double> getPastGroups() {
        return pastGroups;
    }

    public List<PeopleList> getPremadeGroups() {
        return premadeGroups;
    }
}

