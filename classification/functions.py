


#
# This code defines the needed functions to carry out the classification
# between couples of passes of Juventus and Napoli (but the functions could
# be re-used for other purposes)
#



# import the needed packages 
import math
import numpy as np


# define a function which checks that the global variables, stored in the global_variables variable,
# are valid (they will be used in all the functions; this function, to be called before everything,
# avoid each function to check the variable each time they are called)
def check_global_variables(global_variables):
    
    '''
    0,1 ---> names of the teams (str)
    2,3 ---> length and width of the pitch, must be >0 (float)
    4,5,6 ---> number of rows, columns and total number of zones defined on the
               pitch, must be >0 (int)
               In addition, the number of zones must be the product of the
               number of rows times the number of columns
    7,8 ---> length and width of a single zone (in %), must be >0 and <=100 (float)
             They are defined as 100/n_rows and 100/n_columns
    '''
    
    if type(global_variables) != list:                                         # type 1
        raise TypeError('The global_variable variable should be a tuple')
        
    if len(global_variables) != 9:                                              # length
        raise Exception('The number of global variables should be 9 but is found to be'+str(len(global_variables)))
        
    types = [ type(i) for i in global_variables ]
    if types != [str,str,float,float,int,int,int,float,float]:                  # type 2
        raise TypeError('Some of the global variables are of unexpected type')

    if np.min(global_variables[2:]) <= 0:                                       # >0
        raise ValueError('Non-positive value encountered within the global variables')
    
    if global_variables[7]>100 or global_variables[8]>100:                      # <=100
        raise ValueError('Length and width of the zones must not be grater than 100%')
        
    if global_variables[6] != global_variables[4] * global_variables[5]:        # n_zones = n_r * n_c
        raise Exception('The number of zone must be the product of the number of rows times the number of columns')
        
    if global_variables[7] != 100 / global_variables[4]:
        raise Exception('Wrong relation between pitch length and zone length')
        
    if global_variables[8] != 100 / global_variables[5]:
        raise Exception('Wrong relation between pitch width and zone width')
        
    return 0
    

