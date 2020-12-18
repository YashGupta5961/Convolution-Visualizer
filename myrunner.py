from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy.ndimage.interpolation import shift

# Returns (2,2) list of axis limits
def getAxis(x, y): # x is the input (array of time values) y is a list containing [ft, ht, yt]  
    aft = [x[0], x[-1], min([min(y[0])*1.2,-1]), max(y[0])*1.2]
    aht = [x[0], x[-1], min([min(y[1])*1.2,-1]), max(y[1])*1.2]
    afthT = [x[0], x[-1], min(aft[2], aht[2]), max(aft[3], aht[3])]
    ayt = [x[0], x[-1], min([min(y[2])*1.2,-1]), max(y[2])*1.2]
    return [[aft, afthT],[aht,ayt]]

# Updates plot based on slider value
# z - slider value
# x - input (array of time values)
# y - list containing [ft, ht, yt]
# plots - list of subplots of visualizer
# hatus - list of flipped and shifted h(t)s
# axis - list of appropriate view windows
# labels - labels for subplots
def uVal(z, x, y, plot, htaus, axis, labels):
    lim = int((z - x[0])*100) # calculates index value corresponding to slider value

    # updates f(tau) and h(t-tau) plot
    plot[0,1].clear() # clears f(tau) and h(t-tau) plot
    plot[0,1].plot(x, y[0]) # replots f(tau)
    plot[0,1].plot(x, htaus[lim]) # plots h(t-tau) depending on previously calculated index value

    #updates y(t)
    temp = np.zeros(x.shape[0]) # initializes new y(t)
    temp[:lim] = y[2][:lim] # assigns values of y(t) from lower time limit to slider value
    plot[1,1].clear() # clears y(t) plot
    plot[1,1].plot(x, temp) # replots new y(t)

    # Makes plots look pretty
    for p in range(2):
        plot[p,1].axis(axis[p][1]) # adjusts view window 
        plot[p,1].set_title(labels[p][1]) # titles plots
        plot[p,1].grid(True, which = "both") # adds a grid
        plot[p,1].spines['left'].set_position('zero') # adds y axis
        plot[p,1].spines['bottom'].set_position('zero') # adds x axis

# Visualizer GUI
# x is the input (array of time values) 
# y is a list containing [ft, ht, yt]
# hatus is a list of flipped and shifted h(t)s
def draw(x, y, htaus): 
    fig, axs = plt.subplots(2, 2) #initializes 4 subplots
    fig.suptitle("Convoltuion Visualizer") #Title
    axis = getAxis(x, y) # gets appropriately scaled view windows for each subplot
    labels = [["f(t)", "f(Tau) and h(t-Tau)"],["h(t)", "y(t)"]] # initialized labels for each subplot
    axs[0,0].plot(x, y[0]) # plots f(t)
    axs[1,0].plot(x, y[1]) # plots h(t)
    axs[0,1].plot(x, y[0]) # initializes f(tau) and h(t-tau) by plotting f(tau)
    axs[1,1].plot(x, np.zeros(x.shape[0])) # initializes y(t) by plotting zeros

    # Makes plots look pretty
    for a in range(2):
        for b in range(2):
            axs[a,b].axis(axis[a][b])
            axs[a,b].set_title(labels[a][b])
            axs[a,b].grid(True, which = "both")
            axs[a,b].spines['left'].set_position('zero')
            axs[a,b].spines['bottom'].set_position('zero')

    # initializes slider
    sldr = Slider(plt.axes([0.125, 0.01, 0.775, 0.05]), "t", valmin=x[0]*0.9, valmax=x[-1]*0.9, valinit=x[0]*0.9)
    
    # helper function that calls uVal() using slider value
    updateVal = lambda z: uVal(z, x, y, axs, htaus, axis, labels)

    # gets updated slider value and calls updateVal()
    sldr.on_changed(updateVal)

    #Visualizes
    plt.show()

# convolutution
# inp - array of time values
# ft - array of values representing f(t)
# ht - array of values representing h(t)
def convolve(inp, ft, ht):
    tStart = inp[0] # gets start time
    tEnd = inp[-1] # gets end time
    count = len(inp) # gets number of time values
    resolution = (tEnd-tStart)/count # calculates resolution of input (time intervals)
    baseShift = int(tStart/resolution) # calculates first index of shift
    hTau = np.flipud(ht) # flips h(t)
    hTaus = np.tile(hTau, (count,1)) # copies flipped h(t) for all possible shifts
    res = np.zeros(hTau.shape[0]) # initializes y(t) with zeros
    for i in range(count): # iterates overs all possible shifts 
        hTaus[i] = shift(hTau, baseShift+i, cval=0) # updates array of flipped h(t)s by shifting appropriately 
        res[i] = np.trapz(np.multiply(ft, hTaus[i]), x=inp) # integrates h(t-tau)*f(tau) over input time interval
    return hTaus, res # returns shifted h(t-taus) and y(t) 

# Visualizes convolution of f(t) and h(t)
# inp - array of time values
# ft - array of values representing f(t)
# ht - array of values representing h(t)
def visualize(inp, ft, ht):
    hTaus, yt = convolve(inp, ft, ht) # gets shifted h(t-taus) and y(t)
    draw(inp, [ft, ht, yt], hTaus) # plots visualization


