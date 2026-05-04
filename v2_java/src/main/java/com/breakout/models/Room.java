package com.breakout.models;

import java.io.IOException;
import java.util.*;

/**
 * Represents a collection of breakout rooms for event participants.
 *
 * Created by: 龍ONE
 * Date Created: January 25, 2021
 * Date Ported to Java: May 3, 2026
 */
public class Room {
    private List<PeopleList> rooms;
    private Map<String, Double> pastGroups;
    private int peoplePerRoom;
    private PeopleList peoplePresent;
    private int premadeGroupsCount;
    private int oldPairs;
    private int totalPairs;

    public Room(Map<String, Double> pastGroups, int peoplePerRoom,
                          PeopleList peoplePresent, PeopleList peoplePresentF,
                          PeopleList peoplePresentM, List<PeopleList> premadeGroups) {
        this.pastGroups = pastGroups;
        this.peoplePerRoom = peoplePerRoom;
        this.peoplePresent = peoplePresent;

        // Set premade groups count
        if (premadeGroups == null) {
            this.premadeGroupsCount = 0;
        } else {
            this.premadeGroupsCount = premadeGroups.size();
        }

        // Create empty rooms
        int roomCount = (int) Math.floor(peoplePresent.size() / (double) peoplePerRoom) + this.premadeGroupsCount;
        this.rooms = new ArrayList<>();
        for (int i = 0; i < roomCount; i++) {
            this.rooms.add(new PeopleList());
        }

        // Add premade groups to the end
        if (premadeGroups != null) {
            for (int i = 0; i < premadeGroups.size(); i++) {
                PeopleList group = premadeGroups.get(i);
                int roomIndex = this.rooms.size() - premadeGroups.size() + i;
                this.rooms.set(roomIndex, group);
                group.setPremade(true);
            }
        }

        // Fill rooms
        this.fillRooms(peoplePresentF, peoplePresentM);
    }

    /**
     * Add a person to a room (either randomly or optimally based on past groups).
     */
    public void addPerson(Person person) throws IOException {
        if (this.pastGroups == null || this.pastGroups.isEmpty()) {
            // Random placement
            Random rand = new Random();
            int roomNum;
            do {
                roomNum = rand.nextInt(this.rooms.size() - this.premadeGroupsCount);
            } while (this.rooms.get(roomNum).size() >= this.peoplePerRoom);

            this.rooms.get(roomNum).add(person);
            this.peoplePresent.add(person);
            System.out.println(person + " was added to Room " + (roomNum + 1));
        } else {
            // Optimal placement based on past groups
            List<Integer> roomSizes = getRoomSizes();
            int bestRoom = -1;
            double lowestEv = Double.POSITIVE_INFINITY;

            Room tempRooms = this.copy();
            for (int index = 0; index < tempRooms.rooms.size(); index++) {
                if (roomSizes.get(index) > this.peoplePerRoom) {
                    continue;
                }
                tempRooms.rooms.get(index).add(person);
                double ev = tempRooms.errorVal();
                if (ev < lowestEv) {
                    bestRoom = index;
                    lowestEv = ev;
                }
            }

            this.rooms.get(bestRoom).add(person);
            this.peoplePresent.add(person);
            System.out.println(person + " was added to Room " + (bestRoom + 1));
        }

        this.printRooms();
    }

    /**
     * Balance rooms by moving people from oversized to undersized rooms.
     */
    public void balanceRooms(boolean output) {
        List<Integer> roomSizes = getRoomSizes();
        while (roomSizes.contains(this.peoplePerRoom + 1) && roomSizes.contains(this.peoplePerRoom - 1)) {
            // Find people eligible to move
            List<int[]> moveList = new ArrayList<>();
            for (int index = 0; index < this.rooms.size(); index++) {
                if (this.rooms.get(index).size() == this.peoplePerRoom + 1) {
                    for (Person person : this.rooms.get(index).getList()) {
                        if (!person.isLeader() && !person.isNewcomer()) {
                            moveList.add(new int[]{index, moveList.size()});
                        }
                    }
                }
            }

            // Find rooms needing people
            List<Integer> fillRooms = new ArrayList<>();
            for (int index = 0; index < this.rooms.size(); index++) {
                if (this.rooms.get(index).size() == this.peoplePerRoom - 1 && !this.rooms.get(index).isPremade()) {
                    fillRooms.add(index);
                }
            }

            if (moveList.isEmpty() || fillRooms.isEmpty()) {
                break;
            }

            moveToRooms(fillRooms, moveList, output);
            roomSizes = getRoomSizes();
        }
    }

