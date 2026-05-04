package com.breakout.models;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Represents an event with breakout room configuration.
 *
 * Date Ported to Java: May 3, 2026
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

    // Getters and setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getPeoplePerRoom() {
        return peoplePerRoom;
    }

    public void setPeoplePerRoom(int peoplePerRoom) {
        this.peoplePerRoom = peoplePerRoom;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public Map<String, Double> getPastGroups() {
        return pastGroups;
    }

    public void setPastGroups(Map<String, Double> pastGroups) {
        this.pastGroups = pastGroups;
    }

    public List<PeopleList> getPremadeGroups() {
        return premadeGroups;
    }

    public void setPremadeGroups(List<PeopleList> premadeGroups) {
        this.premadeGroups = premadeGroups;
    }

    public PeopleList getAttendees() {
        return attendees;
    }

    public void setAttendees(PeopleList attendees) {
        this.attendees = attendees;
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

