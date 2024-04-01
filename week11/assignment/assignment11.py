"""
Course: CSE 251
Lesson Week: 10
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE = 'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE = 'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'


def cleaner_waiting():
    time.sleep(random.uniform(0, 2))


def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))


def guest_waiting():
    time.sleep(random.uniform(0, 2))


def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))


def cleaner(cart, clean, start, id):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    # while loop to check time
    while (time.time() - start < TIME):

        # waiting for room to be available
        cleaner_waiting()

        # locks toom and sends in cleaners
        with cart:
            # starts cleaning
            print(STARTING_CLEANING_MESSAGE)
            cleaner_cleaning(id + 1)
            clean.value += 1
            print(STOPPING_CLEANING_MESSAGE)
            # ends cleaning


def guest(light, cart, party, start, room, id):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while (time.time() - start < TIME):
        # waiting for room to become available
        guest_waiting()
        with light:
            room.value += 1
            party.value += 1

            # turns on lights
            if room.value == 1:
                cart.acquire()
                print(STARTING_PARTY_MESSAGE)
        guest_partying(id + 1)
        with light:
            # turns off lights if last guest leaves the room
            if room.value == 1:
                print(STOPPING_PARTY_MESSAGE)
                cart.release()
            room.value -= 1


def main():
    # Start time of the running of the program.
    start_time = time.time()

    # TODO - add any variables, data structures, processes you need
    cleaned_count = mp.Value('i', 0)
    party_count = mp.Value('i', 0)
    room = mp.Value('i', 0)
    cart = mp.Lock()
    light = mp.Lock()

    # TODO - add any arguments to cleaner() and guest() that you need
    guests = [mp.Process(target=(guest), args=(
        light, cart, party_count, start_time, room, i))for i in range(HOTEL_GUESTS)]
    cleaners = [mp.Process(target=(cleaner), args=(
        cart, cleaned_count, start_time, i))for i in range(CLEANING_STAFF)]

    # starts guests and cleaners
    for g in guests:
        g.start()
    for c in cleaners:
        c.start()

    # ends guests and cleaners after a hard days work and partying
    for g in guests:
        g.join()
    for c in cleaners:
        c.join()

    # Results
    print(
        f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()
