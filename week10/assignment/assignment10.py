'''
Purpose: Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        ***************************************************
        ** DO NOT search for a solution on the Internet, **
        ** your goal is not to copy a solution, but to   **
        ** work out this problem.                        **
        ***************************************************

- When a philosopher wants to eat, it will ask the waiter if it can.  If the waiter 
  indicates that a philosopher can eat, the philosopher will pick up each fork and eat.  
  There must not be an issue picking up the two forks since the waiter is in control of 
  the forks. When a philosopher is finished eating, it will inform the waiter that they
  are finished.  If the waiter indicates to a philosopher that they can not eat, the 
  philosopher will wait between 1 to 3 seconds and try again.

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout. This can be useful to not
  block when trying to acquire a lock.
- Philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- Philosophers need to think (digest?) for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks (minimum of 5 philosophers).
- Use threads for this problem.
- Provide a way to "prove" that each philosophers will not starve. This can be counting
  how many times each philosophers eat and display a summary at the end. Or, keeping track
  how long each philosopher is eating and thinking.
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat. Hint, they are
  sitting in a circle.
'''

import time
import threading
import logging
import random

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5
MEAL_COUNT = [0, 0, 0, 0, 0]
THINK_COUNT = [0, 0, 0, 0, 0]
EATING_COUNT = [0, 0, 0, 0, 0]


class Waiter(object):
    def __init__(self,
                 number):
        self.cv = threading.Condition(threading.Lock())
        self.p = number

    def up(self):
        # waiters tells philospher to eat
        print('waiters is telling philosopher to eat\n')
        with self.cv:
            while self.p == 0:
                self.cv.wait()
            self.p -= 1

    def down(self):
        # waiters tell philosopher to stop
        with self.cv:
            self.p += 1
            self.cv.notify_all()
            print('waiter is telling philosopher he is done eating\n')


class Philosopher (threading.Thread):

    def __init__(self, number, left, right, Waiter):
        threading.Thread.__init__(self)
        self.number = number            # philosopher number
        self.left = left
        self.right = right
        self.waiter = Waiter

    def run(self):
        global MAX_MEALS
        global MEAL_COUNT
        global THINK_COUNT
        global EATING_COUNT
        # for loop to rotate forks between philosophers
        for i in range(MAX_MEALS - 5):
            self.waiter.up()
            print('made it pass waiter\n')
            self.left.acquire()
            print('left forked is picked up\n')
            self.right.acquire()
            print('right forked is picked up\n')
            print(f'eating has started')
            eating = random.randrange(1, 3)
            time.sleep(eating)
            EATING_COUNT[self.number] += eating
            self.right.release()
            self.left.release()
            print('forks are set down\n')
            thinking = random.randrange(1, 3)
            time.sleep(thinking)
            THINK_COUNT[self.number] += thinking
            MEAL_COUNT[self.number] += 1
            self.waiter.down()


def main():
    # TODO - create the waiter (A class would be best here).
    global PHILOSOPHERS
    global MEAL_COUNT
    global EATING_COUNT
    waiter = Waiter(PHILOSOPHERS - 1)

    # TODO - create the forks (What kind of object should a fork be?).
    forks = [threading.Lock() for i in range(PHILOSOPHERS)]

    # TODO - create PHILOSOPHERS philosophers.
    phil = [Philosopher(i, forks[i], forks[(i+1) % PHILOSOPHERS], waiter)
            for i in range(PHILOSOPHERS)]

    # TODO - Start them eating and thinking.
    for p in range(PHILOSOPHERS):
        phil[p].start()
    for p in range(PHILOSOPHERS):
        phil[p].join()

    # TODO - Display how many times each philosopher ate,
    #        how long they spent eating, and how long they spent thinking.
    for i in range(PHILOSOPHERS):
        print(f'Philosopher {i + 1} ate {MEAL_COUNT[i]} meals')
        print(f'Philosopher {i + 1} thought for {THINK_COUNT[i]} seconds')
        print(f'Philosopher {i + 1} ate for {EATING_COUNT[i]} seconds')


if __name__ == '__main__':
    main()
