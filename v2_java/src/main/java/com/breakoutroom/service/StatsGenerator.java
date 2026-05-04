package com.breakoutroom.service;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.*;
import java.util.*;

/**
 * Helper functions for generating statistics and Excel files.
 *
 * Created by: 龍ONE
 * Date Created: November 26, 2020
 * Date Ported to Java: May 3, 2026
 */
public class StatsGenerator {
    private String eventName;
    private List<List<String>> pastGroups;
    private List<String[]> pastPairs;
    private int longestName;

    public StatsGenerator() {
        this.pastGroups = new ArrayList<>();
        this.pastPairs = new ArrayList<>();
        this.longestName = 0;
    }

    /**
     * Generate an Excel file with breakout room statistics.
     */
    public void generateExcel() throws IOException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the event name: ");
        this.eventName = scanner.nextLine();

        // Check if event exists and load past groups
        checkEventName();

        // Generate data frame (in our case, a map for Excel)
        Map<String, Map<String, Integer>> dataFrame = generateDataFrame();

        // Write data to Excel
        writeExcelFile(dataFrame);

        System.out.println("Excel file created: files/breakout_rooms_data.xlsx");
    }

    /**
     * Check if event exists in previous-rooms.txt and load past groups.
     */
    private void checkEventName() throws IOException {
        boolean eventExists = false;
        boolean pastRoomsExist = false;
        int groupNum = 0;

        File previousRoomsFile = new File("files/previous-rooms.txt");
        try (BufferedReader reader = new BufferedReader(new FileReader(previousRoomsFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.strip();

                if (line.equals("EVENT: " + this.eventName + " (Y)")) {
                    eventExists = true;
                    pastRoomsExist = true;
                } else if (pastRoomsExist && line.contains("EVENT:")) {
                    break;
                } else if (pastRoomsExist && !line.isEmpty()) {
                    this.pastGroups.add(Arrays.asList(line.split(", ")));
                } else if (pastRoomsExist && line.isEmpty()) {
                    groupNum++;
                }
            }
        }

        if (!eventExists || !pastRoomsExist) {
            System.out.println("Event was not found or event was found but there were no previous rooms.");
            System.exit(1);
        }

        // Create list of all previous pairs
        for (List<String> group : this.pastGroups) {
            if (group.size() > 0) {
                for (int p1 = 0; p1 < group.size(); p1++) {
                    for (int p2 = p1 + 1; p2 < group.size(); p2++) {
                        this.pastPairs.add(new String[]{group.get(p1).strip(), group.get(p2).strip()});
                    }
                }
            }
        }
    }

    /**
     * Generate a data frame (as a map) from past groups.
     */
    private Map<String, Map<String, Integer>> generateDataFrame() {
        // Get all unique participants
        Set<String> participants = new TreeSet<>();
        for (List<String> group : this.pastGroups) {
            for (String person : group) {
                participants.add(person.strip());
            }
        }

        // Create and fill data frame
        Map<String, Map<String, Integer>> dataFrame = new TreeMap<>();
        for (String person : participants) {
            dataFrame.put(person, new TreeMap<>());
            for (String other : participants) {
                dataFrame.get(person).put(other, 0);
            }
        }

        // Fill in pair counts
        for (String[] pair : this.pastPairs) {
            String p1 = pair[0].strip();
            String p2 = pair[1].strip();
            if (dataFrame.containsKey(p1) && dataFrame.get(p1).containsKey(p2)) {
                dataFrame.get(p1).put(p2, dataFrame.get(p1).get(p2) + 1);
                dataFrame.get(p2).put(p1, dataFrame.get(p2).get(p1) + 1);
            }
        }

        // Set diagonals to -1
        for (String person : participants) {
            dataFrame.get(person).put(person, -1);
        }

        // Find longest name
        this.longestName = participants.stream()
            .mapToInt(String::length)
            .max()
            .orElse(0);

        return dataFrame;
    }

    /**
     * Write data frame to Excel file.
     */
    private void writeExcelFile(Map<String, Map<String, Integer>> dataFrame) throws IOException {
        File directory = new File("files");
        if (!directory.exists()) {
            directory.mkdirs();
        }

        try (Workbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet(this.eventName);

            List<String> columns = new ArrayList<>(dataFrame.keySet());

            // Write header row
            Row headerRow = sheet.createRow(0);
            Cell headerCell = headerRow.createCell(0);
            headerCell.setCellValue("");

            for (int i = 0; i < columns.size(); i++) {
                Cell cell = headerRow.createCell(i + 1);
                cell.setCellValue(columns.get(i));
            }

            // Write data rows
            int rowNum = 1;
            for (String rowPerson : columns) {
                Row row = sheet.createRow(rowNum++);
                Cell rowLabelCell = row.createCell(0);
                rowLabelCell.setCellValue(rowPerson);

                for (int colNum = 0; colNum < columns.size(); colNum++) {
                    Cell cell = row.createCell(colNum + 1);
                    int value = dataFrame.get(rowPerson).get(columns.get(colNum));
                    if (value == -1) {
                        cell.setCellValue("X");
                    } else {
                        cell.setCellValue(value);
                    }
                }
            }

            // Set column widths
            sheet.setColumnWidth(0, this.longestName * 256);
            for (int i = 1; i <= columns.size(); i++) {
                sheet.setColumnWidth(i, this.longestName * 256);
            }

            // Write to file
            FileOutputStream outputStream = new FileOutputStream("files/breakout_rooms_data.xlsx");
            workbook.write(outputStream);
            outputStream.close();
        }
    }
}

