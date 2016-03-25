'''''''''
''
'' vetoboxing.py
''
'' This script is designed to run a simulation of veto player voting processes.
''
'' by: Kim de Bie
'' created: 2 February 2016
'' last updated: 24 March 2016
''
'''''''''

#----------------------------------------------------------------------------------------------------#

# IMPORTING PACKAGES

import numpy as np
import math
from scipy.spatial import distance as dist
import csv
import os
import operator
import itertools
import errno
import time


#----------------------------------------------------------------------------------------------------#

# CLASSES AND GLOBAL VARIABLES
# no need to touch this part
'''
Class that stores position of a voter, whether they are an agenda setter or
veto player or not.
'''


class Voter(object):
	def __init__(self, position, agenda_setter, veto_player):
		self.position = position
		self.agenda_setter = agenda_setter
		self.veto_player = veto_player
		self.original_position = position

# set up additional global variables - no need to touch!
model_number = None
agenda_setter = ''
veto_players = []

#----------------------------------------------------------------------------------------------------#

# GLOBAL VARIABLES

'''
Setting global variables as input for the simulation.
For each variable, a value should be entered as per the input specifications.
'''

# number of runs of the simulation
# input: any integer > 0
runs 				= 1000

# the method used to calculate distance between to points
# input: 'pyth' (Pythagorean) or 'city-block' (city-block distance)
distance_type 		= 'pyth'

# the number of dimensions that the game uses
# input: 1, 2, 3 TODO: extend to more dimensions
number_dimensions 	= 1

# setting up the voters
# input layout: Voter ( (POSITION), AS, VP )
# NOTE: in 1 dimension, input voter values like so: (1,0,)
voter_A 			= Voter((1.0,), False, True)
voter_B				= Voter((4.0,), True, False)
voter_C 			= Voter((3.0,), False, False)
voter_D 			= Voter((2.0,), False, False)
voter_E 			= Voter((2.5,), False, False)

# vector with the voters
# input: the names of all voters
voters 				= [voter_A, voter_B, voter_C, voter_D, voter_E]

# determine the initial status quo
# input: point with floats
# NOTE: in 1 dimension, input status quo like so: (1,0,)
status_quo 			= (5.0,4.5)

# determine whether status quo changes for each iteration
# input: 'no', 'random', 'history', 'history and drift'
alter_status_quo	= 'history and drift'

# set the drift in each dimension for the status quo
# input: a list with the drift in each(!) dimension (can be zero)
# only required when alter_status_quo = 'history and drift'
drift_status_quo	= [0.2,0.5,0.2]

# determine whether preferences for voters change for each iteration
# input: 'no', 'drift'
alter_preferences	= 'drift'

# set the drift in each dimension for the voter
# input: a list with the drift in each(!) dimension (can be zero), applied to every voter
drift_players		= [0.2,0.5,0.1]

# determine what type of distribution is used for random draws
# input: 'normal', 'uniform', 'exponential', 'paretian'
distribution_type	= 'normal'

# determine what method is used for picking optimal point
# input: 0, 1		where 0 = point-grid, 1 = constrained optimization
dummy_type			= 0

# determine how large the grid should be
# input: positive integer
grid_size 			= 300

# determine the interval at which points should be placed in grid
# input: positive float
breaks 				= 0.1

# boolean that determines if results are saved in csv
# input: True, False
save_results 		= True

# folder for saving results
# input: 'FOLDERNAME' (only mandatory when save_results is True)
folder				= 'RESULTS'


#----------------------------------------------------------------------------------------------------#

