# tacBot
A genetic algorithm that plays ultimate tic-tac-toe.

GA started with 10 different strategy encodings that have 500 random board states and strategies

after each generation the encodings are crossbred and each strategy for a particular board encoding has a chance to be mutated

in this case a mutation is the flipping of two bits in the encoding

ie. 123456789 may mutate to be 193456782 where 2 and 9 are switched

to run the code once use the command 
->java -jar match-wrapper-1.3.2.jar "$(cat wrapper-commands.json)"

[Academic Presentation](https://docs.google.com/presentation/d/1smBhLRyMERevP7XOFFJNQzophZwYg6BEwrUq7yebqWw/edit?usp=sharing)
