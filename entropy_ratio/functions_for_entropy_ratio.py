


#
# This code defines the needed functions to carry out the analysis
# performed using the Entropy Ratio concept, with the related simulations
#



# import the needed packages
import math
import numpy as np



# define a function which generates a simulated dataset of couples
# of passes; the parameters are:
# size -> number of possible states
# numbers -> number of transitions between each couple of states; it
#            defines the transition probability matrix
# steps -> number of transitions generated (passes, not couples)
# new_rate -> probability to make a 'jump' from a state
#             to another (without considering it a transition)
def generate_couples(size,numbers,steps,new_rate):
    
    
    # check types and values of the parameters
    if type(size) != int:
        raise TypeError('The number of states must be an integer number')
        
    if size <= 0:
        raise ValueError('The number of states must be positive')
        
    if not all([ all([ numbers[i][j] >= 0 for j in range(len(numbers[i])) ]) for i in range(len(numbers)) ]):
        raise ValueError('The number of transitions must not be negative')
        
    if type(steps) != int:
        raise TypeError('The number of steps must be an integer number')
        
    if steps <= 0:
        raise ValueError('The number of steps must be positive')
        
    if type(new_rate) not in [int,float]:
        raise TypeError('The probability of a jump must be a number')
        
    if new_rate < 0 or new_rate > 1:
        raise ValueError('The probability of a jump must be between 0 and 1')
        
    if len(numbers) != size:
        raise ValueError('The dimension of the transition matrix must be size^2')
        
    if not all([ len(numbers[i]) == size for i in range(len(numbers)) ]):
        raise ValueError('The dimension of the transition matrix must be size^2')
        
    
    # define some variables for the number of transitions and the related probabilities    
    n_i = np.zeros(size)
    n_ij = numbers
    p_i = np.zeros(size)
    p_ij = np.zeros((size,size))
    
    for i in range(0,size):
        
        for j in range(0,size):
            n_i[i] += n_ij[i][j]

    n_tot = sum(n_i)
    if n_tot == 0:
        raise Exception('The total number of transitions must not be zero')
    
    for i in range(0,size):
        
        try:
            p_i[i] = n_i[i] / n_tot
        except ZeroDivisionError:
            raise ZeroDivisionError('Found total number of transitions equal to 0')
            
        if n_i[i] > 0:
            for j in range(0,size):
                p_ij[i][j] = n_ij[i][j] / n_i[i]
        else:
            for j in range(0,size):
                p_ij[i][j] = 0

    # define the cumulative probabilities
    p_cum_i = np.zeros(size)
    p_cum_ij = np.zeros((size,size))    
    
    tot1 = 0
    for i in range(0,size):
        
        tot1 += p_i[i]
        p_cum_i[i] = tot1
        tot2 = 0
        
        for j in range(0,size):
            
            tot2 += p_ij[i][j]
            p_cum_ij[i][j] = tot2
            
    
    # create the list of couples of passes
    couples = []
    
    first_pass = True
    
    # iterate over all the steps
    
    i = 0
    
    while i < steps:
        
        
        # if we are generating the first pass of a passing chain, we
        # randomly generate the first zone and then the other ones
        if first_pass == True:
            
            # in this case we are generating two passes, so we
            # increase the iterator by two
            i += 2
            
            # generate the first zone
            j = 0
            random_number = np.random.rand()
            while random_number > p_cum_i[j]:
                j += 1
            # we add one to the zone because we want it to start from 1, not
            # from 0
            zone1 = j + 1
            
            # generate the second zone
            j = 0
            random_number = np.random.rand()
            while random_number > p_cum_ij[zone1-1][j]:
                j += 1
            zone2 = j + 1
            # the third zone is always equal to the second one
            zone3 = zone2
            
            # generate the fourth zone
            #
            # ( the property of being a Markov process is
            # imposed here! )
            #
            j = 0
            random_number = np.random.rand()
            while random_number > p_cum_ij[zone3-1][j]:
                j += 1
            zone4 = j + 1
         
        # if we are not generating a 'first pass', the first pass is equal
        # to the last one generated
        else:
            
            # in this case we are generating onw pass, so we
            # increase the iterator by one
            i += 1
            
            # the first three zones are already determined
            zone1 = couples[-1]['zone'][2]
            zone2 = couples[-1]['zone'][3]
            zone3 = zone2
            
            # generate the fourth zone
            j = 0
            random_number = np.random.rand()
            while random_number > p_cum_ij[zone3-1][j]:
                j += 1
            zone4 = j + 1
        
        
        # create a dictionary where to store the informations of the
        # couple of passes and add it to the dataset
        dict = { 'zone' : [zone1,zone2,zone3,zone4] , 'firstPass' : first_pass}
        couples.append(dict)
        
        # generate a random number to decide if to make a 'jump'
        first_pass = np.random.rand() < new_rate
        
        
        
    return couples



