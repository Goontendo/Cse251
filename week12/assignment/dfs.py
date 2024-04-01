"""
Course: CSE 251
Lesson Week: 12
File: assignment.py
Author: <your name>
Purpose: Assignment 12 - Family Search
"""
import json
import threading
import time

import requests
from virusApi import *

TOP_API_URL = 'http://127.0.0.1:8129'
NUMBER_GENERATIONS = 6  # set this to 2 as you are testing your code
NUMBER_THREADS = 0  # TODO use this to keep track of the number of threads you create
THREADS = []

# -----------------------------------------------------------------------------


class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        global NUMBER_THREADS
        response = requests.get(self.url)
        NUMBER_THREADS += 1
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


def dfs_recursion(family_id, pandemic: Pandemic):

    global NUMBER_THREADS
    global THREADS
    threads = []

    # base case
    if family_id == None:
        return

   # print(f'{family_id=} Retrieving Family: {family_id}\n', end="")

    # add family to pandemic
    family_response = Request_thread(rf'{TOP_API_URL}/family/{family_id}')
    family_response.start()
    family_response.join()

    if ("id" not in family_response.response):
        return

    family = Family.fromResponse(family_response.response)
    # print(f'{family_id=} family.response={family_t.response}\n', end="")
    pandemic.add_family(family)

    # creates threads
    response1 = Request_thread(
        rf'http://{hostName}:{serverPort}/virus/{family.virus1}')
    response2 = Request_thread(
        rf'http://{hostName}:{serverPort}/virus/{family.virus2}')
    response1.start()
    response2.start()

    virus1 = None
    virus2 = None

    # Get OFFSPRING
    offspring = []
    for id in family.offspring:
        response = Request_thread(
            rf'http://{hostName}:{serverPort}/virus/{id}')
        threads.append(response)
        response.start()

    # Get VIRUS1
    if family.virus1 != None:
        response1.join()
        virus1 = response1.response

    # Get VIRUS2
    if family.virus2 != None:
        response2.join()
        virus2 = response2.response

    # ADD VIRUS1 to Pandemic
    if virus1 != None:
        # print(virus1)
        v = Virus.createVirus(virus1)
        pandemic.add_virus(v)
        # print(f'virus1 added')
        p = threading.Thread(target=dfs_recursion, args=(v.parents, pandemic))
        if v.parents != None:
            NUMBER_THREADS += 1
            THREADS.append(p)
            p.start()
            # dfs_recursion(v.parents, pandemic)

    # ADD VIRUS2 to Pandemic
    if virus2 != None:
        # print(virus2)
        v = Virus.createVirus(virus2)
        # print(f'virus2 added')
        pandemic.add_virus(v)
        p = threading.Thread(target=dfs_recursion, args=(v.parents, pandemic))
        if v.parents != None:
            NUMBER_THREADS += 1
            THREADS.append(p)
            p.start()
            # dfs_recursion(v.parents, pandemic)

    for thread in threads:
        thread.join()
        offspring.append(thread.response)

    # ADD offspring to Pandemic
    for o in offspring:
        v = Virus.createVirus(o)
        # don't try and add virus that we have already added
        # (happens when we add a virus and then loop over the
        # virus parent's offspring)
        if not pandemic.does_virus_exist(v.id):
            # print(f'offspring virus added')
            pandemic.add_virus(v)
            # print(v)


def dfs(start_id, generations):
    pandemic = Pandemic(start_id)

    global THREADS

    # tell server we are starting a new generation of viruses
    requests.get(f'{TOP_API_URL}/start/{generations}')

    # get all the viruses in the pandemic recursively
    p = threading.Thread(target=dfs_recursion, args=(start_id, pandemic))
    p.start()
    p.join()

    requests.get(f'{TOP_API_URL}/end')

    print('')
    print(f'Total Viruses  : {pandemic.get_virus_count()}')
    print(f'Total Families : {pandemic.get_family_count()}')
    print(f'Generations    : {generations}')

    return pandemic.get_virus_count()


def main():
    # Start a timer
    begin_time = time.perf_counter()

    print(f'Pandemic starting...')
    print('#' * 60)

    response = requests.get(f'{TOP_API_URL}')
    jsonResponse = response.json()

    print(f'First Virus Family id: {jsonResponse["start_family_id"]}')
    start_id = jsonResponse['start_family_id']

    virus_count = dfs(start_id, NUMBER_GENERATIONS)

    # THREADS.reverse()

    for t in THREADS:
        print(t)
        t.join()

    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)

    print(f'\nTotal time = {total_time_str} sec')
    print(f'Number of threads: {NUMBER_THREADS}')
    print(f'Performance: {round(virus_count / total_time, 2)} viruses/sec')


if __name__ == '__main__':
    main()
