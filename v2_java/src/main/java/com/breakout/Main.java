package com.breakout;

import com.breakout.generator.RoomGenerator;

import java.io.IOException;

/**
 * Main entry point for the Breakout Room Generator application.
 * Generates zoom breakout rooms given a list of people, with options for size balancing or overall balance.
 */
public class Main {
    public static void main(String[] args) throws IOException {
        RoomGenerator generator = new RoomGenerator();
        generator.generateBreakoutRooms();
    }
}