# define a function which, given a dataset of number of passes, compute
# the entropy ratio
def SR(couples_dataset,size):
    

    # check types and values of the parameters
    if type(couples_dataset) != list:
        raise TypeError('The couples dataset must be a list')
        
    if len(couples_dataset) == 0:
        raise ValueError('The couples dataset is empty')
        

  
    # define the number of passes
    n_of_passes = 0  
  
    # define and compute the number of passes for different possibilities:
    # - from zone i
    # - from zone i to zone j
    # - zone i --> j --> l
    n_i = np.zeros(size)
    n_ij = np.zeros((size,size))
    n_ijl = np.zeros((size,size,size))
    
    
    # iterate over the dataset
    for couple in couples_dataset:
        
        if couple['firstPass'] == True:
            
            n_i[couple['zone'][0]-1] += 1
            n_i[couple['zone'][2]-1] += 1
            n_ij[couple['zone'][0]-1][couple['zone'][1]-1] += 1
            n_ij[couple['zone'][2]-1][couple['zone'][3]-1] += 1
            
            # if it is a first pass we have two 'new' passes
            n_of_passes += 2
            
        else:
            
            n_i[couple['zone'][2]-1] += 1
            n_ij[couple['zone'][2]-1][couple['zone'][3]-1] += 1
            
            n_of_passes += 1
        
        n_ijl[couple['zone'][0]-1][couple['zone'][1]-1][couple['zone'][3]-1] += 1
        

    # find the different probabilities
    p_i = np.zeros(size)
    p_ij = np.zeros((size,size))
    p_ijl = np.zeros((size,size,size))
                     
    
    if n_of_passes == 0:
        raise Exception('The total number of passes must not be zero')
    
    
    for i in range(0,size):
        
        
        try:
            p_i[i] = n_i[i] / n_of_passes
        except ZeroDivisionError:
            raise ZeroDivisionError('Found null total number of passes, must be positive')
            
            
        if n_i[i] > 0:
            for j in range(0,size):
                p_ij[i][j] = n_ij[i][j] / n_i[i]
        else:
            for j in range(0,size):
                p_ij[i][j] = 0
                

        for j in range(0,size):
            
            
            if n_ij[i][j] > 0:
                for l in range(0,size):
                    p_ijl[i][j][l] = n_ijl[i][j][l] / n_ij[i][j]
            else:
                for l in range(0,size):
                    p_ijl[i][j][l] = 0
                    
                
                               
    # define and compute the entropy and the entropy ratio
    s_i = np.zeros(size)
    s_ij = np.zeros((size,size))
    
    
    for i in range(0,size):
        
        for j in range(0,size):
            
            if p_ij[i][j] > 0:
                s_i[i] -= p_ij[i][j] * math.log(p_ij[i][j])
            else:
                pass
            
        for j in range(0,size):
            
            for l in range(0,size):
                
                if p_ijl[i][j][l] > 0:
                    s_ij[i][j] -= p_ijl[i][j][l] * math.log(p_ijl[i][j][l])
                else:
                    pass
            
    
    # compute the entropy ratio and the total entropy
    SR = 0
    total_entropy = 0
    
    for i in range(0,size):
        
        
        for j in range(0,size):
            
            if s_i[j] > 0:
                SR_ij = s_ij[i][j] / s_i[j]
                
            else:
                SR_ij = 0
                
            SR += SR_ij * p_ij[i][j] * p_i[i]
            
            if p_ij[i][j] > 0:
                total_entropy -= p_i[i] * p_ij[i][j] * math.log(p_ij[i][j])
            else:
                pass
           
            
    # return a list with SR, total entropy and number of transitions (used
    # to make simulations)
    return [SR,total_entropy,n_ij] 






