/*
	---------------------------------------

Course: CSE 251
Lesson Week: 12
File: team.go
Author: Brother Comeau

Purpose: team activity - finding primes

Instructions:

- Process the array of numbers, find the prime numbers using goroutines

worker()

This goroutine will take in a list/array/channel of numbers.  It will place
prime numbers on another channel

readValue()

This goroutine will display the contents of the channel containing
the prime numbers

---------------------------------------
*/
package main

import (
	"fmt"
	"math/rand"
	"time"
)

func isPrime(n int) bool {
	// Primality test using 6k+-1 optimization.
	// From: https://en.wikipedia.org/wiki/Primality_test

	if n <= 3 {
		return n > 1
	}

	if n%2 == 0 || n%3 == 0 {
		return false
	}

	i := 5
	for (i * i) <= n {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
		i += 6
	}
	return true
}

func worker(num int, inc int, numbers []int) {
	// TODO - process numbers on one channel and place prime number on another
	new := num * inc
	for w := new; w <= new + inc; w++{
		if isPrime(w) == true{
			numbers[w] = w
		}	
	}
}

func readValues(numbers []int) {
	// TODO -Display prime numbers from a channel
	for i := 1; i == 100; i++{
		fmt.Printf("%d", numbers[i])
	}

}

func main() {

	workers := 10
	numberValues := 100
	end := 100
	increment := 10

	// Create any channels that you need
	// Create any other "things" that you need to get the workers to finish(join)
	numbers := make([] int, end)

	// create workers
	for w := 1; w <= workers; w++ {
		go worker(w, increment, numbers) // Add any arguments
	}

	rand.Seed(time.Now().UnixNano())
	for i := 0; i < numberValues; i++ {
		//ch <- rand.Int()
	}

	go readValues(numbers) // Add any arguments

	fmt.Println("All Done!")
}
