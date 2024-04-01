'''
Requirements
1. Create a multiprocessing program that reads in files with defined tasks to perform.
2. The program should use a process pool per task type and use apply_async calls with callback functions.
3. The callback functions will store the results in global lists based on the task to perform.
4. Once all 4034 tasks are done, the code should print out each list and a breakdown of 
   the number of each task performed.
   
Questions:
1. How many processes did you specify for each pool:
   >Finding primes:1
   >Finding words in a file:2
   >Changing text to uppercase:1
   >Finding the sum of numbers:1
   >Web request to get names of Star Wars people:10
   
   >How do you determine these numbers:
   
2. Specify whether each of the tasks is IO Bound or CPU Bound?
   >Finding primes:CPU
   >Finding words in a file:IO
   >Changing text to uppercase:CPU
   >Finding the sum of numbers:CPU
   >Web request to get names of Star Wars people:IO
   
3. What was your overall time, with:
   >one process in each of your five pools:  37.89 seconds
   >with the number of processes you show in question one:  6.74 seconds
'''

import glob
import json
import string as sp
import math
import multiprocessing as mp
import os
import time
from datetime import datetime, timedelta

import numpy as np
import requests

TYPE_PRIME = 'prime'
TYPE_WORD = 'word'
TYPE_UPPER = 'upper'
TYPE_SUM = 'sum'
TYPE_NAME = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []


def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def prime_callback(result):
    # Calls Global variable
    global result_primes

    # print(f'prime is reached {result=}')

    # Adds result to global array
    result_primes.append(result)


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    # if else statement to create string for awway
    if is_prime(value) == True:
        string = '{value} is prime'
    else:
        string = '{value} is not prime'

    return string


def word_callback(result):
    # calls Global variable
    global result_words

    # print(f'word is reached {result=}')

    # adds results to words array
    result_words.append(result)


def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found
    """
    # creates file and runs loop to read contents
    filename = 'C:\\Users\\Jared\\Documents\\CSE251w23\\cse251w23\\week09\\assignment\\words.txt'

    with open(filename, 'r') as file:

        # read all content of a file
        content = file.read()

        # check if string present in a file
        if word in content:
            string = '{} Found'.format(word)
        else:
            string = '{} not found'.format(word)

    return string


def upper_callback(result):
    global result_upper
    # print(f'upper is reached {result=}')
    result_upper.append(result)


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    utext = text.upper()
    text.lower()
    string = '{} ==>  uppercase version of {}'.format(text, utext)
    return string


def sum_callback(result):
    global result_sums
    # print(f'sum is reached {result=}')
    result_sums.append(result)


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = start_value + end_value
    string = "sum of {} to {} = {}".format(start_value, end_value, total)
    return string


def name_callback(result):
    global result_names
    # print(f'name is reached {result=}')
    result_names.append(result)


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    # pulls from url
    response = requests.get(url)
    # Check the status code to see if the request succeeded.
    if response.status_code == 200:
        string = '{} has name: {}'.format(url, response.text)
    else:
        string = ' {} had an error receiving the information'.format(url)

    return string


def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data
    else:
        return {}


def main():
    begin_time = time.time()

    # TODO Create process pools

    # The below code is test code to show you the logic of what you are supposed to do.
    # Remove it and replace with using process pools with apply_async calls.
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    count = 0
    # initializes pools
    pool_prime = mp.Pool(1)
    pool_word = mp.Pool(2)
    pool_upper = mp.Pool(1)
    pool_sum = mp.Pool(1)
    pool_name = mp.Pool(10)

    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        # print(task)
        count += 1
        task_type = task['task']
        # print(f'{task_type=}')
        if task_type == TYPE_PRIME:
            pool_prime.apply_async(task_prime, args=(
                task['value'], ), callback=prime_callback)
        elif task_type == TYPE_WORD:
            pool_word.apply_async(task_word, args=(
                task['word'], ), callback=word_callback)
        elif task_type == TYPE_UPPER:
            pool_upper.apply_async(task_upper, args=(
                task['text'], ), callback=upper_callback)
        elif task_type == TYPE_SUM:
            pool_sum.apply_async(task_sum, args=(
                task['start'], task['end']), callback=sum_callback)
        elif task_type == TYPE_NAME:
            pool_name.apply_async(task_name, args=(
                task['url'], ), callback=name_callback)
        else:
            print(f'Error: unknown task type {task_type}')
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # TODO start pools and block until they are done before trying to print
    # close Pools
    pool_prime.close()
    pool_word.close()
    pool_upper.close()
    pool_sum.close()
    pool_name.close()

    # joins Pools
    pool_prime.join()
    pool_word.join()
    pool_upper.join()
    pool_sum.join()
    pool_name.join()

    def print_list(lst):
        for item in lst:
            print(item)
        print(' ')

    print('-' * 80)
    print(f'Primes: {len(result_primes)}')
    print_list(result_primes)

    print('-' * 80)
    print(f'Words: {len(result_words)}')
    print_list(result_words)

    print('-' * 80)
    print(f'Uppercase: {len(result_upper)}')
    print_list(result_upper)

    print('-' * 80)
    print(f'Sums: {len(result_sums)}')
    print_list(result_sums)

    print('-' * 80)
    print(f'Names: {len(result_names)}')
    print_list(result_names)

    print(f'Number of Primes tasks: {len(result_primes)}')
    print(f'Number of Words tasks: {len(result_words)}')
    print(f'Number of Uppercase tasks: {len(result_upper)}')
    print(f'Number of Sums tasks: {len(result_sums)}')
    print(f'Number of Names tasks: {len(result_names)}')
    print(f'Finished processes {count} tasks = {time.time() - begin_time}')


if __name__ == '__main__':
    main()
