package com.breakout.models;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

/**
 * Represents a person participating in a breakout room.
 * Parses special name notations: (N) for newcomer, (G#) for premade groups.
 * Loads gender and leader status from master file.
 */
public record Person(String name, int group, boolean newcomer, String gender, boolean leader) {

    public static Person of(String rawName) {
        String parsedName;
        int group;
        boolean newcomer;

        if (rawName.contains("(N)")) {
            group = 0;
            newcomer = true;
        } else if (rawName.contains("(G")) {
            int startIdx = rawName.indexOf("(G") + 2;
            int endIdx = rawName.indexOf("(G") + 3;
            group = Integer.parseInt(rawName.substring(startIdx, endIdx));
            newcomer = false;
        } else {
            group = 0;
            newcomer = false;
        }

        if (rawName.contains("(")) {
            parsedName = rawName.substring(0, rawName.indexOf("(")).trim();
        } else {
            parsedName = rawName;
        }

        String gender = null;
        boolean leader = false;
        File masterFile = new File("files/master.txt");

        try (BufferedReader reader = new BufferedReader(new FileReader(masterFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.contains(parsedName)) {
                    gender = line.contains("(M") ? "M" : "F";
                    leader = line.contains(",L)");
                    break;
                }
            }
        } catch (IOException e) {
            // Master file not found, will prompt user for gender
        }

        if (gender == null) {
            gender = promptForGender(parsedName);
        }

        return new Person(parsedName, group, newcomer, gender, leader);
    }

    private static String promptForGender(String name) {
        java.util.Scanner scanner = new java.util.Scanner(System.in);
        String gender = "";
        while (!gender.equalsIgnoreCase("M") && !gender.equalsIgnoreCase("F")) {
            System.out.println("Input the gender for: " + name);
            System.out.println("Type M for male, F for female");
            gender = scanner.nextLine();
        }
        return gender.equalsIgnoreCase("M") ? "M" : "F";
    }

    @Override
    public String toString() {
        return name;
    }
}
