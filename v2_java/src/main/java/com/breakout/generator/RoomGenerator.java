package com.breakout.generator;

import com.breakout.models.Person;
import com.breakout.models.PeopleList;
import com.breakout.models.Room;
import com.breakout.parser.InputParser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Main orchestrator for room generation.
 * Coordinates parsing, validation, room creation, and optimization.
 */
public class RoomGenerator {
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
    public Room generateBreakoutRooms() throws IOException {
        // Parse event details from present.txt
        InputParser parser = new InputParser();
        parser.parseEventDetails();

        this.eventName = parser.getEventName();
        this.peoplePerRoom = parser.getPeoplePerRoom();
        this.peoplePresent = parser.getPeoplePresent();
        this.premadeGroupsCount = parser.getPremadeGroupsCount();

        // Parse previous groups for the event
        parser.parsePastGroups();
        this.pastGroups = parser.getPastGroups();

        // Separate premade groups if applicable
        if (this.premadeGroupsCount > 0) {
            separatePremadeGroups();
        }

        // Fill gendered lists for participants
        separateGender();

        // Create rooms based on whether past groups exist
        Room breakoutRooms;
        if (this.pastGroups.isEmpty()) {
            breakoutRooms = new Room(
                this.pastGroups,
                this.peoplePerRoom,
                this.peoplePresent,
                this.peoplePresentF,
                this.peoplePresentM,
                this.premadeGroups
            );
        } else {
            ScoringEngine engine = new ScoringEngine(
                this.peoplePresent,
                this.peoplePresentF,
                this.peoplePresentM,
                this.pastGroups,
                this.peoplePerRoom,
                this.premadeGroups
            );
            breakoutRooms = engine.generateOptimalRooms();
        }

        // Print and return rooms
        breakoutRooms.printRooms();
        breakoutRooms.editRooms();

        return breakoutRooms;
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