def simulation():

	'''
	Function to run the simulation. Here, all different parts of the simulation come together. Reading it
	will give you a general understanding of the logic of this script. In adddition, all variables that
	are ultimately saved to csv are stored in this function.
	'''
	# set up agenda setter
	global agenda_setter
	for voter in voters:
		if voter.agenda_setter == True:
			agenda_setter = voter

	# set up array for veto players
	for voter in voters:
		if voter.veto_player == True:
			veto_players.append(voter)

	# results will be stored in an array
	final_results = []

	# add random points on a grid
	# grid stays constant for every run
	random_points = addRandomPoints(grid_size, breaks)

	# set model number for csv
	global model_number
	model_number = setModelNumber()

	for run in range(runs):

		print 'Simulation number', run+1, 'running...'

		# array to store results of current iteration
		current_results = []

		# append the preferences of the players (for the existing players) to results
		for i in range(0,5):
			try:
				current_results.append(voters[i].position)
			except:
				current_results.append('NA')

		# append the preferences of the veto players (for those present) to results
		for i in range(0,3):
			try:
				current_results.append(veto_players[i].position)
			except:
				current_results.append('NA')

		# append the status quo to results
		current_results.append(status_quo)

		# determine the coalitions that can be formed to get to a majority
		possible_coalitions = determineCoalitions()

		# this will store the outcome selected by each coalition
		possible_outcomes = []

		# determine the possible outcomes based on different coalitions
		for coalition in possible_coalitions:
			# select the points that are in the winset for the current coalition
			points_in_circle = pointsInWinset(random_points, coalition)

			# determine coalition's preference and append to all outcomes
			possible_outcome = closestToAgendaSetter(points_in_circle)
			possible_outcomes.append(possible_outcome)

		# select the point preferred by the agenda setter out of all
		# possible coalitions, and append to results
		outcome = closestToAgendaSetter(possible_outcomes)
		current_results.append(outcome)

		# determine the euclidian distance that was travelled in this run and append to results
		total_pyth_dist = determineDistance(outcome, status_quo, 'pyth')
		current_results.append(total_pyth_dist)

		# determine the manhattan distance that was travelled in this run and append to results
		total_manh_dist = determineDistance(outcome, status_quo, 'city-block')
		current_results.append(total_manh_dist)

		# determine the distance travelled in each dimension and append to results
		for i in range(0,3):
			try:
				if number_dimensions == 1:
					distance = determineDistance(outcome, status_quo)
				else:
					distance = determineDistance(outcome[i], status_quo[i])
				current_results.append(distance)
			except:
				current_results.append('NA')

		# append number of dimensions to results
		current_results.append(number_dimensions)

		# append number of veto players to results
		current_results.append(len(veto_players))

		# append model type to results
		current_results.append(model_number)

		# append dummy for optimization type to results
		current_results.append(dummy_type)

		# results added to overall results
		final_results.append(current_results)

		# set the new status quo
		alterStatusQuo(outcome)

		# set the new players' preferences
		alterPlayerPreferences()

	# save results to a csv file
	if save_results == True:
		saveResults(final_results)

	return final_results


def addRandomPoints(size, breaks):

	'''
	Quick solution to the problem of calculating the position of points on cutoffs of circles. Points
	are systematically added to a grid of a given height and width, at set intervals.
	TODO: make this a LOT prettier :-) (recursion?)
	'''

	points = []

	if number_dimensions == 1:
		for i in np.arange(0, size, breaks):
			point = (float(i))
			points.append(point)

	elif number_dimensions == 2:
		for i in np.arange(0, size, breaks):
			for j in np.arange(0, size, breaks):
				point = (float(i),float(j))
				points.append(point)

	elif number_dimensions == 3:
		for i in np.arange(0, size, breaks):
			for j in np.arange(0, size, breaks):
				for k in np.arange(0, size, breaks):
					point = (float(i), float(j), float(k))
					points.append(point)

	return points


def pointsInWinset(random_points, voter_selection):

	'''
	Function to determine which points fall inside the preference circles of both the agenda
	setter and all veto players, as well as possible additional players required to get to
	a majority. Thus, a first selection of elegible points is made: the 'winner'
	must be in this set; otherwise it is the status quo.
	This function is first used to determine the optimum within each coalition, and then
	to determine the final outcome: the optimal point across all coalitions.
	'''

	# points will be stored in this array
	selected_points = []

	# determining the radius of agenda setter: how far away can points be to still be inside circle?
	as_radius = determineDistance(agenda_setter.position, status_quo)

	# determining the radius for all relevant players
	voter_radius = []
	for voter in voter_selection:
		radius = determineDistance(voter.position, status_quo)
		voter_radius.append(radius)

	# to determine if points are inside a circle:
	# https://stackoverflow.com/questions/481144/equation-for-testing-if-a-point-is-inside-a-circle

	for point in random_points:

		# determine the distance of point to agenda setter
		distance_point_as = determineDistance(agenda_setter.position, point)

		# check if point is inside preference circle of agenda setter
		if distance_point_as < as_radius:

			# so far, the point has not been vetoed: the AS may propose it
			point_vetoed = False

			# check with each voter if point is OK
			for i, player in enumerate(voter_selection):

				# determine the distance of point to every voter
				distance_point_voter = determineDistance(voter_selection[i].position, point)

				# check if point is outside preference circle: it will be vetoed
				if distance_point_voter > voter_radius[i]:
					point_vetoed = True

			# if a point was not vetoed by anyone, it can be appended
			if point_vetoed == False:
				selected_points.append(point)

	return selected_points

