#main generator

all: main

main.o: main.cpp
	g++ -c main.cpp -std=c++14

polygon.o: polygon.cpp polygon.h
	g++ -c polygon.cpp -std=c++14

main: main.o polygon.o
	g++ main.o polygon.o -o main -std=c++14

clean:
	rm *.o main
