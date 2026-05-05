package com.breakout;

import com.breakout.output.ExcelExporter;
import com.breakout.parser.InputParser;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

/**
 * Main entry point for the Statistics Generator application.
 * Imports breakout room data to Excel files and creates statistics.
 */
public class StatsMain {
    public static void main(String[] args) throws IOException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the event name: ");
        String eventName = scanner.nextLine();

        // Load past groups for the event
        List<List<String>> pastGroups = new ArrayList<>();
        List<String[]> pastPairs = new ArrayList<>();

        checkEventName(eventName, pastGroups, pastPairs);

        // Generate Excel file
        ExcelExporter exporter = new ExcelExporter();
        exporter.setEventName(eventName);
        exporter.setPastGroups(pastGroups);
        exporter.setPastPairs(pastPairs);

        Map<String, Map<String, Integer>> dataFrame = exporter.generateDataFrame();
        exporter.exportToExcel(dataFrame);

        System.out.println("Excel file created: files/breakout_rooms_data.xlsx");
    }

    /**
     * Check if event exists in previous-rooms.txt and load past groups.
     */
    private static void checkEventName(String eventName,
                                       List<List<String>> pastGroups,
                                       List<String[]> pastPairs) throws IOException {
        boolean pastRoomsExist = false;

        File previousRoomsFile = new File("files/previous-rooms.txt");
        try (BufferedReader reader = new BufferedReader(new FileReader(previousRoomsFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.strip();

                if (line.equals("EVENT: " + eventName + " (Y)")) {
                    pastRoomsExist = true;
                } else if (pastRoomsExist && line.contains("EVENT:")) {
                    break;
                } else if (pastRoomsExist && !line.isEmpty()) {
                    pastGroups.add(Arrays.asList(line.split(", ")));
                }
            }
        }

        if (!pastRoomsExist) {
            System.out.println("Event was not found or event was found but there were no previous rooms.");
            System.exit(1);
        }

        // Create list of all previous pairs
        for (List<String> group : pastGroups) {
            if (group.size() > 0) {
                for (int p1 = 0; p1 < group.size(); p1++) {
                    for (int p2 = p1 + 1; p2 < group.size(); p2++) {
                        pastPairs.add(new String[]{group.get(p1).strip(), group.get(p2).strip()});
                    }
                }
            }
        }
    }
}

