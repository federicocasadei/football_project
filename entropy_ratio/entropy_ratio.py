


#
# 
#



# import the needed packages
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd



# import the functions defined in the files 'functions' and
# 'functions_for_entropy_ratio'
from functions import check_global_variables,zone,perc_to_len,create_pass_couples
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


# define the teams on which perform the classification
FIRST_TEAM = 'Juventus'
SECOND_TEAM = 'Napoli'


# define the pitch dimensions in meters
LENGTH = 105.0
WIDTH = 68.0
    
 
# define the number of zones on the pitch
N_COLUMNS = 5
N_ROWS = 4
NUMBER_OF_ZONES = N_ROWS * N_COLUMNS
    

# compute the lenght and width of the zones (in %
# of the pitch dimensions)
try:
    ZONE_LENGTH = 100 / N_COLUMNS
    ZONE_WIDTH = 100 / N_ROWS
except ZeroDivisionError:
    raise ZeroDivisionError('The number of rows and columns of the zones must be positive')

    
# merge together the global variables; this tuple will be passed to the functions
# that need them in a more compact way
global_variables = [FIRST_TEAM,SECOND_TEAM,LENGTH,WIDTH,N_COLUMNS,N_ROWS,NUMBER_OF_ZONES,ZONE_LENGTH,ZONE_WIDTH]


# check the validity of the global variables (then used in the following functions without checking)
check_global_variables(global_variables)



# set a seed to be able to reproduce data
np.random.seed(0)


# create the dataset with the pass couples for Juventus, used then to
# make Markov simulations with the transition probabilities estimated
# by them
couples_juve = create_pass_couples('Juventus',teams,events,global_variables)


# use the SR function to compute the number of transitions between
# the zones (no entropy ration needed for now)
n_ij_juve = SR(couples_juve,global_variables[6])[2]


# create another matrix with the number of transitions
# with a Poisson distribution
n_ij_poisson = np.zeros((global_variables[6],global_variables[6]))

for i in range(0,global_variables[6]):
    
    for j in range(0,global_variables[6]):
        
        n_ij_poisson[i][j] = np.random.poisson(50)
        

# simulate a Markov process, using the probabilities coming from
# the Juventus couples of passes and from the Poissonian ones, with
# different number of steps; then compute the entropy ratio for
# each of them
# the new_rate parameter is set to zero, beacuse now the jumps
# between zones are not considered

number_of_steps = [1000,5000,10000,30000,50000,75000,100000]

SR_markov_juve = np.zeros(len(number_of_steps))
SR_markov_poisson = np.zeros(len(number_of_steps))

for i in range(len(number_of_steps)):
    
    
    # simulate the Markov process
    markov_juve = generate_couples(global_variables[6],n_ij_juve,number_of_steps[i],0)
    markov_poisson = generate_couples(global_variables[6],n_ij_poisson,number_of_steps[i],0)
    
    # compute the entropy ratio for the two cases
    SR_markov_juve[i] = SR(markov_juve,global_variables[6])[0]
    SR_markov_poisson[i] = SR(markov_poisson,global_variables[6])[0]
    
    
# create the plot of the entropy ratio as a function of the number of transitions
# for the two cases, save it and show it
plt.scatter(number_of_steps,SR_markov_juve,color='red',label='Juventus')
plt.plot(number_of_steps,SR_markov_juve,color='red',alpha=0.6)
plt.scatter(number_of_steps,SR_markov_poisson,color='green',label='Poisson')
plt.plot(number_of_steps,SR_markov_poisson,color='green',alpha=0.6)
plt.xlabel('number of transitions')
plt.ylabel('Entropy Ratio')
plt.title('Entropy Ratio vs number of transitions')
plt.grid(alpha=0.5)
plt.gca().axhline(1,color='blue',linestyle='dashed')
plt.legend()

plt.savefig('../images/Markov_simulation.png',dpi=300)
plt.show()




# simulate a Markov process, using the probabilities coming from
# the Juventus couples of passes and from the Poissonian ones, with
# different number of steps; then compute the entropy ratio for
# each of them
# the new_rate parameter is set to 0.3, to simulate a typical 'jump'
# probability of football teams
      
SR_markov_juve_jump = np.zeros(len(number_of_steps))
SR_markov_poisson_jump = np.zeros(len(number_of_steps))

for i in range(len(number_of_steps)):
    
    
    # simulate the Markov process
    markov_juve = generate_couples(global_variables[6],n_ij_juve,number_of_steps[i],0.3)
    markov_poisson = generate_couples(global_variables[6],n_ij_poisson,number_of_steps[i],0.3)
    
    # compute the entropy ratio for the two cases
    SR_markov_juve_jump[i] = SR(markov_juve,global_variables[6])[0]
    SR_markov_poisson_jump[i] = SR(markov_poisson,global_variables[6])[0]
    
    
# create the plot of the entropy ratio as a function of the number of transitions
# for the two cases, save it and show it
plt.scatter(number_of_steps,SR_markov_juve_jump,color='red',label='Juventus')
plt.plot(number_of_steps,SR_markov_juve_jump,color='red',alpha=0.6)
plt.scatter(number_of_steps,SR_markov_poisson_jump,color='green',label='Poisson')
plt.plot(number_of_steps,SR_markov_poisson_jump,color='green',alpha=0.6)
plt.xlabel('number of transitions')
plt.ylabel('Entropy Ratio')
plt.title('Entropy Ratio vs number of transitions')
plt.grid(alpha=0.5)
# plt.gca().axhline(1,color='blue',linestyle='dashed')
plt.legend()

