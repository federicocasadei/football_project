


#
# This code tests all the functions included in the file 'functions_for_entropy_ratio.py'
# Those functions are used in the file 'entropy_ratio.py' and will be tested here
# both in positive and in negative ways
#



# import the needed packages
import numpy as np
import json
import pytest



# The functions imported from 'functions.py' are tested in the file
# 'classification_tests.py' and so are not tested here


# import the the functions to be tested from the file
from functions_for_entropy_ratio import generate_couples,SR


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



# test the function 'generate_couples'
def test_generate_couples():
    
    
    
    # check the validity of the returned variable
    numbers = [[34,22,1],[45,0,3],[4,5,78]]
    couples = generate_couples(3,numbers,10,0.5)
    assert type(couples) == list
    assert len(couples) <= 10 - 1
    assert all([ type(couples[i]) == dict for i in range(len(couples)) ])
    assert all([ len(couple['zone']) == 4 for couple in couples ])
    assert all([ all([ type(couple['zone'][i]) == int for i in range(len(couple)) ]) for couple in couples ])
    assert all([ all([ zone >= 1 and zone <= 3 for zone in couple['zone'] ]) for couple in couples ])
    assert all([ type(couple['firstPass']) == bool for couple in couples ])
    
    # putting the jump probability to 0 or 1, the number of couples should
    # be respectively 10 - 1 and 5
    couples = generate_couples(3,numbers,10,0)
    assert len(couples) == 10 - 1
    couples = generate_couples(3,numbers,10,1)
    assert len(couples) == 5
    
    
    # check if a TypeError is raised if wrong parameters are passed
    pytest.raises(TypeError,generate_couples,3,numbers,10,'unlikely')
    pytest.raises(TypeError,generate_couples,3,numbers,10.5,0.5)
    pytest.raises(TypeError,generate_couples,[3,6,7],numbers,10,0.5)
    
    # check if a ValueError is raised if parameters out of range are passed
    pytest.raises(ValueError,generate_couples,-1,numbers,10,0.5)
    pytest.raises(ValueError,generate_couples,0,numbers,10,0.5)
    pytest.raises(ValueError,generate_couples,3,numbers,-45,0.5)
    pytest.raises(ValueError,generate_couples,3,numbers,10,-1.5)
    pytest.raises(ValueError,generate_couples,3,numbers,10,1.1)
    negative_numbers = [[-34,-22,-1],[-45,0,-3],[-4,-5,-78]]
    pytest.raises(ValueError,generate_couples,3,negative_numbers,10,0.5)
    
    # check if a ValueError is raised if 'size' and 'numbers' are
    # not compatible
    pytest.raises(ValueError,generate_couples,6,numbers,10,1.1)
    
    # check if an Exception is raised if the total number of passes (in the
    # transition matrix) is zero
    empty_numbers = [[0,0,0],[0,0,0],[0,0,0]]
    pytest.raises(Exception,generate_couples,3,empty_numbers,10,0.5)
    
    
    return 0


test_generate_couples()



# test the function 'SR'
def test_SR():
    
    
    
    # check the validity of the returned variable
    numbers = [[34,22,1],[45,0,3],[4,5,78]]
    couples = generate_couples(3,numbers,10,0.5)
    entropy_ratio,total_entropy,n_ij = SR(couples,3)
    assert len(n_ij) == 3
    assert all([ len(n_ij[i]) == 3 for i in range(len(n_ij)) ])
    assert entropy_ratio >= 0 and entropy_ratio <= 1
    assert total_entropy >= 0
    
    
    # check if a TypeError is raised couples_dataset is not a list
    pytest.raises(TypeError,SR,'couples',global_variables)
    pytest.raises(TypeError,SR,3.5,global_variables)
    
    # check if a ValueError is raised if the length of
    # couples_dataset is zero
    pytest.raises(ValueError,SR,[],global_variables)
    
    
    return 0


test_SR()
    
    
    
    
    
    
    
    
    
    
    
    
    
    