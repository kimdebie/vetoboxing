'''''''''
'' 
'' vetoboxing.py
''
'' This script is designed to run a simulation of veto player voting processes.
''
'' by: Kim de Bie
'' created: 2 February 2016
'' last updated: 22 February 2016
'' 
'''''''''

import numpy as np
import math
from scipy.spatial import distance as dist
import csv


#----------------------------------------------------------------------------------------------------#

'''
Setting global variables as input for the simulation.
For each variable, a value should be entered as per the input specifications.
'''

# number of runs of the simulation
# input: any integer >0
runs 				= 2

# the method used to calculate distance between to points
# input: 'pyth' (Pythagorean) or 'city-block' (city-block distance)
distance_type 		= 'city-block'

# the number of dimensions that the game uses
# input: an integer > 1
number_dimensions 	= 2

# the preferences of the voters
# input: two-dimensional point with floats. List may be extended with more voters
voter_A 			= (1.0,1.0)
voter_B				= (8.0,4.0)
voter_C 			= (3.0,8.0)

# vector with the voters
# input: the names of all voters
voters 				= [voter_A, voter_B, voter_C]

# determine the status quo
# input: two-dimensional point with floats
status_quo 			= (5.0,5.0) 

# the agenda setter
# input: one of the voters
agenda_setter 		= voter_B

# determine who the veto players are
# input: any, or none, of the voters
veto_players 		= [voter_A]

# boolean that determines if results are saved in csv
# input: True or False
save_results 		= True

# filename for saving results
# input: 'FILENAME.csv' (only mandatory when save_results is True)
filename 			= 'results.csv'

#----------------------------------------------------------------------------------------------------#

def simulation():

	'''
	Function to run the simulation.
	'''

	# results will be stored in an array
	final_results = []

	for run in range(runs):

		print 'Simulation number', run+1, 'running...'

		# array to store results of current iteration
		current_results = []

		# add random points on a grid
		random_points = addRandomPoints(10, 10, 0.1)

		# which points are candidates? 
		# should be in preference circles of both agenda setter and veto players
		points_in_circle = pointsInWinset(random_points)

		# select the preferred point and append it to results
		outcome = closestToAgendaSetter(points_in_circle)
		current_results.append(outcome)
		
		# determine the euclidian distance that was travelled in this run and append to results
		total_pyth_dist = determineDistance(outcome, status_quo, 'pyth')
		current_results.append(total_pyth_dist)

		# determine the manhattan distance that was travelled in this run and append to results
		total_eucl_dist = determineDistance(outcome, status_quo, 'city-block')
		current_results.append(total_eucl_dist)

		# determine the distance travelled in each dimension
		for i in range(number_dimensions):
			distance = determineDistance(outcome[i], status_quo[i])
			current_results.append(distance)

		# results added to overall results
		final_results.append(current_results)

	if save_results == True:
		with open(filename, 'wb') as output_file:
			saveResults(output_file, final_results)

	return final_results


def addRandomPoints(height, width, breaks):

	'''
	Quick solution to the problem of calculating the position of points on cutoffs of circles. Points
	are systematically added to a grid of a given height and width, at set intervals. 
	'''
	
	points = []

	for i in np.arange(0, height, breaks):

		for j in np.arange(0, width, breaks):

			point = (float(i),float(j))
			points.append(point)

	return points


def pointsInWinset(random_points):

	'''
	Function to determine which points fall inside the preference circles of both the agenda 
	setter and all veto players. Thus, a first selection of elegible points is made: the 'winner'
	must be in this set; otherwise it is the status quo.
	TODO: currently, this function only works when there is only one veto player. Must be upgraded
	to work for multiple (or no) veto players.
	'''

	# points will be stored in this array
	selected_points = []

	# determining the radius of agenda setter: how far away can points be to still be inside circle?
	as_radius = determineDistance(agenda_setter, status_quo)

	# determining the radius for all veto players
	veto_radius = []
	for veto in veto_players:
		radius = determineDistance(veto, status_quo)
		veto_radius.append(radius)

	# to determine if points are inside a circle:
	# https://stackoverflow.com/questions/481144/equation-for-testing-if-a-point-is-inside-a-circle

	for point in random_points:
		
		# check if point is inside preference circle of agenda setter
		if ((agenda_setter[0] - point[0])**2 + (agenda_setter[1] - point[1])**2) < as_radius**2:

			# if so, check if point is insider preference circle of veto player
			# TODO: this should be adapted so that all veto players are checked (currently only fit for 1 VP)
			if ((veto_players[0][0] - point[0])**2 + (veto_players[0][1] - point[1])**2) < veto_radius[0]**2:

				#if both are the case, the point is a candidate for the outcome
				selected_points.append(point)		

	return selected_points


def closestToAgendaSetter(points_in_circle):

	'''
	This function determines which point from a given array is closest to the agenda setter. This
	will be the most-preferred point and the outcome of the veto-player game. If there is no point that
	lies in the preference circles of all veto players and the agenda setter, this function returns the 
	status quo. 
	'''

	preferred_point = ''

	# if there are no points inside all preference circles, the outcome will be the status quo
	if len(points_in_circle) == 0:
		preferred_point = status_quo

	else: 
		lowest_distance_to_as = ''

		for point in points_in_circle:

			# determine the distance of each eligible point to the agenda setter
			distance = determineDistance(point, agenda_setter)

			# if the current point is closest to the agenda setter compared to the points considered
			# so far, that point must be saved
			if lowest_distance_to_as == '' or distance < lowest_distance_to_as:
				preferred_point = point

				# distance is also saved, to compare to distances of other points
				lowest_distance_to_as = distance

	return preferred_point


def determineDistance(point1, point2, set_type=distance_type):

	''' 
	This function determines the distance between two points in any number of dimensions.
	As such, it can also be used to determine the radius of a preference circle (by inputting 
	a point	and the status quo).
	'''

	if set_type == 'pyth':
		# determines distance between two points using Pythagorean theorem
		distance = dist.euclidean(point1, point2)

	elif set_type == 'city-block':
		# determines the city-block or Manhattan distance between two points
		distance = dist.cityblock(point1, point2)

	return distance


def saveResults(file, results):

	'''
	Function to save results to a csv file. 
	'''

	writer = csv.writer(file)

	print 'Saving results to csv...'

	# first row contains variable names
	writer.writerow(['Outcome', 'Euclidean distance', 'Manhattan Distance', 'First dimension', 'Second dimension', 'Third dimension'])

	# write all result-rows to csv
	for result in results:
		writer.writerow(result)

	print 'Done! Find your results in', filename



#----------------------------------------------------------------------------------------------------#

# running the simulation
results = simulation()