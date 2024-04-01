'''
Requirements
1. Create a multiprocessing program that connects the processes using Pipes.
2. Create a process from each of the following custom process classes,
   Marble_Creator, Bagger, Assembler, and Wrapper.
3. The Marble_Creator process will send a marble to the Bagger process using
   a Pipe.
4. The Bagger process will create a Bag object with the required number of
   marbles.
5. The Bagger process will send the Bag object to the Assembler using a Pipe.
6. The Assembler process will create a Gift object and send it to the Wrapper
   process using a Pipe.
7. The Wrapper process will write to a file the current time followed by the
   gift string.
8. The program should not hard-code the number of marbles, the various delays,
   nor the bag count. These should be obtained from the settings.txt file.

Questions:
1. Why can you not use the same pipe object for all the processes (i.e., why
   do you need to create three different pipes)?
   >becuase it only transfers one data between functions.
   >
2. Compare and contrast pipes with queues (i.e., how are the similar or different)?
   >queues can go between any function and require locks while pipes are a one way tansfer without the need for locks.
   >
'''

import datetime
import json
import math
import multiprocessing as mp
from multiprocessing import Value
import multiprocessing.connection as pipe
import os
import random
import time

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables


class Bag():
    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
              'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
              'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby',
              'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
              'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
              'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
              'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
              'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
              'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
              'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
              'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
              'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
              'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
              'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self,
                 pipe: pipe.PipeConnection,
                 settings: dict
                 ):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.send = pipe
        self.marble_count = settings[MARBLE_COUNT]
        self.delay = settings[CREATOR_DELAY]

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        # loops to create all marbles accoding to marble count
        for i in range(self.marble_count):

            # sends random marble to bagger
            self.send.send(random.choice(Marble_Creator.colors))

        # signals bagger that there are no more marbels
        self.send.send(None)

        # closes pipe
        self.send.close()

        # Sleep a little.
        time.sleep(self.delay)


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """

    def __init__(self,
                 recieved: pipe.PipeConnection,
                 send: pipe.PipeConnection,
                 settings: dict,
                 Bag
                 ):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.send = send
        self.recv = recieved
        self.delay = settings[BAGGER_DELAY]
        self.bag = settings[BAG_COUNT]
        self.marble = settings[MARBLE_COUNT]
        self.q = Bag

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            marble = self.recv.recv()
            # checks to make sure there are more marbles to bag
            if marble != None:
                # add marble to bag
                self.q.add(marble)

                # Determines if bag is full and sends bag
                if self.q.get_size() == math.floor(self.marble/self.bag) + 1:
                    self.send.send(self.q)

                    # reinstintates bag
                    self.q = Bag()

                    # Bagger delay
                    time.sleep(self.delay)
                else:
                    pass
            else:
                # Sends partial bag (not enough marbles made)
                self.send.send(self.q)

                # sleep a little while
                time.sleep(self.delay)

                # None is the indicator that tells the Assembler it is done.
                self.send.send(None)
                break


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss',
                    'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self,
                 recieved: pipe.PipeConnection,
                 send: pipe.PipeConnection,
                 settings: dict,
                 Bag,
                 gifts
                 ):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.recv = recieved
        self.send = send
        self.delay = settings[ASSEMBLER_DELAY]
        self.q = Bag
        self.count = gifts

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            # pulls bag from Bagger
            self.q = self.recv.recv()

            # checks and make sure there are bags left
            if self.q != None:

                # creates Gifts
                line = Gift(random.choice(Assembler.marble_names), self.q)

                # sends Gift
                self.send.send(line)

                # counts ammount of gifts
                self.count.value += 1

                # sleep for a bit
                time.sleep(self.delay)
            else:
                self.send.send(None)
                time.sleep(self.delay)
                break


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """

    def __init__(self,
                 recieved: pipe.PipeConnection,
                 settings: dict
                 ):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.recv = recieved
        self.delay = settings[WRAPPER_DELAY]

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        (see prepare00.md for helpful file operations)
        '''
        while True:
            # pulls from assembeler
            line = self.recv.recv()

            # checks to see if there are more gifts
            if line != None:

                # Send Gifts to Boxes
                with open(BOXES_FILENAME, "a") as f:
                    f.write(str(line))
                    f.write('\n\n')

                # sleeps for a while
                time.sleep(self.delay)
            else:
                break


def display_final_boxes(filename):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        print(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                print(line.strip())
                print
    else:
        print(
            f'ERROR: The file {filename} doesn\'t exist.  No boxes were created.')


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    """ Main function """

    # Start a timer
    begin_time = time.perf_counter()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        print(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    print(f'Marble count                = {settings[MARBLE_COUNT]}')
    print(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    print(f'settings["bag-count"]       = {settings[BAG_COUNT]}')
    print(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    print(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    print(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    send_creator, recv_bagger = pipe.Pipe()
    send_bagger, recv_assemblr = pipe.Pipe()
    send_assemblr, recv_wrapper = pipe.Pipe()
    # TODO create variable to be used to count the number of gifts
    gifts = mp.Value('i', 0)
    bags = Bag()

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    print('Create the processes')

    # TODO Create the processes (ie., classes above)
    p1 = Marble_Creator(send_creator, settings)
    p2 = Bagger(recv_bagger, send_bagger, settings, bags)
    p3 = Assembler(recv_assemblr, send_assemblr,
                   settings, bags, gifts)
    p4 = Wrapper(recv_wrapper, settings)

    print('Starting the processes')
    # TODO add code here
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    print('Waiting for processes to finish')
    # TODO add code here
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    display_final_boxes(BOXES_FILENAME)

    # TODO Print the number of gifts created.
    print(f'Number of Gifts: {gifts.value}')


if __name__ == '__main__':
    main()
