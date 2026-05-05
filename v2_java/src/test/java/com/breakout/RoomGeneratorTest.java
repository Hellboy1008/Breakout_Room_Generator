package com.breakout;

import com.breakout.generator.RoomGenerator;
import com.breakout.models.Person;
import com.breakout.models.PeopleList;
import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;

/**
 * Unit tests for RoomGenerator.
 */
public class RoomGeneratorTest {

    private RoomGenerator generator;

    @Before
    public void setUp() {
        generator = new RoomGenerator();
    }

    @Test
    public void testRoomGeneratorInitialization() {
        assertNotNull(generator);
        assertNotNull(generator.getPeoplePresent());
        assertNotNull(generator.getPastGroups());
        assertEquals(0, generator.getPremadeGroups().size());
    }

    @Test
    public void testPeopleListOperations() {
        PeopleList list = new PeopleList();
        Person person = Person.of("John Doe");

        list.add(person);
        assertEquals(1, list.size());
        assertFalse(list.isEmpty());
        assertEquals(person, list.get(0));
    }

    @Test
    public void testPersonParsing() {
        Person newPerson = Person.of("Jane Smith (N)");
        assertTrue(newPerson.newcomer());

        Person groupPerson = Person.of("Bob Jones (G1)");
        assertEquals(1, groupPerson.group());
    }

    @Test
    public void testPeopleListRemove() {
        PeopleList list = new PeopleList();
        list.add(Person.of("Alice"));
        list.add(Person.of("Bob"));
        list.add(Person.of("Charlie"));

        assertEquals(3, list.size());
        list.remove("Bob");
        assertEquals(2, list.size());
    }
}

