


#
# This code tests all the functions included in the file 'functions.py'
# Those functions are used in the file 'classification.py' and will be tested here
# both in positive and in negative ways
#



# import the needed packages
import numpy as np
import json
import pytest


# import the the functions to be tested from the file
from functions import check_global_variables,zone,perc_to_len,create_pass_couples


# load all the teams, competitions and players from the datasets (competitions and players are not needed here)
with open("../data/teams.json") as f:
    teams = json.load(f)
# with open("../data/competitions.json") as g:
#     competitions = json.load(g)
# with open("../data/players.json") as h:
#     players = json.load(h)
   

# load the matches and the events of italian Serie A from the datasets
with open("../data/events_Italy/events_Italy.json") as l:
    events = json.load(l)
with open("../data/matches/matches_Italy.json") as m:
    matches = json.load(m)
    
    
# inizialize the global variable, which are used by the functions

FIRST_TEAM = 'Juventus'
SECOND_TEAM = 'Napoli'
LENGTH = 105.0
WIDTH = 68.0
N_COLUMNS = 5
N_ROWS = 4
NUMBER_OF_ZONES = N_ROWS * N_COLUMNS
ZONE_LENGTH = 100 / N_COLUMNS
ZONE_WIDTH = 100 / N_ROWS
global_variables = [FIRST_TEAM,SECOND_TEAM,LENGTH,WIDTH,N_COLUMNS,N_ROWS,NUMBER_OF_ZONES,ZONE_LENGTH,ZONE_WIDTH]



# test the function 'check_global_variables'
def test_check_global_variables():
    
    
    '''
    in order to test this function, a copy of the global_variables set is
    created
    '''
    
    
    # copy of the global_variables set
    glob_var_copy = list(global_variables)
    
    
    # test if the function returns 0 without exceptions if the right
    # set of variables is passes
    assert check_global_variables(glob_var_copy) == 0
    
    
    # test if the function returns 0 without exceptions if the glovìbal variables
    # are changed in a valid way
    glob_var_copy[0] = 'Milan'
    glob_var_copy[2] = 12.0
    glob_var_copy[4] = 1
    glob_var_copy[6] = glob_var_copy[4] * glob_var_copy[5]
    glob_var_copy[7] = 100 / glob_var_copy[4]
    assert check_global_variables(glob_var_copy) == 0
    
    
    # check if changing some elements with wrong types TypeError is raised
    glob_var_copy = list(global_variables)
    glob_var_copy[0] = 43.7
    pytest.raises(TypeError,check_global_variables,glob_var_copy)
    
    
    glob_var_copy = list(global_variables)
    glob_var_copy[8] = 'Zone_width'
    pytest.raises(TypeError,check_global_variables,glob_var_copy)
    
    
    glob_var_copy = list(global_variables)
    glob_var_copy[4] = 5.0
    pytest.raises(TypeError,check_global_variables,glob_var_copy)
    

    # check if passing a null tuple or a tuple of wrong length an Exception
    # is raised
    glob_var_copy = []
    pytest.raises(Exception,check_global_variables,glob_var_copy)
    
    glob_var_copy = ['Juventus','Napoli',105.0]
    pytest.raises(Exception,check_global_variables,glob_var_copy)
    
    glob_var_copy = [1,2,3,4,5,6,7,8,9,10]
    pytest.raises(Exception,check_global_variables,glob_var_copy)
    
    
    # check if passing a variale of wrong type a TypeError (must be a
    # tuple) is raised
    glob_var_copy = 'Juventus is better than Napoli'
    pytest.raises(TypeError,check_global_variables,glob_var_copy)
    
    glob_var_copy = np.zeros(9)
    pytest.raises(TypeError,check_global_variables,glob_var_copy)
    
    
    # check if the global variables are not in the correct range a ValueError
    # is raised
    glob_var_copy = list(global_variables)
    glob_var_copy[2] = -3.0
    pytest.raises(ValueError,check_global_variables,glob_var_copy)
    
    
    # check if relations between variables are ensured (otherwise, Exception should
    # be raised)
    glob_var_copy = list(global_variables)
    glob_var_copy[6] = 555
    pytest.raises(Exception,check_global_variables,glob_var_copy)
    
    glob_var_copy = list(global_variables)
    glob_var_copy[8] = 99
    pytest.raises(Exception,check_global_variables,glob_var_copy)


    return 0

test_check_global_variables()



