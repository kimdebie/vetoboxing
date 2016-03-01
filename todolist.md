# TO DO LIST
#### As discussed on 22/02
* DONE add more veto players, and allow for game with 0 veto players
* DONE add iterations
* let the status quo change for each iteration:
	* DONE with history: the new status quo is the outcome
	* DONE with random draws from various distributions: normal, uniform, exponential, paretian (mean of 0)
	* with a combination of history and randomness
* allow random draws from distributions for the players (variation in player preferences)
* DONE calculate preference changes with city-block distance
* calculate the outcome properly: 'constrained optimization problem'
* adding and removing dimensions

####To keep in mind for later:
* visualization

--------------------------------------

##### Generate vectors of policy changes as output (write to csv?)
Output per treatment (1000 iterations):
* Pythagorean distance
* City-block distance
* Distance moved in the first dimension
* Distance moved in the second dimension
* Distance moved in the third dimension

#####Play 27 games in total:

Variation in status quo:
* mobile status quo: random draws
* mobile status quo: with history
* mobile status quo: with history plus random draws

Variation in the number of veto players:
* 0 veto players
* 1 veto players
* 2 veto players

Variation in the input distributions:
* Normal distribution
* Uniform distribution
* Exponential distribution

For each of the 27 games (3x3x3), save the 5 variables above.

-------------------------------------

Questions:
* should the cityblock distance also be used to determine the radius of circles? or should that always be done using pythagorean
