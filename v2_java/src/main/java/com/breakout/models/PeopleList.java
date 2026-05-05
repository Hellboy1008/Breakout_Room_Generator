package com.breakout.models;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Represents a list of people for breakout rooms.
 * Provides utilities for managing, randomizing, and organizing participants.
 */
public class PeopleList {
    private List<Person> list;
    private boolean premade;

    public PeopleList() {
        this.list = new ArrayList<>();
        this.premade = false;
    }

    /**
     * Add a person to the list.
     */
    public void add(Person person) {
        this.list.add(person);
    }

    /**
     * Move all newcomers to the front of the list.
     */
    public void pushNewcomers() {
        List<Person> newcomers = new ArrayList<>();
        List<Person> nonNewcomers = new ArrayList<>();

        for (Person person : this.list) {
            if (person.newcomer()) {
                newcomers.add(person);
            } else {
                nonNewcomers.add(person);
            }
        }

        this.list.clear();
        this.list.addAll(newcomers);
        this.list.addAll(nonNewcomers);
    }

    /**
     * Randomly shuffle the list.
     */
    public void randomize() {
        Collections.shuffle(this.list);
    }

    /**
     * Remove a person by name.
     */
    public void remove(String personName) {
        this.list.removeIf(person -> person.name().equals(personName));
    }

    @Override
    public String toString() {
        return this.list.toString();
    }

    public List<Person> getList() {
        return list;
    }

    public int size() {
        return this.list.size();
    }

    public Person get(int index) {
        return this.list.get(index);
    }

    public boolean isEmpty() {
        return this.list.isEmpty();
    }

    public boolean isPremade() {
        return premade;
    }

    public void setPremade(boolean premade) {
        this.premade = premade;
    }
}

