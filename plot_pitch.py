


#
# This code plots a football pitch (using the function 'createPitch' in the
# file 'FCPython') and the 20 zones used for the project
#



# import pyplot
import matplotlib.pyplot as plt


# define the pitch dimensions in meters and the colors of the lines
LENGTH = 105.0
WIDTH = 68.0
linecolor = 'white'
linecolor2 = 'black'


# import the function used to plot the pitch and plot it
from FCPython import createPitch
fig, ax = createPitch(LENGTH,WIDTH,'meters',linecolor)


# set the color of the pitch
fig.set_facecolor('green')


# draw the lines that define the 20 zones on the pitch
plt.plot([LENGTH/5,LENGTH/5],[0,WIDTH], color=linecolor2, linestyle='dashed')
plt.plot([2*LENGTH/5,2*LENGTH/5],[0,WIDTH], color=linecolor2, linestyle='dashed')
plt.plot([3*LENGTH/5,3*LENGTH/5],[0,WIDTH], color=linecolor2, linestyle='dashed')
plt.plot([4*LENGTH/5,4*LENGTH/5],[0,WIDTH], color=linecolor2, linestyle='dashed')
plt.plot([0,LENGTH],[WIDTH/4,WIDTH/4], color=linecolor2, linestyle='dashed')
plt.plot([0,LENGTH],[2*WIDTH/4,2*WIDTH/4], color=linecolor2, linestyle='dashed')
plt.plot([0,LENGTH],[3*WIDTH/4,3*WIDTH/4], color=linecolor2, linestyle='dashed')



# write the number of each zone
plt.text(LENGTH/10,7*WIDTH/8,'1',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(LENGTH/10,5*WIDTH/8,'6',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(LENGTH/10,3*WIDTH/8,'11',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(LENGTH/10,WIDTH/8,'16',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(3*LENGTH/10,7*WIDTH/8,'2',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(3*LENGTH/10,5*WIDTH/8,'7',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(3*LENGTH/10,3*WIDTH/8,'12',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(3*LENGTH/10,WIDTH/8,'17',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(5*LENGTH/10,7*WIDTH/8,'3',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(5*LENGTH/10,5*WIDTH/8,'8',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(5*LENGTH/10,3*WIDTH/8,'13',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(5*LENGTH/10,WIDTH/8,'18',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(7*LENGTH/10,7*WIDTH/8,'4',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(7*LENGTH/10,5*WIDTH/8,'9',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(7*LENGTH/10,3*WIDTH/8,'14',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(7*LENGTH/10,WIDTH/8,'19',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(9*LENGTH/10,7*WIDTH/8,'5',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(9*LENGTH/10,5*WIDTH/8,'10',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(9*LENGTH/10,3*WIDTH/8,'15',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)
plt.text(9*LENGTH/10,WIDTH/8,'20',size=20, horizontalalignment='center', verticalalignment='center', color=linecolor2)



# save and draw the figure
plt.savefig('images/pitch.png',dpi=300)
plt.show()


