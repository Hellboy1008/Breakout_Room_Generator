package com.breakout.output;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.*;

/**
 * Exports breakout room statistics to Excel format.
 */
public class ExcelExporter {
    private String eventName;
    private List<List<String>> pastGroups;
    private List<String[]> pastPairs;
    private int longestName;

    public ExcelExporter() {
        this.pastGroups = new ArrayList<>();
        this.pastPairs = new ArrayList<>();
        this.longestName = 0;
    }

    /**
     * Create a data frame from past groups and write to Excel.
     */
    public void exportToExcel(Map<String, Map<String, Integer>> dataFrame) throws IOException {
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

    /**
     * Generate data frame (as a map) from past groups.
     */
    public Map<String, Map<String, Integer>> generateDataFrame() {
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

    // Getters
    public String getEventName() {
        return eventName;
    }

    public void setEventName(String eventName) {
        this.eventName = eventName;
    }

    public List<List<String>> getPastGroups() {
        return pastGroups;
    }

    public void setPastGroups(List<List<String>> pastGroups) {
        this.pastGroups = pastGroups;
    }

    public List<String[]> getPastPairs() {
        return pastPairs;
    }

    public void setPastPairs(List<String[]> pastPairs) {
        this.pastPairs = pastPairs;
    }
}

