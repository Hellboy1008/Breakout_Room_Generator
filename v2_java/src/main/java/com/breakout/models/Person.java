package com.breakout.models;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

/**
 * Represents a person participating in a breakout room.
 *
 * Created by: 龍ONE
 * Date Created: February 1, 2021
 * Date Ported to Java: May 3, 2026
 */
public class Person {
    private String name;
    private int group;
    private boolean newcomer;
    private String gender;
    private boolean leader;

    public Person(String name) {
        this.parseNameAndGroup(name);
        this.addGender();
    }

    /**
     * Parse the person's name and extract group/newcomer information from notation.
     * Notation: (N) for newcomer, (G#) for premade group
     */
    private void parseNameAndGroup(String name) {
        // Check if person is a newcomer or in a premade group
        if (name.contains("(N)")) {
            this.group = 0;
            this.newcomer = true;
        } else if (name.contains("(G")) {
            int startIdx = name.indexOf("(G") + 2;
            int endIdx = name.indexOf("(G") + 3;
            this.group = Integer.parseInt(name.substring(startIdx, endIdx));
            this.newcomer = false;
        } else {
            this.group = 0;
            this.newcomer = false;
        }

        // Remove special notations from name
        if (name.contains("(")) {
            this.name = name.substring(0, name.indexOf("(")).trim();
        } else {
            this.name = name;
        }

        this.leader = false;
    }

    /**
     * Add gender and leader status from master file.
     */
    private void addGender() {
        this.gender = null;
        File masterFile = new File("files/master.txt");

        try (BufferedReader reader = new BufferedReader(new FileReader(masterFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.contains(this.name)) {
                    if (line.contains("(M")) {
                        this.gender = "M";
                    } else {
                        this.gender = "F";
                    }
                    if (line.contains(",L)")) {
                        this.leader = true;
                    } else {
                        this.leader = false;
                    }
                    break;
                }
            }
        } catch (IOException e) {
            // Master file not found, will prompt user for gender
        }

        // If gender not found in master file, prompt user
        if (this.gender == null) {
            this.leader = false;
            this.gender = promptForGender();
        }
    }

    /**
     * Prompt user for gender input.
     */
    private String promptForGender() {
        java.util.Scanner scanner = new java.util.Scanner(System.in);
        String gender = "";
        while (!gender.equalsIgnoreCase("M") && !gender.equalsIgnoreCase("F")) {
            System.out.println("Input the gender for: " + this.name);
            System.out.println("Type M for male, F for female");
            gender = scanner.nextLine();
        }
        return gender.equalsIgnoreCase("M") ? "M" : "F";
    }

    @Override
    public String toString() {
        return this.name;
    }

    // Getters and setters
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getGroup() {
        return group;
    }

    public void setGroup(int group) {
        this.group = group;
    }

    public boolean isNewcomer() {
        return newcomer;
    }

    public void setNewcomer(boolean newcomer) {
        this.newcomer = newcomer;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public boolean isLeader() {
        return leader;
    }

    public void setLeader(boolean leader) {
        this.leader = leader;
    }
}

