package com.breakout.generator;

import com.breakout.models.Person;
import com.breakout.models.PeopleList;
import com.breakout.models.Room;

import java.util.Map;

/**
 * Scoring and optimization engine for breakout room generation.
 * Handles algorithm logic for finding optimal room configurations.
 */
public class ScoringEngine {
    private static final int GREEDY_TRIALS = 5000;
    private static final int SIMULATED_ANNEALING_TRIALS = 2500;

    private PeopleList peoplePresentF;
    private PeopleList peoplePresentM;
    private Map<String, Double> pastGroups;
    private int peoplePerRoom;
    private PeopleList peoplePresent;
    private java.util.List<PeopleList> premadeGroups;

    public ScoringEngine(PeopleList peoplePresent,
                         PeopleList peoplePresentF,
                         PeopleList peoplePresentM,
                         Map<String, Double> pastGroups,
                         int peoplePerRoom,
                         java.util.List<PeopleList> premadeGroups) {
        this.peoplePresent = peoplePresent;
        this.peoplePresentF = peoplePresentF;
        this.peoplePresentM = peoplePresentM;
        this.pastGroups = pastGroups;
        this.peoplePerRoom = peoplePerRoom;
        this.premadeGroups = premadeGroups;
    }

    /**
     * Generate optimal breakout rooms using greedy and simulated annealing algorithms.
     */
    public Room generateOptimalRooms() {
        Room bestRoom = null;
        double lowestEv = Double.POSITIVE_INFINITY;

        // Greedy algorithm
        for (int count = 0; count < GREEDY_TRIALS; count++) {
            System.out.print("Applying algorithm 1... " + (count + 1) + "/" + GREEDY_TRIALS + "\r");

            Room room = new Room(
                this.pastGroups,
                this.peoplePerRoom,
                this.peoplePresent,
                this.peoplePresentF,
                this.peoplePresentM,
                this.premadeGroups
            );

            double ev = room.errorVal();
            if (ev < lowestEv) {
                bestRoom = room.copy();
                lowestEv = ev;
            }

            if (lowestEv == 0) {
                break;
            }
        }

        if (bestRoom != null) {
            bestRoom.balanceRooms(false);
        }
        System.out.println("\nAlgorithm 1 completed");

        // Simulated annealing
        for (int count = 0; count < SIMULATED_ANNEALING_TRIALS; count++) {
            System.out.print("Applying algorithm 2... " + (count + 1) + "/" + SIMULATED_ANNEALING_TRIALS + "\r");

            boolean validPair = false;
            Person p1 = null, p2 = null;

            // Find a valid pair to switch
            while (!validPair) {
                java.util.Random rand = new java.util.Random();
                PeopleList selectedList;
                if (rand.nextInt(2) == 0) {
                    this.peoplePresentF.randomize();
                    selectedList = this.peoplePresentF;
                } else {
                    this.peoplePresentM.randomize();
                    selectedList = this.peoplePresentM;
                }

                p1 = selectedList.get(0);
                p2 = selectedList.get(1);

                if (p1.leader() == p2.leader() &&
                    p1.newcomer() == p2.newcomer() &&
                    bestRoom.getRoomNum(p1.name()) != bestRoom.getRoomNum(p2.name())) {
                    validPair = true;
                }
            }

            Room tempRooms = bestRoom.copy();
            tempRooms.swap(p1, p2);
            double ev = tempRooms.errorVal();

            if (ev < lowestEv) {
                bestRoom = tempRooms.copy();
                lowestEv = ev;
            }

            if (lowestEv == 0) {
                break;
            }
        }

        System.out.println("\nAlgorithm 2 completed");
        return bestRoom;
    }

    public int getGreedyTrials() {
        return GREEDY_TRIALS;
    }

    public int getSimulatedAnnealingTrials() {
        return SIMULATED_ANNEALING_TRIALS;
    }
}

