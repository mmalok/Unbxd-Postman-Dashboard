package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("started at : ", time.Now())
	time.Sleep(time.Second * 8)
	fmt.Println("Ended at : ", time.Now())
}