# define a function which return the zone number, given a 2D point on
# the pitch (x and y are assumed to be % of the pitch dimensions, as
# data are)
def zone(x,y,global_variables):
    
    # check the type (must be integer)
    if type(x) != int or type(y) != int:
        raise TypeError('The x and y positions on the pitch must be integers')
    
    # check the position
    if x<0 or x>100 or y<0 or y>100:
        raise ValueError('Invalid 2D point:\nx = '+str(x)+'\t;\ty = '+str(y))
    
    
    try:
        i = int(x//global_variables[7])
        j = int(y//global_variables[8])
    except ZeroDivisionError:
        raise ZeroDivisionError('The lenght and width of the zones must be positive')
    
    if x==100:
        i -= 1
    if y==100:
        j -= 1
            
    # find the zone on the pitch and check its type and value
    zone_ = j*global_variables[4] + i + 1
    if type(zone_) != int:
        raise TypeError('Non-integer zone encountered')
    if zone_<1 or zone_>global_variables[6]:
        raise Exception('A zone number must be between 1 and '+str(global_variables[6])+'\nFound zone: '+str(zone_))
        
    return zone_
        


# define a function to convert from % to length or width on the pitch
# (the factor argument can be the total lenght or the width of the pitch)
def perc_to_len(perc,factor):
    
    # check the type (must be integer)
    if type(perc) != int:
        raise TypeError('The % values must be integers')
        
    # check the value
    if perc<0 or perc>100:
        raise ValueError('Invalid % value: '+str(perc))
        
    # check the type of the multiplicative factor (accepted int or float)
    if type(factor) not in [int,float]:
        raise TypeError('The multiplicative factor must be a number')
        
    # check the value of the multiplicative factor (must not be negative)
    if factor < 0:
        raise ValueError('The multiplicative factor must not be negative')
        
    result = perc / 100 * factor
    if result < 0:
        raise Exception('The length must not be negative\nFound length = '+str(result))
        
    return perc / 100 * factor

    

# define a function function that create the dataset of couples of passes
def create_pass_couples(team_name,teams,events,global_variables):
    
    # check the type (must be string)
    if type(team_name) != str:
        raise TypeError('Invalid team name: must be a string')
    
    
    # find the total number of events and check it is not zero
    N = len(events)
    if N==0:
        raise ValueError('The event dataset is empty')
        
        
    # find the total number of teams and check it is not zero
    M = len(teams)
    if M==0:
        raise ValueError('The teams dataset is empty')
    
    
        
    # find the team id
    team_id = -1
    for team in teams:
        if team['name'] == team_name:
            team_id = team['wyId']
    if team_id == -1:
        raise Exception('Team id not found in the dataset')
    
    
    
    # create the pass couples dataset (it is a list of dictionaries)
    couples = []
    
    # define a variable that will be used to discriminate between a couple of passes which starts a chain
    # and one that does not
    first_pass = True
    
    # iterate over all the events (it starts from the second event on purpose):
    for i in range(1,N):
        
        # if two consecutive events are made from the same team ...
        if events[i]['teamId'] == team_id and events[i-1]['teamId'] == team_id:
            
            # ... and if they are both passes ...
            if events[i]['eventName'] == 'Pass' and events[i-1]['eventName'] == 'Pass':
                
                # ... performed in the same match ...
                if events[i]['matchId'] == events[i-1]['matchId']:
                    
                    # ... and in the same half:
                    if events[i]['matchPeriod'] == events[i-1]['matchPeriod']:
                        
                        # all the conditions are satisfied: define the parameters
                        # of the couple and add it to the dataset
                        
                        # find the initial and final positions, on the pitch, of the two passes
                        # (data are such that x2==x3 and y2==y3)
                        x1 = perc_to_len(events[i-1]['positions'][0]['x'],global_variables[2])
                        x2 = perc_to_len(events[i-1]['positions'][1]['x'],global_variables[2])
                        x3 = perc_to_len(events[i]['positions'][0]['x'],global_variables[2])
                        x4 = perc_to_len(events[i]['positions'][1]['x'],global_variables[2])
                        
                        y1 = perc_to_len(events[i-1]['positions'][0]['y'],global_variables[3])
                        y2 = perc_to_len(events[i-1]['positions'][1]['y'],global_variables[3])
                        y3 = perc_to_len(events[i]['positions'][0]['y'],global_variables[3])
                        y4 = perc_to_len(events[i]['positions'][1]['y'],global_variables[3])
                        
                        # check that the positions are inside the pitch
                        if np.min([x1,x2,x3,x4])<0 or np.max([x1,x2,x3,x4])>global_variables[2]:
                            raise ValueError('Invalid x position encountered:',[x1,x2,x3,x4])
                        if np.min([y1,y2,y3,y4])<0 or np.max([y1,y2,y3,y4])>global_variables[3]:
                            raise ValueError('Invalid y position encountered:',[y1,y2,y3,y4])
                        
                        # compute the average lenght of the two passes
                        av_length = ( math.dist((x1,y1),(x2,y2)) + math.dist((x3,y3),(x4,y4)) ) / 2
                        
                        # compute the angle of the two passes
                        theta1 = math.atan2(y2-y1,x2-x1)
                        theta2 = math.atan2(y4-y3,x4-x3)

                        # compute the difference of the angles and correct to make it lay between 0°
                        # and 180°
                        theta = math.fabs(theta2-theta1)
                        if theta > math.pi:
                            theta = 2*math.pi - theta
                            
                        # convert from radiants to degrees
                        theta = math.degrees(theta)
                        
                        # find the timestamps of the two passes
                        time1 = events[i-1]['eventSec']
                        time2 = events[i]['eventSec']
                        
                        # compute the time difference and check that it's not negative
                        delta_t = time2 - time1
                        if delta_t<0:
                            raise ValueError('The time delay between two consecutive passes must not be negative')
                        
                        
                        # assign a label to the two teams among which one wants to do
                        # the classification
                        label = -1
                        if team_name == global_variables[0]:
                            label = 1
                        if team_name == global_variables[1]:
                            label = 0
                        
                        # find the initial and final zones of the two passes
                        # (data are such that zone2==zone3)
                        zone1 = zone(events[i-1]['positions'][0]['x'],events[i-1]['positions'][0]['y'],global_variables)
                        zone2 = zone(events[i-1]['positions'][1]['x'],events[i-1]['positions'][1]['y'],global_variables)
                        zone3 = zone(events[i]['positions'][0]['x'],events[i]['positions'][0]['y'],global_variables)
                        zone4 = zone(events[i]['positions'][1]['x'],events[i]['positions'][1]['y'],global_variables)
                        
                        zones = [zone1,zone2,zone3,zone4]
                        
                        # cut the couples with a time delay greater than 30 s, make sure that zone2==zone3 and
                        # build up the dictionary with all the variables; then append it to the dataset
                        if delta_t <= 30 and zone2 == zone3:
                            dict = { 'length' : av_length , 'angle' : theta , 'time' : delta_t , 'zone' : zones , 'firstPass' : first_pass , 'startZone' : zones[0] , 'medZone' : zones[1] , 'endZone' : zones[3] , 'Label' : label }
                            couples.append(dict)
                            first_pass = False
                        else:
                            first_pass = True
                    else:
                        first_pass = True
                else:
                    first_pass = True
            else:
                first_pass = True
        else:
            first_pass = True
          
            
    return couples
                        

