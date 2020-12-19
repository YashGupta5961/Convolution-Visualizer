from matplotlib import pyplot as plt
import numpy as np
import myfunc
from myrunner import visualize

# Creates input time array
# lower - start time of visualization
# upper - end time of visualization
# resolution - time interval of input array
def initialize(lower, upper, resolution):
    count = int((upper - lower) / resolution) # gets number of time intervals
    return np.linspace(lower, upper, count) # returns equally spaced array of time intervals from lower to upper

# Creates array of values respresenting given function
# function - function for which values need to be calculated
# input - input array of time values
def calc(function, input):
    vcalc = np.vectorize(lambda t: function.getVal(t)) # creates vectorized function
    return vcalc(input) # returns array representing function

# Allows user to input custom functions
def createFunc(inp):
    print("Choose one of the following functions:")
    print("1. Unit Step")
    print("2. Rect")
    print("3. Triangle")
    print("4. Exponential")
    f = int(input("Base function: "))
    amp = float(input("Enter Amplitude: "))
    offset = float(input("Enter time shift: " ))
    
    #if exponential
    if(f == 4):
        tscale = float(input("Enter time scale: "))
        lBound = input("Enter lower bound. If unbounded press enter: ")
        uBound = input("Enter upper bound. If unbounded press enter: ")
        lBound = np.nan if(len(lBound) == 0) else float(lBound)
        uBound = np.nan if(len(uBound) == 0) else float(uBound)
        return calc(myfunc.Exp(amp, offset, tscale, lBound, uBound), inp)

    #if triangular
    elif(f == 3):
        width = float(input("Enter width: "))
        return calc(myfunc.Triangle(amp, offset, width), inp)
    
    #if rectangular
    elif(f == 2):
        width = float(input("Enter width: "))
        return calc(myfunc.Rect(amp, offset, width), inp)

    #if unit step
    elif(f == 1):
        return calc(myfunc.Step(amp, offset), inp)

    #error handling
    else:
        print("Function not listed. Please try again.")
        return np.zeros(inp.shape[0])
    
# Plots user inputed functions
# inp - array of time values
# ft - array of values representing f(t)
# ht - array of values representing h(t)
def check(inp, ft, ht):
    print("Here is what they look like!")
    fig, axs = plt.subplots(2)
    
    # plots f(t)
    axs[0].plot(inp, ft) #plots f(t)
    axs[0].axis([inp[0], inp[-1], min([min(ft)*1.2,-1]), max([max(ft)*1.2, 1])]) # sets appropriate view window
    axs[0].set_title("f(t)") # labels plot
    axs[0].grid(True, which = "both") # adds grid
    axs[0].spines['left'].set_position('zero') # adds y-axis
    axs[0].spines['bottom'].set_position('zero') # adds x-axis

    # plots h(t)
    axs[1].plot(inp, ht) #plots h(t)
    axs[1].axis([inp[0], inp[-1], min([min(ht)*1.2,-1]), max([max(ht)*1.2, 1])]) # sets appropriate view window
    axs[1].set_title("h(t)") # labels plot
    axs[1].grid(True, which = "both") # adds grid
    axs[1].spines['left'].set_position('zero') # adds y-axis
    axs[1].spines['bottom'].set_position('zero') # adds x-axis  

    plt.show() 

# Driver code
def main():
    print("Convolution Visualizer by Yash Gupta")
    tstart = float(input("Enter lower limit for the time axis: "))
    tend = float(input("Enter upper limit for the time axis: "))

    inp = initialize(tstart, tend, 0.01) # creates input array
    ft = np.zeros(inp.shape[0]) # intializes f(t) with zeros
    ht = np.zeros(inp.shape[0]) # intializes h(t) with zeros

    fCount = int(input("If f(t) is a composite function, how many functions would you like to superpose: "))
    hCount = int(input("If h(t) is a composite function, how many functions would you like to superpose: "))
    attempt = "n"
    # loops till user is satisfied with f(t) and h(t)
    while(attempt == "n"):
        ft = np.zeros(inp.shape[0]) # resets f(t)
        ht = np.zeros(inp.shape[0]) # resets h(t)

        # adds composite functions for f(t)
        for i in range(fCount):
            print(f"f{i}(t):")
            ft += createFunc(inp)

        # adds composite functions for h(t)
        for j in range(hCount):
            print(f"h{j}(t):")
            ht += createFunc(inp)

        # visualizes user inputed f(t) and h(t)
        check(inp, ft, ht)

        # checks if user is satisfied
        attempt = input("Satisfied with your f(t) and h(t)? (y or n): ")
    
    # runs visualizer
    visualize(inp, ft, ht)
    print("Thank you!")    

main()

# # ft = calc(myfunc.Rect(1,-2,2), inp)
# # ht = calc(myfunc.Rect(2,-1,2), inp)

# # ft = calc(myfunc.Exp(2, 0, -0.5, 0), inp)
# # ht = calc(myfunc.Rect(1,-1,2), inp)

# ft = calc(myfunc.Rect(1, 3, 2), inp) + calc(myfunc.Rect(-2, -3.5, 3), inp)
# ht = calc(myfunc.Rect(2, -1, 2), inp)