    /**
     * Create a deep copy of this Room object.
     */
    public Room copy() {
        Room copy = new Room(
            new HashMap<>(this.pastGroups),
            this.peoplePerRoom,
            copyPeopleList(this.peoplePresent),
            new PeopleList(),
            new PeopleList(),
            null
        );
        copy.rooms = new ArrayList<>();
        for (PeopleList room : this.rooms) {
            PeopleList newRoom = copyPeopleList(room);
            newRoom.setPremade(room.isPremade());
            copy.rooms.add(newRoom);
        }
        copy.premadeGroupsCount = this.premadeGroupsCount;
        return copy;
    }

    /**
     * Create a copy of a PeopleList.
     */
    private PeopleList copyPeopleList(PeopleList original) {
        PeopleList copy = new PeopleList();
        for (Person person : original.getList()) {
            copy.add(person);
        }
        return copy;
    }

    /**
     * Prompt user to edit rooms (add/remove people).
     */
    public void editRooms() throws IOException {
        System.out.println("Would you like the option to edit this breakout room?");
        Scanner scanner = new Scanner(System.in);
        String userResponse = "";
        while (!userResponse.equalsIgnoreCase("y") && !userResponse.equalsIgnoreCase("n")) {
            System.out.println("Enter Y for yes, N for no");
            userResponse = scanner.nextLine();
        }

        if (userResponse.equalsIgnoreCase("n")) {
            return;
        }

        userResponse = "";
        while (!userResponse.equals("3")) {
            System.out.println("Enter one of the following numbers to edit rooms:");
            System.out.println("1. Add new person");
            System.out.println("2. Remove existing person");
            System.out.println("3. End program");
            userResponse = scanner.nextLine();

            if (userResponse.equals("1") || userResponse.equals("2")) {
                System.out.println("Enter the name of the person");
                String name = scanner.nextLine();
                if (userResponse.equals("1")) {
                    this.addPerson(new Person(name));
                } else {
                    this.removePerson(name);
                }
            }
        }
    }

    /**
     * Calculate error value based on how many past pairs are in same room.
     */
    public double errorVal() {
        if (this.pastGroups == null || this.pastGroups.isEmpty()) {
            return 0.0;
        }

        double ev = 0.0;
        this.oldPairs = 0;
        this.totalPairs = 0;

        List<PeopleList> roomsToCheck = this.rooms;
        if (this.premadeGroupsCount > 0) {
            roomsToCheck = this.rooms.subList(0, this.rooms.size() - this.premadeGroupsCount);
        }

        for (PeopleList room : roomsToCheck) {
            for (int p1 = 0; p1 < room.size(); p1++) {
                for (int p2 = p1 + 1; p2 < room.size(); p2++) {
                    String key1 = room.get(p1).getName() + "," + room.get(p2).getName();
                    String key2 = room.get(p2).getName() + "," + room.get(p1).getName();

                    if (this.pastGroups.containsKey(key1)) {
                        ev += this.pastGroups.get(key1);
                        this.oldPairs++;
                    } else if (this.pastGroups.containsKey(key2)) {
                        ev += this.pastGroups.get(key2);
                        this.oldPairs++;
                    }
                    this.totalPairs++;
                }
            }
        }

        if (this.totalPairs > 0) {
            ev *= (1 - (1.0 - (double) this.oldPairs / this.totalPairs));
        }
        return ev;
    }

