'''
File: Util
----------
This file contains several helper methods and a Belief class that you
can (and should) use to answer the various parts of the Driverless
Car assignment. Read each method description!

In addition to the Belief class, this file contains the
following helper methods:
 saveTransProb()
 loadTransProb()
 xToCol(x)
 yToRow(y)
 colToX(col)
 rowToY(row)
 pdf(mean, std, value)
 weightedRandomChoice(weightDict)
 
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''

from engine.const import Const
import cPickle as pickle
import math
import os.path
import random

# Function: Save Trans Prob
# -------------------------
# Saves the transition probabilities that have been generated by running
# "learner." The transDict can by a dictionary of any type that you design.
# For example it could be a dictionary of tuples that are associated with
# their own dictionaries.
def saveTransProb(transDict, transFile):
    pickle.dump(transDict, transFile)

# Function: Load Trans Prob
# -------------------------
# Loads the transition probabilities that have been generated by running
# "learner." 
def loadTransProb():
    transFileName = Const.WORLD + 'TransProb.p'
    transFilePath = os.path.join('learned', transFileName)
    with open(transFilePath) as transFile:
        return pickle.load(transFile)
    raise Exception('could not load ' + transFilePath + '. Did you run learner on this layout?')

# Function: X to Col
# -------------------------
# Returns the col in the discretized grid, that the value x falls into.
# This function does not check that x is in bounds.
# Warning! Do not confuse rows and columns!
def xToCol(x):
    return int((x / Const.BELIEF_TILE_SIZE))

# Function: Y to Row
# -------------------------
# Returns the row in the discretized grid, that the value y falls into.
# This function does not check that y is in bounds.
# Warning! Do not confuse rows and columns!
def yToRow(y):
    return int((y / Const.BELIEF_TILE_SIZE))

# Function: Row to y
# -------------------------
# Returns the y value of the center of a tile in row in the discretized grid.
# This function does not check that row is in bounds.
# Warning! Do not confuse x and y!
def rowToY(row):
    return (row + 0.5) * Const.BELIEF_TILE_SIZE

# Function: Col to x
# -------------------------
# Returns the x value of the center of a tile in col in the discretized grid.
# This function does not check that col is in bounds.
# Warning! Do not confuse x and y!
def colToX(col):
    return (col + 0.5) * Const.BELIEF_TILE_SIZE

# Function: Pdf
# -------------------------
# Returns the probability density of a Gaussian distribution with
# the specified mean and std, evaluated at the specified value.
def pdf(mean, std, value):
    u = float(value - mean) / abs(std)
    y = (1.0 / (math.sqrt(2 * math.pi) * abs(std))) * math.exp(-u * u / 2.0)
    return y

# Function: Weighted Random Choice
# --------------------------------
# Given a dictionary of the form element -> weight, selects an element
# randomly based on distribution proportional to the weights. Weights can sum
# up to be more than 1. 
def weightedRandomChoice(weightDict):
    weights = []
    elems = []
    for elem in weightDict:
        weights.append(weightDict[elem])
        elems.append(elem)
    total = sum(weights)
    key = random.uniform(0, total)
    runningTotal = 0.0
    chosenIndex = None
    for i in range(len(weights)):
        weight = weights[i]
        runningTotal += weight
        if runningTotal > key:
            chosenIndex = i
            return elems[chosenIndex]
    raise Exception('Should not reach here')

# Class: Belief
# ----------------
# This class represents the belief for a single inference state of a single 
# car. It has one belief value for every tile on the map. You *must* use
# this class to store your belief values. Not only will it break the 
# visualization and simulation control if you use your own, it will also
# break our autograder :).
class Belief(object):
    
    # Function: Init
    # --------------
    # Constructor for the Belief class. It creates a belief grid which is
    # numRows by numCols. As an optional third argument you can pass in a the
    # initial belief value for every tile (ie Belief(3, 4, 0.0) would create
    # a belief grid with dimensions (3, 4) where each tile has belief = 0.0.
    def __init__(self, numRows, numCols, value = None):
        self.numRows = numRows
        self.numCols = numCols
        numElems = numRows * numCols
        if value == None:
            value = (1.0 / numElems)
        self.grid = [[value for _ in range(numCols)] for _ in range(numRows)]
        
    # Function: Set Prob
    # ------------------
    # Sets the probability of a given row, col to be p
    def setProb(self, row, col, p):
        self.grid[row][col] = p
        
    # Function: Add Prob
    # ------------------
    # Increase the probability of row, col by delta. Belief probabilities are
    # allowed to increase past 1.0, but you must later normalize.
    def addProb(self, row, col, delta):
        self.grid[row][col] += delta
        assert self.grid[row][col] >= 0.0
        
    # Function: Get Prob
    # ------------------
    # Returns the belief for tile row, col.
    def getProb(self, row, col):
        return self.grid[row][col]
    
    # Function: Normalize
    # ------------------
    # Makes the sum over all beliefs 1.0 by dividing each tile by the total.
    def normalize(self):
        total = self.getSum()
        for r in range(self.numRows):
            for c in range(self.numCols):
                self.grid[r][c] /= total
    
    # Function: Get Num Rows
    # ------------------
    # Returns the number of rows in the belief grid.
    def getNumRows(self):
        return self.numRows
    
    # Function: Get Num Cols
    # ------------------
    # Returns the number of cols in the belief grid.
    def getNumCols(self):
        return self.numCols
    
    # Function: Get Sum
    # ------------------
    # Return the sum of all the values in the belief grid. Used to make sure
    # that the matrix has been normalized.
    def getSum(self):
        total = 0.0
        for r in range(self.numRows):
            for c in range(self.numCols):
                total += self.getProb(r, c)
        return total
