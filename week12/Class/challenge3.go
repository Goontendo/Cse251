package main

import (
	"fmt"
	"sync"
)

func main() {

	// use 'make' to make a buffered channel that takes integers
	ch := make(chan int, 5)
	fmt.Printf("Capacity: %d\n", cap(ch))

	// create an array of 5 integers using 'make'
	values := make([]int, 5)

	// TODO create a wait group as a barrier to wait until all goroutinues finish
	wg := new(sync.WaitGroup)
	// initialize the 5 indexes with values
	for i := 0; i < 5; i++ {
		values[i] = i
		// TODO increment wait group by one
	}

	// use 'go' to create a goroutine and pass in the channel
	// and the array of ints
	fmt.Println("Sending value to channel")
	go send(ch, values)

	fmt.Println("Receiving from channel")
	// TODO pass in wait group
	go receive(ch, wg)

	// TODO wait until all goroutines finish
	fmt.Println("Done ")
}

func send(ch chan int, values []int) {
	for i := 0; i < len(values); i++ {
		ch <- values[i]
	}
}

func receive(ch chan int, wg *sync.WaitGroup) {
	for val := range ch {
		fmt.Printf("Value Received=%d in receive function\n", val)
		// TODO decrement wait group by one
	}
}