    /**
     * Fill rooms with people, balancing gender and leader/newcomer status.
     */
    private void fillRooms(PeopleList peoplePresentF, PeopleList peoplePresentM) {
        // Randomize lists
        peoplePresentF.randomize();
        peoplePresentM.randomize();

        int roomNumF = 0;
        int roomNumM = -1;

        // Place female leaders
        roomNumF = placeInRooms(
            peoplePresentF.getList().stream()
                .filter(Person::isLeader)
                .toList(),
            roomNumF
        );

        // Place male leaders
        roomNumM = placeInRooms(
            peoplePresentM.getList().stream()
                .filter(Person::isLeader)
                .toList(),
            roomNumF
        );

        // Push newcomers to front
        peoplePresentF.pushNewcomers();
        peoplePresentM.pushNewcomers();

        // Place remaining females
        roomNumF = placeInRooms(
            peoplePresentF.getList().stream()
                .filter(p -> !p.isLeader())
                .toList(),
            roomNumF
        );

        // Place remaining males
        if (roomNumM == -1) {
            roomNumM = roomNumF;
        }
        placeInRooms(
            peoplePresentM.getList().stream()
                .filter(p -> !p.isLeader())
                .toList(),
            roomNumM
        );

        // Balance rooms if no past groups
        if (this.pastGroups == null || this.pastGroups.isEmpty()) {
            this.balanceRooms(false);
        }
    }

    /**
     * Get the room number where a person is located.
     */
    public int getRoomNum(String name) {
        for (int index = 0; index < this.rooms.size(); index++) {
            for (Person person : this.rooms.get(index).getList()) {
                if (person.getName().equals(name)) {
                    return index;
                }
            }
        }
        return -1;
    }

    /**
     * Get sizes of all rooms (excluding premade groups).
     */
    public List<Integer> getRoomSizes() {
        List<Integer> roomSizes = new ArrayList<>();
        for (int i = 0; i < this.rooms.size() - this.premadeGroupsCount; i++) {
            roomSizes.add(this.rooms.get(i).size());
        }
        return roomSizes;
    }

    /**
     * Move people to fill rooms.
     */
    private void moveToRooms(List<Integer> fillRooms, List<int[]> moveList, boolean output) {
        // TODO: Implement movement logic
    }

    /**
     * Place people in rooms sequentially.
     */
    private int placeInRooms(List<Person> peopleList, int roomNum) {
        for (Person person : peopleList) {
            this.rooms.get(roomNum).add(person);
            roomNum++;
            if (roomNum > this.rooms.size() - 1 - this.premadeGroupsCount) {
                roomNum = 0;
            }
        }
        return roomNum;
    }

    /**
     * Print all rooms to console.
     */
    public void printRooms() {
        // Sort names in each room
        for (PeopleList room : this.rooms) {
            room.getList().sort(Comparator.comparing(Person::getName));
        }

        // Print rooms
        for (int index = 0; index < this.rooms.size(); index++) {
            List<String> names = new ArrayList<>();
            for (Person person : this.rooms.get(index).getList()) {
                names.add(person.toString());
            }
            System.out.println("Breakout Room " + (index + 1) + ": " + String.join(", ", names));
        }

        // Print error value
        double ev = errorVal();
        System.out.printf("Error Val: %.2f%n", ev);

        // Print new pairs info if past groups exist
        if (this.pastGroups != null && !this.pastGroups.isEmpty()) {
            System.out.printf("New pairs: %d out of %d (%.2f%%)%n",
                this.totalPairs - this.oldPairs,
                this.totalPairs,
                (this.totalPairs > 0 ? (1 - (double) this.oldPairs / this.totalPairs) * 100 : 0)
            );
        }
        System.out.println();
    }

    /**
     * Remove a person from rooms.
     */
    public void removePerson(String name) {
        int roomNum = getRoomNum(name);
        if (roomNum == -1) {
            System.out.println(name + " is not currently in a breakout room");
            return;
        }

        this.rooms.get(roomNum).remove(name);
        this.peoplePresent.remove(name);
        this.balanceRooms(true);
        System.out.println(name + " was removed from Room " + (roomNum + 1));
        this.printRooms();
    }

    /**
     * Swap two people between rooms.
     */
    public void swap(Person p1, Person p2) {
        int roomNum1 = getRoomNum(p1.getName());
        int roomNum2 = getRoomNum(p2.getName());

        this.rooms.get(roomNum1).remove(p1.getName());
        this.rooms.get(roomNum1).add(p2);
        this.rooms.get(roomNum2).remove(p2.getName());
        this.rooms.get(roomNum2).add(p1);
    }

    // Getters
    public List<PeopleList> getRooms() {
        return rooms;
    }

    public int getPremadeGroupsCount() {
        return premadeGroupsCount;
    }

    public int getOldPairs() {
        return oldPairs;
    }

    public int getTotalPairs() {
        return totalPairs;
    }
}