def determineCoalitions():

	'''
	This function will be used to determine which possible coalitions can form a majority. It checks
	how many more (if any) voters are needed besides the veto players and the agenda setter (which
	are always required to vote for a proposal), and creates all possible combinations of voters.
	'''

	# variable to store all possible coalitions
	possible_coalitions = []

	# variable to store the required voters: the agenda setter...
	required_voters = [agenda_setter]

	# ... and all veto players
	for player in veto_players:
		required_voters.append(player)

	# check if veto players and the agenda setter are a majority by themselves
	if len(required_voters) < 0.5 * len(voters):

		# if they are not: determine how many more voters are needed
		more_voters = int(math.ceil(0.5 * len(voters) - len(veto_players) - 1))

		# the voters that are not yet in the required_voters (the not-AS & VPs)
		normal_voters = []
		for voter in voters:
			if voter not in required_voters:
				normal_voters.append(voter)

		# the combinations of voters that can be added to the required voters to get a coalition
		coalition_extensions = itertools.combinations(normal_voters, more_voters)

		# add every coalition (required + extension) to list of possible coalitions
		for extension in coalition_extensions:
			possible_coalition = required_voters + list(extension)
			possible_coalitions.append(possible_coalition)


	# if VPs and agenda setter are already a majority, they are the only coalition
	else:
		possible_coalitions.append(required_voters)

	return possible_coalitions


def closestToAgendaSetter(points_in_selection):

	'''
	This function determines which point from a given array is closest to the agenda setter. It takes all
	points that a have a theoretical majority; now the point is to determine which the AS likes most. This
	will be the most-preferred point and the outcome of the veto-player game. If there is no point that
	lies in the preference circles of all veto players and the agenda setter, this function returns the
	status quo.
	'''

	preferred_point = ''

	# if there are no points inside all preference circles, the outcome will be the status quo
	if len(points_in_selection) == 0:
		preferred_point = status_quo

	else:
		lowest_distance_to_as = ''

		for point in points_in_selection:

			# determine the distance of each eligible point to the agenda setter
			distance = determineDistance(point, agenda_setter.position)

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



def alterStatusQuo(outcome):

	'''
	This function sets the status quo for the new simulation. Based on the parameters
	defined at the top of the document, a new value for the status quo is picked.
	'''
	# first, check if the status quo should be altered
	global status_quo
	#history _ random error + biased drift

	# because of the flexible number of dimensions (and because it is not possible
	# to append to a tuple), the points are first stored in a list and the status
	# quo is also stored as a list
	status_quo = list(status_quo)
	new_status_quo = []

	# setting the appropriate vibration type
	vibration = setVibration()

	# if the status quo is not altered, it vibrates nonetheless
	if alter_status_quo == 'no':
		for i in range(number_dimensions):
			dim = status_quo[i] - vibration
			new_status_quo.append(dim)

	# pick a new, completely random status quo - and vibrate it
	if alter_status_quo == 'random':
		for i in range(number_dimensions):
			dim = np.random.uniform(0.0, 10.0) - vibration
			new_status_quo.append(dim)

	# alter status quo based on outcome of previous run, and vibration
	elif alter_status_quo == 'history':
		#outcome temporarily stored as list
		if not isinstance(outcome, tuple):
			dim = outcome - vibration
			new_status_quo.append(dim)
		else:
			outcome = list(outcome)
			for i in range(number_dimensions):
				dim = outcome[i] - vibration
				new_status_quo.append(dim)

	# alter status quo based on outcome of previous run, drift, and vibration
	elif alter_status_quo == 'history and drift':
		#outcome temporarily stored as list
		if not isinstance(outcome, tuple):
			dim = outcome - vibration + drift_status_quo[0]
			new_status_quo.append(dim)
		else:
			outcome = list(outcome)
			for i in range(number_dimensions):
				dim = outcome[i] - vibration + drift_status_quo[i]
				new_status_quo.append(dim)

	# status quo is stored as a tuple again, as it was before
	status_quo = tuple(new_status_quo)


def alterPlayerPreferences():

	'''
	Function to alter the preferences of the players for every run. Two options: preferences
	do not change (yet there is some vibration), or preferences have a drift in a certain
	direction.
	'''

	global voters

	# setting the appropriate vibration type
	vibration = setVibration()

	# if the preferences are not altered, there is still vibration
	# movement from the initial position of the voter - at the start of the simulation
	if alter_preferences == 'no':

		# apply changes to every voter
		for i, voter in enumerate(voters):
			# set up list for new voter
			new_voter = []
			voter = list(voters[i].original_position)
			for j in range(number_dimensions):
				dim = voter[j] + vibration
				new_voter.append(dim)
			voters[i].position = tuple(new_voter)

	elif alter_preferences == 'drift':

		# apply changes to every voter
		for i, voter in enumerate(voters):
			# set up list for new voter
			new_voter = []
			voter = list(voters[i].position)
			for j in range(number_dimensions):
				dim = voter[j] + vibration + drift_players[j]
				new_voter.append(dim)
			voters[i].position = tuple(new_voter)

	else:
		print 'alter_preferences was not defined correctly.'


