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
     * Get all names in the list.
     */
    public List<String> getNames() {
        List<String> names = new ArrayList<>();
        for (Person person : this.list) {
            names.add(person.getName());
        }
        return names;
    }

    /**
     * Remove and return the first person from the list.
     */
    public Person pop() {
        if (this.list.isEmpty()) {
            return null;
        }
        Person person = this.list.get(0);
        this.list.remove(0);
        return person;
    }

    /**
     * Move all newcomers to the front of the list.
     */
    public void pushNewcomers() {
        List<Person> newcomers = new ArrayList<>();
        List<Person> nonNewcomers = new ArrayList<>();

        for (Person person : this.list) {
            if (person.isNewcomer()) {
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
        this.list.removeIf(person -> person.getName().equals(personName));
    }

    @Override
    public String toString() {
        return this.list.toString();
    }

    public List<Person> getList() {
        return list;
    }

    public void setList(List<Person> list) {
        this.list = list;
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

