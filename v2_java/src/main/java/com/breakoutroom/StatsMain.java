package com.breakoutroom;

import com.breakoutroom.service.StatsGenerator;

import java.io.IOException;

/**
 * Main entry point for the Statistics Generator application.
 *
 * Created by: 龍ONE
 * Date Created: October 5, 2020
 * Date Ported to Java: May 3, 2026
 *
 * Purpose:
 * Import breakout room data to excel file and create a text file for statistics.
 */
public class StatsMain {
    public static void main(String[] args) throws IOException {
        StatsGenerator generator = new StatsGenerator();
        generator.generateExcel();
    }
}