def saveResults(results):

	'''
	Function to save results to a csv file in a folder called RESULTS.
	'''

	# setting up a directory to store files called RESULTS
	results_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], folder)
	create_dir(results_dir)

	# creating datestamp for file
	timestr = time.strftime("%Y-%m-%d_%H%M")

	# setting up the name of the file
	filename = ''.join(('results', '-', str(model_number), '-', str(number_dimensions),
	 	'-', str(len(veto_players)), '__', timestr, '.csv'))


	print 'Saving results to csv...'

	csv_file = os.path.join(results_dir, filename)
	writer = csv.writer(open(csv_file, 'wb'))

	# first row contains variable names
	writer.writerow(['Voter_A', 'Voter_B', 'Voter_C', 'Voter_D', 'Voter_E',
		'VP_1', 'VP_2', 'VP_3', 'Status Quo', 'Policy Decision', 'Total Euclidean Distance',
		'Total Manhattan Distance', 'Distance first dimension', 'Distance second dimension',
		'Distance third dimension', 'Number of dimensions', 'Number of VPs', 'Model', 'Optimization?'])

	# write all result-rows to csv
	for result in results:
		writer.writerow(result)

	print 'Done! Find your results in', filename



#----------------------------------------------------------------------------------------------------#

# SETTING UP ADDITIONAL VARIABLES - NO NEED TO EDIT

# setting model number (for diagnostics in csv)

def setModelNumber():

	'''
	This function sets the model number of the simulation. It is only used for classifying the model
	in the csv.
	'''

	if alter_status_quo == 'no':
		return 0
	elif alter_status_quo == 'random':
		return 1
	elif alter_status_quo == 'history':
		return 2
	elif alter_status_quo == 'history and drift' and alter_preferences == 'no':
		return 3
	elif alter_status_quo == 'history and drift' and alter_preferences == 'drift':
		return 4
	else:
		return 'NA'


def setVibration():
	'''
	This function picks the appropriate distribution to draw from
	for the vibration of players and status quo.
	'''
	if distribution_type == 'normal':
		return randomNormal()
	elif distribution_type == 'uniform':
		return randomUniform()
	elif distribution_type == 'exponential':
		return randomExponential()
	elif distribution_type == 'paretian':
		return randomPareto()
	else:
		print 'Distribution type undefined. Cannot set up new simulation'

#----------------------------------------------------------------------------------------------------#


# Minor functions that aid the functions above

# random draws from a normal distribution
# currently mean is set at 1, standard deviation at 0.25
def randomNormal():
	return np.random.normal(0, 0.2)

# TODO currently only randomNormal is used, check how appropriate
# the values for the other distributions are
def randomUniform():
	return np.random.uniform(low=0.0, high=10.0)

def randomExponential():
	return np.random.exponential(scale=1.0)

def randomPareto():
	return np.random.pareto(5)

def create_dir(directory):
    '''
    Create directory if needed.
    '''

    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise


#----------------------------------------------------------------------------------------------------#
# Currently unused function
def oldDetermineMajority():

	'''
	Function to determine which voters are needed. The function determines who, in addition to
	the veto players and the agenda setter, are needed to get a majority. For this, the players
	closest to the agenda setter (in addition to the veto players) are selected.
	This method proved incorrect (leaving it here for potential later use - just in case).
	'''

	# variable to store the required voters: the agenda setter...
	required_voters = [agenda_setter]

	# ... and all veto players
	for player in veto_players:
		required_voters.append(player)

	# check if veto players and the agenda setter are a majority by themselves
	if len(required_voters) < 0.5 * len(voters):

		# if they are not: determine how many more voters are needed
		more_voters = int(math.ceil(0.5 * len(voters) - len(veto_players) - 1))

		# this array will contain potential voters and their distances to the agenda setter
		possible_voters = []

		# determine the distance of each voter to the agenda setter
		for voter in voters:
			# exclude voters that are already in the list of required voters
			if voter not in required_voters:

				distance = determineDistance(voter, agenda_setter)
				voter_distance = (voter, distance)
				possible_voters.append(voter_distance)

		# sort the voters by their distance to the agenda setter
		# from https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples
		sorted_voters = sorted(possible_voters, key=lambda tup: tup[1])

		# add the number of voters required to make a majority
		for i in range(more_voters):
			required_voters.append(sorted_voters[i][0])

	return required_voters

#----------------------------------------------------------------------------------------------------#

# running the simulation
results = simulation()
