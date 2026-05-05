package com.breakout;

import com.breakout.generator.ScoringEngine;
import com.breakout.models.Person;
import com.breakout.models.PeopleList;
import com.breakout.models.Room;
import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;

import java.util.HashMap;
import java.util.Map;

/**
 * Unit tests for ScoringEngine.
 */
public class ScoringEngineTest {

    private ScoringEngine engine;
    private PeopleList peoplePresent;
    private PeopleList peoplePresentF;
    private PeopleList peoplePresentM;
    private Map<String, Double> pastGroups;

    @Before
    public void setUp() {
        peoplePresent = new PeopleList();
        peoplePresentF = new PeopleList();
        peoplePresentM = new PeopleList();
        pastGroups = new HashMap<>();

        // Add test people
        Person p1 = Person.of("Alice");
        Person p2 = Person.of("Bob");
        Person p3 = Person.of("Charlie");
        Person p4 = Person.of("Diana");

        peoplePresent.add(p1);
        peoplePresent.add(p2);
        peoplePresent.add(p3);
        peoplePresent.add(p4);

        peoplePresentF.add(p1);
        peoplePresentF.add(p4);
        peoplePresentM.add(p2);
        peoplePresentM.add(p3);

        engine = new ScoringEngine(
            peoplePresent,
            peoplePresentF,
            peoplePresentM,
            pastGroups,
            2,
            null
        );
    }

    @Test
    public void testScoringEngineInitialization() {
        assertNotNull(engine);
        assertEquals(5000, engine.getGreedyTrials());
        assertEquals(2500, engine.getSimulatedAnnealingTrials());
    }

    @Test
    public void testErrorValCalculation() {
        // Create a simple room and test error value
        Room room = new Room(
            null,
            2,
            peoplePresent,
            peoplePresentF,
            peoplePresentM,
            null
        );

        double errorVal = room.errorVal();
        assertEquals(0.0, errorVal, 0.01);
    }

    @Test
    public void testEmptyPastGroups() {
        assertTrue(pastGroups.isEmpty());
        Room room = new Room(
            pastGroups,
            2,
            peoplePresent,
            peoplePresentF,
            peoplePresentM,
            null
        );

        double errorVal = room.errorVal();
        assertEquals(0.0, errorVal, 0.01);
    }
}

