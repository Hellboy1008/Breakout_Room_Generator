package com.breakout.models;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Represents an event with breakout room configuration and attendee management.
 */
public class Event {
    private String name;
    private int peoplePerRoom;
    private LocalDateTime createdAt;
    private Map<String, Double> pastGroups;
    private List<PeopleList> premadeGroups;
    private PeopleList attendees;

    public Event(String name) {
        this.name = name;
        this.peoplePerRoom = 4; // Default
        this.createdAt = LocalDateTime.now();
        this.pastGroups = new java.util.HashMap<>();
        this.premadeGroups = new ArrayList<>();
        this.attendees = new PeopleList();
    }

    public Event(String name, int peoplePerRoom) {
        this(name);
        this.peoplePerRoom = peoplePerRoom;
    }

    public void addAttendee(Person person) {
        this.attendees.add(person);
    }

    public int getAttendeeCount() {
        return this.attendees.size();
    }

    @Override
    public String toString() {
        return "Event{" +
                "name='" + name + '\'' +
                ", peoplePerRoom=" + peoplePerRoom +
                ", attendees=" + attendees.size() +
                '}';
    }
}

