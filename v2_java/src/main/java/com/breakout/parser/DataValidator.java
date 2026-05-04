package com.breakout.parser;

import com.breakout.models.Person;
import com.breakout.models.PeopleList;

import java.io.File;

/**
 * Validates input data and file integrity.
 *
 * Date Ported to Java: May 3, 2026
 */
public class DataValidator {

    /**
     * Validate that required input files exist.
     */
    public static boolean validateInputFiles() {
        String[] requiredFiles = {
            "files/present.txt",
            "files/master.txt"
        };

        for (String filePath : requiredFiles) {
            File file = new File(filePath);
            if (!file.exists()) {
                System.err.println("Error: Required file not found: " + filePath);
                return false;
            }
        }
        return true;
    }

    /**
     * Validate that people list is not empty.
     */
    public static boolean validatePeopleList(PeopleList peopleList) {
        if (peopleList == null || peopleList.isEmpty()) {
            System.err.println("Error: People list is empty");
            return false;
        }
        return true;
    }

    /**
     * Validate people per room setting.
     */
    public static boolean validatePeoplePerRoom(int peoplePerRoom, int totalPeople) {
        if (peoplePerRoom <= 0) {
            System.err.println("Error: People per room must be greater than 0");
            return false;
        }
        if (peoplePerRoom > totalPeople) {
            System.err.println("Error: People per room cannot exceed total number of people");
            return false;
        }
        return true;
    }

    /**
     * Validate event name.
     */
    public static boolean validateEventName(String eventName) {
        if (eventName == null || eventName.trim().isEmpty()) {
            System.err.println("Error: Event name cannot be empty");
            return false;
        }
        return true;
    }

    /**
     * Validate person data.
     */
    public static boolean validatePerson(Person person) {
        if (person == null) {
            System.err.println("Error: Person is null");
            return false;
        }
        if (person.getName() == null || person.getName().isEmpty()) {
            System.err.println("Error: Person name cannot be empty");
            return false;
        }
        if (person.getGender() == null || (!person.getGender().equals("M") && !person.getGender().equals("F"))) {
            System.err.println("Error: Invalid gender for " + person.getName());
            return false;
        }
        return true;
    }

    /**
     * Check if output directory exists, create if needed.
     */
    public static boolean ensureOutputDirectory() {
        File directory = new File("files");
        if (!directory.exists()) {
            boolean created = directory.mkdirs();
            if (!created) {
                System.err.println("Error: Could not create output directory");
                return false;
            }
        }
        return true;
    }
}

