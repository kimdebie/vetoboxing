# TO DO LIST
* make players' preferences flexible
* calculate the outcome properly: 'constrained optimization problem'
* allow for more than 3 dimensions
	* fix CSV output for more than 3
	* adapt addRandomPoints()
* better error catching - error checking module
* profiling - determineDistance() is slow!
* better CSV outputs. store constants separately or at top of file
* write handbook for user
-------------------------------------

##### Generate vectors of policy changes as output (write to csv?)
1000 trials:
1. Baseline VP model (random draw SQ - no history)
2. DVP model (random walk SQ - with history)
3. DVP model (random walk SQ - with history and biased drift)
4. DVP model (random walk SQ - with history and biased drift, and preferences with drift)

Run 1-4 for 1, 2, and 3 dimensions
Run all under majority rule with 1, 2, and 3 veto players with 5 players total.


-------------------------------------

Questions:
* should the cityblock distance also be used to determine the radius of circles? or should that always be done using pythagorean
