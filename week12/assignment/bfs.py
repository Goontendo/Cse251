import queue
import threading
import time

from virusApi import *

TOP_API_URL = 'http://127.0.0.1:8129'
NUMBER_GENERATIONS = 6  # set this to 2 as you are testing your code
NUMBER_THREADS = 0  # TODO use this to keep track of the number of threads you create
THREAD_COUNT = []

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


def create_family(family_id, q: queue.Queue, pandemic: Pandemic):

    family_thread = Request_thread(
        f'http://{hostName}:{serverPort}/family/{family_id}')

    # threads
    threads = []

    # base case
    if family_id == None:
        return
    else:
        family_thread.start()

    # CREATE FAMILY THREAD
    family_thread.join()

    if ("id" not in family_thread.response):
        return

    # ADD FAMILY
    family = Family.fromResponse(family_thread.response)
    # print(f'###\n{family}\n###')
    pandemic.add_family(family)
    response1 = Request_thread(
        rf'http://{hostName}:{serverPort}/virus/{family.virus1}')
    response2 = Request_thread(
        rf'http://{hostName}:{serverPort}/virus/{family.virus2}')
    response1.start()
    response2.start()
    # Flag to indicate if there are no more parents to check
    any_more_parents = False

    virus1 = None
    virus2 = None

    # Get OFFSPRING
    offspring = []
    for id in family.offspring:
        response3 = Request_thread(
            rf'http://{hostName}:{serverPort}/virus/{id}')
        threads.append(response3)
        response3.start()

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
        v = Virus.createVirus(virus1)
        pandemic.add_virus(v)

        if v.parents != None:
            q.put(v.parents)
            any_more_parents = True

    # ADD VIRUS2 to Pandemic
    if virus2 != None:
        v = Virus.createVirus(virus2)
        pandemic.add_virus(v)

        if v.parents != None:
            q.put(v.parents)
            any_more_parents = True

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
            pandemic.add_virus(v)

    # Exit the WHILE loop
    if not any_more_parents:
        q.put("DONE")


def bfs_recursion(start_id, pandemic):

    # create a queue to store family ids
    q = queue.Queue()

    # put on the first family id and gets family_id
    q.put(start_id)

    while True:
        family_id = q.get()
        p = threading.Thread(target=create_family,
                             args=(family_id, q, pandemic))
        if family_id == "DONE":
            break

        if family_id != None:
            p.start()


def bfs(start_id, generations):
    pandemic = Pandemic(start_id)

    # tell server we are starting a new generation of viruses
    requests.get(f'{TOP_API_URL}/start/{generations}')

    # get all the viruses in the pandemic recursively
    bfs_recursion(start_id, pandemic)

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

    virus_count = bfs(start_id, NUMBER_GENERATIONS)

    for t in THREAD_COUNT:
        t.join()

    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)

    print(f'\nTotal time = {total_time_str} sec')
    print(f'Number of threads: {NUMBER_THREADS}')
    print(f'Performance: {round(virus_count / total_time, 2)} viruses/sec')


if __name__ == '__main__':
    main()