# test the function 'zone'
def test_zone():
    
    
    # check if the function returns correct values for some points
    assert zone(0,0,global_variables) == 1
    assert zone(10,10,global_variables) == 1
    assert zone(100,100,global_variables) == 20
    assert zone(100,0,global_variables) == 5
    assert zone(20,25,global_variables) == 7            # the border is assigned to the forward-right zone
    assert zone(65,51,global_variables) == 14
    assert zone(0,100,global_variables) == 16
    assert zone(50,50,global_variables) == 13
    
    
    # check if a TypeError is raised if non-integer numbers are passed
    # to the function
    pytest.raises(TypeError,zone,23.0,11,global_variables)
    pytest.raises(TypeError,zone,[12,58],global_variables)
    pytest.raises(TypeError,zone,'Left line','Midfield line',global_variables)
    
    
    # check if the function raises a ValueError if parameters out of range
    # are passed
    pytest.raises(ValueError,zone,-1,40,global_variables)
    pytest.raises(ValueError,zone,89,120,global_variables)
    
    
    return 0

test_zone()



# test the function 'perc_to_len'
def test_perc_to_len():
    
    
    # check the correct behavior of the function
    assert perc_to_len(50,20) == 10
    assert perc_to_len(50,20.0) == 10
    assert perc_to_len(13,50) == 6.5
    assert perc_to_len(0,0) == 0
    assert perc_to_len(0,200) == 0
    assert perc_to_len(60,0) == 0
    assert perc_to_len(0,200) == 0
    assert perc_to_len(100,456.78) == 456.78
    
    
    # check if a TypeError is raised if one of the parameter is not acceptable
    pytest.raises(TypeError,perc_to_len,50.0,20)
    pytest.raises(TypeError,perc_to_len,50,'factor')
    pytest.raises(TypeError,perc_to_len,50.0,[20,30,40])
    
    
    # check if a ValueError is raised if the parameters are not in the right range
    pytest.raises(ValueError,perc_to_len,-11,32.5)
    pytest.raises(ValueError,perc_to_len,11,-345)
    pytest.raises(ValueError,perc_to_len,101,32.5)
    
    
    return 0

test_perc_to_len()
    
    
    
# test the function 'create_pass_couples'
def test_create_pass_couples(test_team):
    
    
    # check if, passing a correct team name and correct parameters,
    # the function produces a valid dataset
    couples = create_pass_couples(test_team,teams,events,global_variables)
    
    lengths = [ couples[i]['length'] for i in range(len(couples)) ]
    first_passes = [ couples[i]['firstPass'] for i in range(len(couples)) ]
    angles = [ couples[i]['angle'] for i in range(len(couples)) ]
    times = [ couples[i]['time'] for i in range(len(couples)) ]
    labels = [ couples[i]['Label'] for i in range(len(couples)) ]
    zones = [ couples[i]['zone'] for i in range(len(couples)) ]
    
    assert type(couples) == list
    assert len(couples) > 0
    
    assert all([ type(length) in [int,float] for length in lengths ])
    assert all([ length>=0 for length in lengths ])
    assert all([ length<=np.sqrt(global_variables[2]**2 + global_variables[3]) for length in lengths ])
    
    assert all([ type(first_pass) == bool for first_pass in first_passes ])
    
    assert all([ type(angle) == float for angle in angles ])
    assert all([ angle>=0 for angle in angles ])
    assert all([ angle<=180 for angle in angles ])
    
    assert all([ type(time) == float for time in times ])
    assert all([ time>=0 for time in times ])
    
    assert all([ label in [-1,0,1] for label in labels ])
    
    assert all([ type(zone) == list for zone in zones ])
    assert all([ len(zone) == 4 for zone in zones ])
    assert all([ np.min(zone) >= 1 and np.max(zone) <= 20 for zone in zones ])
    assert all([ all([ type(z) == int for z in zone ]) for zone in zones ])
    
    
    
    # check if passing a wrong team name it raises an Exception
    pytest.raises(Exception,create_pass_couples,'A. S. D. Real Cava',teams,events,global_variables)
    
    
    # check if a TypeException is raised when the team name has a wrong type
    pytest.raises(TypeError,create_pass_couples,0.5,teams,events,global_variables)
    pytest.raises(TypeError,create_pass_couples,['Juventus','Napoli'],teams,events,global_variables)
    
    
    # check if a ValueError is raised when the datasets are empty
    pytest.raises(ValueError,create_pass_couples,test_team,[],events,global_variables)
    pytest.raises(ValueError,create_pass_couples,test_team,teams,[],global_variables)
    
    
    
    return 0

test_create_pass_couples('Juventus')
test_create_pass_couples('Milan')
test_create_pass_couples('Sampdoria')
    



