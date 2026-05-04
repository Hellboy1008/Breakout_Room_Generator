package com.breakoutroom;

import com.breakoutroom.service.RoomGenerator;

import java.io.IOException;

/**
 * Main entry point for the Breakout Room Generator application.
 *
 * Created by: 龍ONE
 * Date Created: October 1, 2020
 * Date Ported to Java: May 3, 2026
 *
 * Purpose:
 * Generate zoom breakout rooms given a list of people. The user can determine
 * whether they want to create rooms with emphasis on the size of the rooms or
 * the overall balance (gender, leaders/newcomers) in the rooms.
 */
public class Main {
    public static void main(String[] args) throws IOException {
        RoomGenerator generator = new RoomGenerator();
        generator.generateBreakoutRooms();
    }
}

