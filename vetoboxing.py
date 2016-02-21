'''''''''
'' 
'' vetoboxing.py
''
'' This script is designed to run a simulation of veto player voting processes.
''
'''''''''

import numpy
import math
from math import hypot



def simulation():
	#ask user for input as points
	voter_A = (1.0,1.0)#input("Please enter the value for voter A: ")
	voter_B = (8.0,4.0)#input("Please enter the value for voter B: ")
	voter_C = (3.0,8.0)#input("Please enter the value for voter C: ")

	voters = [voter_A, voter_B, voter_C]

	#determine the status quo
	status_quo = (7.0,4.0)#input("Please enter the value for the status quo: ")

	#determine who the veto players are
	veto_players = [voter_A]

	#determine the agenda setter
	agenda_setter = voter_B

	#add random points on a grid
	random_points = addRandomPoints(10, 10)

	# which points are candidates? 
	# should be in pref circle of agenda setter and veto players
	points_in_circle = pointsInVetoCircles(random_points, veto_players, agenda_setter, status_quo)

	preferred_point = closestToAgendaSetter(points_in_circle, status_quo, agenda_setter) 

	print 'outcome', preferred_point


def addRandomPoints(height, width):
	points = []

	for i in range(height):
		for j in range(width):
			point = (float(i),float(j))
			points.append(point)

	return points

# determine which points fall inside the preference circle of all veto players
# TODO: currently only works when there is 1 veto player
def pointsInVetoCircles(random_points, veto_players, agenda_setter, status_quo):
	selected_points = []

	veto_radius = determineDistance(veto_players[0], status_quo)
	as_radius = determineDistance(agenda_setter, status_quo)

	for point in random_points:
		# https://stackoverflow.com/questions/481144/equation-for-testing-if-a-point-is-inside-a-circle
		# first, check if point is inside preference circle of agenda setter
		if (2**(agenda_setter[0] - point[0]) + 2**(agenda_setter[1] - point[1])) < 2**as_radius:
			print 'first', point
			#then, check if point is insider preference circle of veto player
			if (2**(veto_players[0][0] - point[0]) + 2**(veto_players[0][1] - point[1])) < 2**veto_radius:
				#if both tests are passed, the point is a candidate for the outcome
				print 'second', point
				selected_points.append(point)		

	return selected_points

# determine point closest to agenda setter
def closestToAgendaSetter(points_in_circle, status_quo, agenda_setter):
	preferred_point = ''
	if len(points_in_circle) == 0:
		print 'the preferred point is the status quo: ' + status_quo
		preferred_point = status_quo

	else: 
		lowest_distance_to_as = ''
		for point in points_in_circle:
			distance = determineDistance(point, agenda_setter) #determine the distance to the AS
			# if the closest point hasn't been determined OR current point is closer, save that point
			if lowest_distance_to_as == '' or distance < lowest_distance_to_as:
				lowest_distance_to_as = distance
				print 'thistance', distance
				preferred_point = point

	return preferred_point


# determining the distance between two points
# can also be used to determine the radius (by inputting a point and the status quo)
def determineDistance(point1, point2):
	distance = math.hypot(point2[0] - point1[0], point2[1] - point1[1])
	return distance


simulation()