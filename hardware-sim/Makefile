.PHONY = all clean 

all:
	gcc main.c private/reader.c private/receiver.c private/sender.c private/sensors.c -o main -Wall

#for debugging
msender:
	gcc private/sender.c -fsyntax-only -Wall

clean: 
	rm -rf main


