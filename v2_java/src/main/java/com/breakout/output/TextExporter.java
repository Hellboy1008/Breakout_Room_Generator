package com.breakout.output;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;

/**
 * Exports breakout room data to text format.
 */
public class TextExporter {

    /**
     * Export room configuration to a text file.
     */
    public void exportRoomsToText(String eventName, List<List<String>> rooms) throws IOException {
        File directory = new File("files");
        if (!directory.exists()) {
            directory.mkdirs();
        }

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String timestamp = LocalDateTime.now().format(formatter);

        String filename = "files/" + eventName + "_rooms_" + timestamp.replace(":", "-") + ".txt";

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            writer.write("EVENT: " + eventName);
            writer.newLine();
            writer.write("Generated: " + timestamp);
            writer.newLine();
            writer.write("=".repeat(50));
            writer.newLine();
            writer.newLine();

            for (int i = 0; i < rooms.size(); i++) {
                writer.write("Room " + (i + 1) + ":");
                writer.newLine();
                for (String person : rooms.get(i)) {
                    writer.write("  - " + person);
                    writer.newLine();
                }
                writer.newLine();
            }
        }

        System.out.println("Rooms exported to: " + filename);
    }

    /**
     * Export statistics summary to text file.
     */
    public void exportStatisticsToText(String eventName, Map<String, Integer> statistics) throws IOException {
        File directory = new File("files");
        if (!directory.exists()) {
            directory.mkdirs();
        }

        String filename = "files/" + eventName + "_statistics.txt";

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            writer.write("STATISTICS FOR EVENT: " + eventName);
            writer.newLine();
            writer.write("Generated: " + LocalDateTime.now());
            writer.newLine();
            writer.write("=".repeat(50));
            writer.newLine();
            writer.newLine();

            for (Map.Entry<String, Integer> entry : statistics.entrySet()) {
                writer.write(entry.getKey() + ": " + entry.getValue());
                writer.newLine();
            }
        }

        System.out.println("Statistics exported to: " + filename);
    }

    /**
     * Export pair frequency matrix to text file.
     */
    public void exportPairFrequencyToText(String eventName, Map<String, Map<String, Integer>> pairFrequency) throws IOException {
        File directory = new File("files");
        if (!directory.exists()) {
            directory.mkdirs();
        }

        String filename = "files/" + eventName + "_pair_frequency.txt";

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            writer.write("PAIR FREQUENCY MATRIX FOR EVENT: " + eventName);
            writer.newLine();
            writer.write("Generated: " + LocalDateTime.now());
            writer.newLine();
            writer.write("=".repeat(50));
            writer.newLine();
            writer.newLine();

            // Get all people
            java.util.Set<String> people = pairFrequency.keySet();

            // Write header
            writer.write("Person");
            for (String person : people) {
                writer.write("\t" + person);
            }
            writer.newLine();

            // Write data
            for (String person1 : people) {
                writer.write(person1);
                for (String person2 : people) {
                    int frequency = pairFrequency.getOrDefault(person1, new java.util.HashMap<>())
                        .getOrDefault(person2, 0);
                    writer.write("\t" + frequency);
                }
                writer.newLine();
            }
        }

        System.out.println("Pair frequency exported to: " + filename);
    }
}

