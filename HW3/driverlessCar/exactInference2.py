#20120888
'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
from engine.const import Const
import util, math, random, collections


class ExactInference(object):
    

    def __init__(self, numRows, numCols):
        self.skipElapse = False ### ONLY USED BY GRADER.PY in case problem 3 has not been completed
        # util.Belief is a class (constructor) that represents the belief for a single
        # inference state of a single car (see util.py).
        self.belief = util.Belief(numRows, numCols)
        self.transProb = util.loadTransProb()
   
     
    ############################################################
    # Problem 2: 
    # Function: Observe (update the probablities based on an observation)
    # -----------------
    # Takes |self.belief| and updates it based on the distance observation
    # $d_t$ and your position $a_t$.
    #
    # - agentX: x location of your car (not the one you are tracking)
    # - agentY: y location of your car (not the one you are tracking)
    # - observedDist: true distance plus a mean-zero Gaussian with standard 
    #                 deviation Const.SONAR_STD
    # 
    # Notes:
    # - Convert row and col indices into locations using util.rowToY and util.colToX.
    # - util.pdf: computes the probability density function for a Gaussian
    # - Don't forget to normalize self.belief!
    ############################################################

    def observe(self, agentX, agentY, observedDist):
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        #raise Exception("Not implemented yet")
        # sum up the probability
        num_of_cols = self.belief.getNumCols()
        num_of_rows = self.belief.getNumRows()
        column = 0
        new_probs = []
        while column < num_of_cols:
            x = util.colToX(column)
            row = 0
            while row < num_of_rows:
                y = util.rowToY(row)
                prev_prob = self.belief.getProb(row,column)
                distSQ = (agentY - y)**2 + (agentX - x)**2
                accuracy = util.pdf(math.sqrt(distSQ),Const.SONAR_STD,observedDist)
                new_prob = (row,column,prev_prob * accuracy)
                new_probs.append(new_prob)
                row += 1
            column += 1
        for new_prob in new_probs:
            row,column,new_prob_val = new_prob
            self.belief.setProb(row,column,new_prob_val)
        self.belief.normalize()
        # END_YOUR_CODE


    def elapseTime(self):
        if self.skipElapse: return ### ONLY FOR THE GRADER TO USE IN Problem 2
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        #raise Exception("Not implemented yet")
        new_probs = []
        for key in self.transProb:
            transition_prob = self.transProb[key]
            if transition_prob == 0: continue
            oldTile,newTile = key[0],key[1]
            oldTile_x,oldTile_y = oldTile[0],oldTile[1]
            newTile_x,newTile_y = newTile[0],newTile[1]
            posterior_prob = self.belief.getProb(oldTile_x,oldTile_y)
            res_prob = posterior_prob * transition_prob
            new_prob = (newTile_x,newTile_y,res_prob)
            new_probs.append(new_prob)
        self.belief = util.Belief(self.belief.getNumRows(),self.belief.getNumCols(),0.0)
        for new_prob in new_probs:
            self.belief.addProb(new_prob[0],new_prob[1],new_prob[2])
        self.belief.normalize()
        # END_YOUR_CODE
      
    # Function: Get Belief
    # ---------------------
    # Returns your belief of the probability that the car is in each tile. Your
    # belief probabilities should sum to 1.    
    def getBelief(self):
        return self.belief

