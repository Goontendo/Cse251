package main

import (
	"fmt"
	"time"
)

func main() {

	// TODO use 'make' to make a buffered channel, of size 5, that takes integers
	ch := make(chan int, 5)
	fmt.Printf("Capacity: %d\n", cap(ch))

	//TODO create an array of 5 integers using 'make'
	numbers := make([] int, 5)

	//TODO initialize the 5 indexes with values
	for i := 0; i < 5; i++{
		numbers[i] = i
	}

	// TODO use 'go' to create a goroutine and pass in the channel and values
	fmt.Println("Sending value to channel")
	go send(ch, numbers)

	fmt.Println("Receiving from channel")
	go receive(ch)

	// leave this
	time.Sleep(time.Second * 5)
	fmt.Println("DONE")
}

func send(ch chan int, values []int) {
	for i := 0; i < 5; i++{
		values[i] = i
	}
}

func receive(ch chan int) {
	// TODO keep looping to receive all the values in the channel
	for val := range ch {
		fmt.Printf("recieved %d", val)
	}
}
