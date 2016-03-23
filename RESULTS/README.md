#Filenames should be read as follows:

###results_modelnumber_dimensions_vetoplayers.csv

where:
####modelnumber:
1.) Baseline VP model (random draw SQ - no history)
2.) DVP model (random walk SQ - with history)
3.) DVP model (random walk SQ - with history and biased drift)
4.) DVP model (random walk SQ - with history and biased drift, and preferences with drift)

####dimensions:
1, 2 or 3 dimensions

####vetoplayers:
1, 2 or 3 vetoplayers


NOTE: The distances for all dimensions are entered, even when they are not actually present. This can be ignored for now (it calculates the total distance travelled for the non-existing dimensions).

NOTES ON SPEED:
* adding dimensions slows down the simulation. I added only 500 runs for the two- and three-dimensional simulations. Also, for the 3-dimensional I set 'breaks' (determines the distance between points on the grid) at 0.5 instead of 0.1 (as I did for 1 and 2-dimensional)
* adding veto players speeds up the simulation. This makes sense, as only points within their pref circles are considered - garbage thrown out quicker. The difference between 1 and 2 veto players is much larger than the difference between 2 and 3 VPs.
* modelnumber doesn't seem to matter much.
