/*
Course: CSE 251
File: team1.cpp

Instructions:

This program will process a list of integers and display which ones are prime.

TODO
- Convert this program to use N pthreads.
- each thread will process 1/N of the array of numbers.
- Create any functions you need
*/

#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <math.h>

#ifdef _WIN32
#include <io.h>
#else
#include <unistd.h>
#endif

#include <time.h>

using namespace std;

#define NUMBERS  100

struct args
{
  int* array;
  int start;
  int end;
};

// ----------------------------------------------------------------------------
int isPrime(int number)
{
  if (number <= 3 && number > 1)
    return 1;            // as 2 and 3 are prime
  else if (number % 2 == 0 || number % 3 == 0)
    return 0;     // check if number is divisible by 2 or 3
  else
  {
    for (unsigned int i = 5; i * i <= number; i += 6) {
      if (number % i == 0 || number % (i + 2) == 0)
        return 0;
    }
    return 1;
  }
}

// ----------------------------------------------------------------------------
void* findPrimes(void* record)
{
  cout << endl << "Starting findPrimes" << endl;

  // Get the structure used to pass arguments
  struct args* arguments = (struct args*)record;

  // Loop through the array looking for prime numbers
  for (int i = arguments->start; i < arguments->end; i++)
  {
    if (isPrime(arguments->array[i]) == 1)
    {
      cout << arguments->array[i] << endl;
    }
  }

  return NULL;
}

// ----------------------------------------------------------------------------
int main()
{
  srand(time(0));

  // Create the array of numbers and assign random values to them
  int arrayValues[NUMBERS];
  for (int i = 0; i < NUMBERS; i++)
  {
    arrayValues[i] = rand() % 1000000000;
    cout << arrayValues[i] << ", ";
  }
  cout << endl;

  //creates threads
  pthread_t thread;
  int threads;

  //asks users for threads desired for experiment
  cout << "input number:";
  cin >> threads;
  cout << endl;

  // intialize numbers needed for calculations
  int start = 0;
  int end = 0;
  int addition = 0;
  int segments = NUMBERS/threads;
  // Create structure that will be used to pass the array and the
  // start of end of the array to another function
  
  
  // Find the primes in the array
  //findPrimes(&rec);

  //create threads
  for(int i = 0; i < threads; i++)
  {  
    end = start + segments;
    cout << "here is start: " << start << endl;
    cout << "here is end: " << end << endl;
    struct args rec = { arrayValues, start, end - 1 };
    start = start + segments;
    pthread_create(&thread, NULL, &findPrimes, &rec);

    //adds last remaining numbers incase threads are odd numbers
    if ( i == 0 )
    {
      if (segments * threads != NUMBERS)
      {
        addition = NUMBERS - (segments*threads);
        start = start + addition;
      }
    }  
  }

  for(int i = 0; i < threads; i++)
  {
    pthread_join(thread, NULL);
  } 
  
  pthread_exit(NULL);
  
  return 0;
}
 