


#
# This code defines the couples of passes for Juventus and Napoli,
# plots the distributions of the variables defined and train a neural
# network (using the library scikit-learn) to perform a classification
# Then the performance results and the ROC curve are displayed
#



# import the needed packages (in particular 'sklearn' (scikit-learn) used for the
# machine learning tools)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import sklearn
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix


# import the functions defined in the file 'functions_for_classification'
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


# create the passes couples of the two teams and
# plot all the variables in histogram
print('Creating pass couples dataset for '+str(global_variables[0])+'...',end='   ')
couples_juve = create_pass_couples(global_variables[0],teams,events,global_variables)
print('done.')
print('Creating pass couples dataset for '+str(global_variables[1])+'...',end='   ')
couples_nap = create_pass_couples(global_variables[1],teams,events,global_variables)
print('done.')




# create numpy arrays and fill them with the variables of the classification (useful for plotting them)

# average lengths
av_lengths_juve = np.array([ couple['length'] for couple in couples_juve ])
av_lengths_nap = np.array([ couple['length'] for couple in couples_nap ])

# time delays
time_juve = np.array([ couple['time'] for couple in couples_juve ])
time_nap = np.array([ couple['time'] for couple in couples_nap ])

# angle differences
angle_juve = np.array([ couple['angle'] for couple in couples_juve ])
angle_nap = np.array([ couple['angle'] for couple in couples_nap ])

# starting zone of the first pass
start_juve = np.array([ couple['startZone'] for couple in couples_juve ])
start_nap = np.array([ couple['startZone'] for couple in couples_nap ])

# ending zone of the first pass (coincident with the starting zone of the second pass)
med_juve = np.array([ couple['medZone'] for couple in couples_juve ])
med_nap = np.array([ couple['medZone'] for couple in couples_nap ])

# ending zone of the second pass
end_juve = np.array([ couple['endZone'] for couple in couples_juve ])
end_nap = np.array([ couple['endZone'] for couple in couples_nap ])


# make histograms of the distribution of each variable, save them and plot them (just for lengths,
# times and angles)

# average lengths
plt.hist(av_lengths_juve,bins=10,histtype='step',color='r',label='Juventus',range=(0,60))
plt.hist(av_lengths_nap,bins=10,histtype='step',color='g',label='Napoli',range=(0,60))
plt.xlabel('lenght [m]')
plt.ylabel('counts')
plt.title('Distributions of average length\nof consecutive passes')
plt.legend()
plt.savefig('../images/lengths_Juve_Napoli.png',dpi=300)
plt.show()

# time delays
plt.hist(time_juve,bins=15,histtype='step',color='r',label='Juventus',range=(0,15))
plt.hist(time_nap,bins=15,histtype='step',color='g',label='Napoli',range=(0,15))
plt.xlabel('time [s]')
plt.ylabel('counts')
plt.title('Distributions of time delay\nbetween consecutive passes')
plt.legend()
plt.savefig('../images/times_Juve_Napoli.png',dpi=300)
plt.show()

# angle differences
plt.hist(angle_juve,bins=10,histtype='step',color='r',label='Juventus',range=(0,180))
plt.hist(angle_nap,bins=10,histtype='step',color='g',label='Napoli',range=(0,180))
plt.xlabel('angle [degrees]')
plt.ylabel('counts')
plt.title('Distributions of angle difference\nof consecutive passes')
plt.legend(loc='upper left')
plt.savefig('../images/angles_Juve_Napoli.png',dpi=300)
plt.show()


# merge the passes couples of the two teams, then store them in a pandas dataframe;
# the unified dataset will be used for the classification
couples = couples_juve + couples_nap
df = pd.DataFrame(couples)


# delete the useless columns; the 6 variables used are:
# - average length
# - angle
# - time delay
# - fisrt zone
# - second zone
# - third zone

del df['zone']
del df['firstPass']
# del df['length']
# del df['angle']
# del df['time']
# del df['startZone']
# del df['medZone']
# del df['endZone']
# del df['label']


# create the target column with the labels of the correct team
target_column = ['Label']


# define and normalize the predictors
predictors = list(set(list(df.columns))-set(target_column))
df[predictors] = df[predictors]/df[predictors].max()
# df.describe().transpose()


# define variables as X and labels as Y
X = df[predictors].values
Y = df[target_column].values


# split the dataframe in training and testing (80% of data used for training and 20% for testing)
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.20,random_state=1)
print('\nNumber of training event:',len(X_train))
print('\nNumber of testing event:',len(X_test))


# train a MultiLayerPerceptron (neural network):
# - 3 hidden layers with 8 nodes each
# - activation function: max(0,x)
mlp = MLPClassifier(hidden_layer_sizes=(8,8,8),activation='relu',solver='adam',max_iter=150)
mlp.fit(X_train,Y_train.ravel())
predict_train = mlp.predict(X_train)
predict_test = mlp.predict(X_test)


# print the results on training data
print('\n\n--- Results on training data ---\n\n')
print('Confusion matrix:\n\n')
conf_matrix_train = confusion_matrix(Y_train,predict_train)
print(str(conf_matrix_train[0][0])+'\t'+str(conf_matrix_train[0][1]))
print('\n')
print(str(conf_matrix_train[1][0])+'\t'+str(conf_matrix_train[1][1]))
print('\n\nPerformances:\n')
print(classification_report(Y_train,predict_train))


# print the results on testing data
print('\n\n--- Results on testing data ---\n\n')
print('Confusion matrix:\n\n')
conf_matrix_test = confusion_matrix(Y_test,predict_test)
print(str(conf_matrix_test[0][0])+'\t'+str(conf_matrix_test[0][1]))
print('\n')
print(str(conf_matrix_test[1][0])+'\t'+str(conf_matrix_test[1][1]))
print('\n\nPerformances:\n')
print(classification_report(Y_test,predict_test))


# build the ROC curve

# find the false positive rate and true positive rate
probs = mlp.predict_proba(X_test)  
probs = probs[:, 1]  
false_positive_rate, true_positive_rate, thresholds = sklearn.metrics.roc_curve(Y_test,probs)


# go from false positive rate to true negative rate
true_negative_rate = 1 - np.array(false_positive_rate)


# plot the ROC curve
plt.plot(true_positive_rate,true_negative_rate,color='orange',label='Neural Network')
plt.plot([0,1],[1,0],color='darkblue',linestyle='--',label='random classification')
plt.ylabel('True Negative Rate')
plt.xlabel('True Positive Rate')
plt.title('ROC Curve')
plt.grid(alpha=0.5)
plt.legend()
plt.savefig('../images/ROC_curve.png',dpi=300)
plt.show()
  

# compute the area under the ROC curve  
area_under_ROCcurve = sklearn.metrics.roc_auc_score(Y_test,probs)
print('\nArea under the ROC curve:',area_under_ROCcurve)




