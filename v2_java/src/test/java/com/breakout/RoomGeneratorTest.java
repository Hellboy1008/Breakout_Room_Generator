package com.breakout;

import com.breakout.generator.RoomGenerator;
import com.breakout.models.Person;
import com.breakout.models.PeopleList;
import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;

/**
 * Unit tests for RoomGenerator.
 *
 * Date Created: May 3, 2026
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
        Person person = new Person("John Doe");

        list.add(person);
        assertEquals(1, list.size());
        assertFalse(list.isEmpty());
        assertEquals(person, list.get(0));
    }

    @Test
    public void testPersonParsing() {
        Person newPerson = new Person("Jane Smith (N)");
        assertTrue(newPerson.isNewcomer());

        Person groupPerson = new Person("Bob Jones (G1)");
        assertEquals(1, groupPerson.getGroup());
    }

    @Test
    public void testPeopleListRemove() {
        PeopleList list = new PeopleList();
        list.add(new Person("Alice"));
        list.add(new Person("Bob"));
        list.add(new Person("Charlie"));

        assertEquals(3, list.size());
        list.remove("Bob");
        assertEquals(2, list.size());
    }
}

