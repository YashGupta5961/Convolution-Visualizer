import numpy as np

class Step():
    def __init__(self, amp = 1, offset = 0):
        self.amplitude = amp
        self.offset = -1*offset

    def getVal(self, t):
        return self.amplitude if (t >= self.offset) else 0.0

class Rect():
    def __init__(self, amp = 1, offset = 0, width = 1):
        self.amplitude = amp
        self.offset = -1*offset
        self.lower = self.offset - (width/2)
        self.upper = self.offset + (width/2)

    def getVal(self, t):
        return self.amplitude if (t >= self.lower and t < self.upper) else 0.0

class Triangle():
    def __init__(self, amp = 1, offset = 0, width = 1):
        self.amplitude = amp
        self.offset = -1*offset
        self.lower = self.offset - (width/2)
        self.upper = self.offset + (width/2)
        self.slope = 2*amp / width

    def getVal(self, t):
        if (self.lower <= t and t < self.offset):
            return self.slope*(t - self.lower)
        elif (self.offset <= t and t < self.upper):
            return -1*self.slope*(t - self.offset) + self.amplitude
        else:
            return 0.0

class Exp():
    def __init__(self, amp = 1, offset = 0, timeScale = 1, lower = np.nan, upper = np.nan):
        self.amplitude = amp
        self.offset = -1*offset
        self.ts = timeScale
        self.lower = lower
        self.upper = upper
        
    def getVal(self, t):    
        if self.lower != np.nan and t < self.lower:
            return 0.0

        if self.upper != np.nan and t >= self.upper:
            return 0.0
   
        return self.amplitude*np.exp([self.ts * (t - self.offset)])[0]
