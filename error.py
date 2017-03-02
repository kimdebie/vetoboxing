
'''''''''
''
'' error.py
''
'' This script is designed to check user input.
''
'' by: Kim de Bie
'' created: 2 February 2016
'' last updated: 5 June 2016
''
'''''''''


def errorcheck(number_dimensions, voters, status_quo, alter_status_quo, drift_status_quo, drift_players, preference_shape, visualize):

    errorcheck_passed = True

    agenda_setter_found = False

    # check if all voters have the correct length
    for voter in voters:

        if preference_shape == 'circle':
            # check if all voters have the correct length
            if number_dimensions != len(voter.position):
                print ('Voters do not seem to have the correct number of dimensions. The program will now exit.')
                errorcheck_passed = False

        if preference_shape == 'ellipse':
            if number_dimensions != 2:
                print ('Elliptical preferences can only have two dimensions. The program will now exit.')
            if len(voter.position) != 5:
                print ('Elliptical preferences input incorrect (values may be missing). The program will now exit.')

        # check if there is only one agenda setter
        if voter.agenda_setter == True:
            if agenda_setter_found == True:
                print ('You have entered multiple agenda setters. The program will now exit.')
                errorcheck_passed = False
            else:
                agenda_setter_found = True

    # check if the status quo has a drift of correct length
    if alter_status_quo == 'history and drift':
        if len(drift_status_quo) != number_dimensions:
            print ('The drift of your status quo does not have the correct number of dimensions. The program will now exit.')
            errorcheck_passed = False

    # check if the players have a drift of correct length
    if alter_status_quo == 'history and drift':
        if len(drift_players) != number_dimensions:
            print ('The drift of your players does not have the correct number of dimensions. The program will now exit.')
            errorcheck_passed = False

    # check if the user attempts to create a visualization of a non-two-dimensional simulation
    if visualize == True and number_dimensions != 2:
        print ('Visualizations are only possible in two-dimensional simulations. The program will now exit.')
        errorcheck_passed = False

    return errorcheck_passed
