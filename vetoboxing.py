'''''''''
'' 
'' vetoboxing.py
''
'' This script is designed to run a simulation of veto player voting processes.
''
'' by: Kim de Bie
'' created: 2 February 2016
'' last updated: 19 February 2016
'' 
'''''''''

import numpy as np
import math

def simulation():

	'''
	Function to set inputs and run the simulation.
	TODO: Everything is currently hardcoded, must be made much more flexible.
	Current setup is easier for testing though
	'''

	# ask user for input as points
	voter_A = (1.0,1.0) #input("Please enter the value for voter A: ")
	voter_B = (8.0,4.0) #input("Please enter the value for voter B: ")
	voter_C = (3.0,8.0) #input("Please enter the value for voter C: ")

	voters = [voter_A, voter_B, voter_C]

	# determine the status quo
	status_quo = (5.0,5.0) #input("Please enter the value for the status quo: ")

	#determine who the veto players are
	veto_players = [voter_A]

	#determine the agenda setter
	agenda_setter = voter_B

	#add random points on a grid
	random_points = addRandomPoints(10, 10, 0.1)

	# which points are candidates? 
	# should be in preference circles of both agenda setter and veto players
	points_in_circle = pointsInVetoCircles(random_points, veto_players, agenda_setter, status_quo)

	# select the preferred point
	preferred_point = closestToAgendaSetter(points_in_circle, status_quo, agenda_setter) 

	print 'The outcome of this veto-player game is', preferred_point


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



def pointsInVetoCircles(random_points, veto_players, agenda_setter, status_quo):

	'''
	Function to determine which points fall inside the preference circles of both the agenda 
	setter and all veto players. Thus, a first selection of elegible points is made: the 'winner'
	must be in this set; otherwise it is the status quo.
	TODO: currently, this function only works when there is only one veto player. Must be upgraded
	to work for multiple veto players.
	'''

	# points will be stored in this array
	selected_points = []

	# determining the radius of veto player and agenda setter: how far away can points be?
	veto_radius = determineDistance(veto_players[0], status_quo)
	as_radius = determineDistance(agenda_setter, status_quo)

	# to determine if points are inside a circle:
	# https://stackoverflow.com/questions/481144/equation-for-testing-if-a-point-is-inside-a-circle

	for point in random_points:
		
		# check if point is inside preference circle of agenda setter
		if ((agenda_setter[0] - point[0])**2 + (agenda_setter[1] - point[1])**2) < as_radius**2:

			#if so, check if point is insider preference circle of veto player
			if ((veto_players[0][0] - point[0])**2 + (veto_players[0][1] - point[1])**2) < veto_radius**2:

				#if both are the case, the point is a candidate for the outcome
				selected_points.append(point)		

	return selected_points


def closestToAgendaSetter(points_in_circle, status_quo, agenda_setter):

	'''
	This function determines which point from a given array is closest to the agenda setter. This
	will be the most-preferred point and the outcome of the veto-player game. If there is no point that
	lies in the preference circles of all veto players and the agenda setter, this function returns the 
	status quo. 
	'''

	preferred_point = ''

	# if there are no points inside all preference circles, the outcome will be the status quo
	if len(points_in_circle) == 0:
		print 'The outcome of this game is the status quo: ', status_quo
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


def determineDistance(point1, point2):

	''' This function determines the distance between two points on a two-dimensional space.
	As such, it can also be used to determine the radius of a preference circle (by inputting 
	a point	and the status quo).
	'''

	# 'hypot' uses the pythagorean theorem to determine distance between two points
	distance = math.hypot(point2[0] - point1[0], point2[1] - point1[1])
	return distance


# running the simulation
simulation()