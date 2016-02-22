# TO DO LIST
#### As discussed on 22/02
* add more veto players, and allow for game with 0 veto players
* add iterations
* let the status quo change for each iteration:
	* with history: the new status quo is the outcome
	* with random draws from various distributions: normal, uniform, exponential, paretian (mean of 0)
* allow random draws from distributions for the players (variation in player preferences)
* calculate preference changes with city-block distance
* calculate the outcome properly: 'constrained optimization problem'
* adding and removing dimensions
* visualization

##### Generate vectors of policy changes as output (write to csv?)
Output per treatment (1000 iterations):
* Pythagorean distance
* City-block distance
* Distance moved in the first dimension
* Distance moved in the second dimension
* Distance moved in the third dimension

Play 27 games in total: 

Variation in status quo: 
1. mobile status quo: random draws
2. mobile status quo: with history
3. mobile status quo: with history plus random draws

Variation in the number of veto players:
1. 0 veto players
2. 1 veto players
3. 2 veto players

Variation in the input distributions:
1. Normal distribution
2. Uniform distribution
3. Exponential distribution

For each of the 27 games (3x3x3), save the 5 variables above.