plt.savefig('../images/Markov_simulation_jumps.png',dpi=300)
plt.show()





# build up the pass couples dataset for each Serie A team, finding the
# number of passes and computing the entropy ratio; then a simulated
# dataset is created for each team and the relative entropy ratio is
# computed
# this allows to find the \eta parameter (making the ratio)


# create a dataframe to store the results
df = pd.DataFrame(columns=['Team','number of passes','Entropy Ratio','Markov SR','eta'])


# iterate over all the teams
for team in teams:

    # we need to exclude 'Italy', which is the italian national team
    if team['area']['name'] == 'Italy' and team['name'] != 'Italy':
        
        
        # create the pass couples dataset
        couples = create_pass_couples(team['name'],teams,events,global_variables)
        
        # count the number of passes and the jump probability
        number_of_first_passes = 0
        number_of_passes = 0
        new_rate = 0.0
        
        for couple in couples:
            
            if couple['firstPass'] == True:
                number_of_first_passes += 1
                number_of_passes += 2
            
            else:
                number_of_passes += 1
        
                
        # the jump probability is not the number of first passes divided by
        # the total number of passes; it has to be divided by the number of
        # couples in the dataset
        try:
            new_rate = number_of_first_passes / len(couples)
        except ZeroDivisionError:
            raise ZeroDivisionError('The number of pass couples is found to be zero')
            
            
        # compute the entropy ratio
        entropy_ratio = SR(couples,global_variables[6])[0]
        
        
        
        # find the number of transitions between zones
        numbers = SR(couples,global_variables[6])[2]
            
        # make a simulation with the number of transitions between zones, the
        # number of passes and the jump probability as estimated by the
        # team itself; then compute the entropy ratio
        simulated_couples = generate_couples(global_variables[6],numbers,number_of_passes,new_rate)
        simulated_entropy_ratio = SR(simulated_couples,global_variables[6])[0]
        
        
        
        # make the ratio between entropy ratios to get the \eta parameter
        try:
            eta = entropy_ratio / simulated_entropy_ratio
        except ZeroDivisionError:
            raise ZeroDivisionError('The simulated Entropy Ratio is found to be zero')
            
        
        # add a row in the dataframe
        df.loc[len(df.index)] = [team['name'],number_of_passes,entropy_ratio,simulated_entropy_ratio,eta]        
        
        
       
# sort the dataframe by team name and display the results
df = df.sort_values('Team')
print(df.loc[:,df.columns!='number of passes'])     
        


# build up the plots, save and show them

# entropy ratio vs number of passes
plt.scatter(df.iloc[:,1].values,df.iloc[:,2].values,color='red')
plt.grid(alpha=0.5)
plt.title('Entropy Ratio vs number of passes')
plt.xlabel('number of passes')
plt.ylabel('Entropy Ratio')

plt.savefig('../images/entropy_ratio_teams.png',dpi=300)
plt.show()


# entropy ratio, simulated entropy ratio and eta vs
# number of passes
plt.scatter(df.iloc[:,1].values,df.iloc[:,2].values,color='red',label='$\hat{SR}$')
plt.scatter(df.iloc[:,1].values,df.iloc[:,3].values,color='blue',label='$\hat{SR^M}$')
plt.scatter(df.iloc[:,1].values,df.iloc[:,4].values,color='green',label='$\eta$')
plt.grid(alpha=0.5)
plt.title('Entropy Ratio vs number of passes')
plt.xlabel('number of passes')
plt.ylabel('Entropy Ratio')
plt.legend()

plt.savefig('../images/SR_and_eta_teams.png',dpi=300)
plt.show()

        
        

# find the points and sored goals for each team to look for a possible correlation
df_standings = pd.DataFrame(columns=['Team','points','goals scored'])

# iterate over all the teams
for team in teams:

    # we need to exclude 'Italy', which is the italian national team
    if team['area']['name'] == 'Italy' and team['name'] != 'Italy':    
        
        
        points = 0
        goals = 0
        
        for match in matches:
            if team['name'] in match['label']:
                if match['winner'] == team['wyId']:
                    points += 3
                elif match['winner'] == 0:
                    points += 1
                goals += match['teamsData'][str(team['wyId'])]['score']
                
                
        df_standings.loc[len(df_standings.index)] = [team['name'],points,goals]
        
        

# display the standings
df_standings = df_standings.sort_values('points',ascending=False)
print(df_standings)


# build up the scatter plot of points and goals scored vs eta

# sort the dataframe to match the order of the first one (where
# the entropy ratios and eta are stored)
df_standings = df_standings.sort_values('Team')


# eta vs points
plt.scatter(df.iloc[:,4],df_standings.iloc[:,1],color='red')
plt.grid(alpha=0.5)
plt.title('$\eta$ vs points')
plt.xlabel('$\eta$')
plt.ylabel('points')

plt.show()


# eta vs goals scored
plt.scatter(df.iloc[:,4],df_standings.iloc[:,2],color='red')
plt.grid(alpha=0.5)
plt.title('$\eta$ vs goals scored')
plt.xlabel('$\eta$')
plt.ylabel('goals scored')

plt.show()






