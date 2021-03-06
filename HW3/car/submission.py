'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
from engine.const import Const
import util, math, random, collections

# Class: ExactInference
# ---------------------
# Maintain and update a belief distribution over the probability of a car
# being in a tile using exact updates (correct, but slow times).
class ExactInference(object):
    
    # Function: Init
    # --------------
    # Constructer that initializes an ExactInference object which has
    # numRows x numCols number of tiles.
    def __init__(self, numRows, numCols):
        self.belief = util.Belief(numRows, numCols)

        ''' initialize any variables you will need later '''
   
    # Function: Observe
    # -----------------
    # Updates beliefs based on the distance observation and your agents position.
    # The noisyDistance is a gaussian distribution with mean of the true distance
    # and std = Const.SONAR_NOISE_STD.
    def observe(self, agentX, agentY, observedDist):
        prob_lst = []
        for col in range(self.belief.getNumCols()):
            for row in range(self.belief.getNumRows()):
                prev_prob = self.belief.getProb(row,col)
                dist = math.sqrt((agentY - util.rowToY(row))**2 + (agentX - util.colToX(col))**2)
                prob_lst.append((row,col,prev_prob * util.pdf(dist,Const.SONAR_STD,observedDist)))

        for i in range(len(prob_lst)):
            self.belief.setProb(prob_lst[i][0], prob_lst[i][1], prob_lst[i][2])
        self.belief.normalize()
        ''' your code here'''

    # Function: Elapse Time
    # ---------------------
    # Update your inference to handle the passing of one heartbeat. Use the
    # transition probability you created in Learner  
    def elapseTime(self):
        tprob = util.loadTransProb()
        prob_lst = []
        for key in tprob:
            if tprob[key] == 0: continue
            prob_lst.append((key[1][0],key[1][1],self.belief.getProb(key[0][0],key[0][1]) * tprob[key]))
        self.belief = util.Belief(self.belief.getNumRows(),self.belief.getNumCols(),0)
        for i in range(len(prob_lst)):
            self.belief.addProb(prob_lst[i][0], prob_lst[i][1], prob_lst[i][2])
        self.belief.normalize()
        ''' your code here'''
      
    # Function: Get Belief
    # ---------------------
    # Returns your belief of the probability that the car is in each tile. Your
    # belief probabilities should sum to 1.    
    def getBelief(self):
        return self.belief

  

class ParticleFilter(object):
    
    NUM_PARTICLES = 200
    
    # Function: Init
    # --------------
    # Constructer that initializes an ExactInference object which has
    # numRows x numCols number of tiles.
    def __init__(self, numRows, numCols):
        self.belief = util.Belief(numRows, numCols)
        self.tprobDict = {}
        self.particles = dict()
        self.spread()
        ''' initialize any variables you will need later '''
   
    # Function: Observe
    # -----------------
    # Updates beliefs based on the distance observation and your agents position.
    # The noisyDistance is a gaussian distribution with mean of the true distance
    # and std = Const.SONAR_NOISE_STD.
    def observe(self, agentX, agentY, observedDist):
        for key in self.particles:
            prev_prob = self.particles[key]
            row, col = key
            if self.particles[key] == 0: continue
            dist = math.sqrt((agentY-util.rowToY(row))**2 + (agentX-util.colToX(col))**2)
            self.particles[key] *= util.pdf(dist, Const.SONAR_STD, observedDist)
        n_particles = dict()

        for i in range(self.NUM_PARTICLES):
            key = util.weightedRandomChoice(self.particles)
            if key not in n_particles:
                n_particles.update({key : 0})
            else:
                n_particles[key] += 1
        self.particles = n_particles

        self.newBelief()
        ''' your code here'''

    # Function: Elapse Time
    # ---------------------
    # Update your inference to handle the passing of one heartbeat. Use the
    # transition probability you created in Learner  
    def elapseTime(self):

        n_particles = dict()
        for tile in self.particles:
            if self.particles[tile] == 0: continue
            for i in range(self.particles[tile]):
                indx = util.weightedRandomChoice(self.tprobDict[tile])
                if indx not in n_particles:
                    n_particles.update({indx : 0})
                else:
                    n_particles[indx] += 1
                    
        self.particles = n_particles
        ''' your code here'''
      
    # Function: Get Belief
    # ---------------------
    # Returns your belief of the probability that the car is in each tile. Your
    # belief probabilities should sum to 1.    
    def getBelief(self):
        return self.belief

    def newBelief(self):
        self.belief = util.Belief(self.belief.getNumRows(), self.belief.getNumCols(), 0)
        for tile in self.particles:
            prob = self.particles[tile]
            self.belief.grid[tile[0]][tile[1]] = prob
        self.belief.normalize()

    def spread(self):
        tprob = util.loadTransProb()
        for (oldTile, newTile) in tprob:
            if oldTile not in self.tprobDict:
                self.tprobDict.update({oldTile : dict()})
            self.tprobDict[oldTile][newTile] = tprob[(oldTile, newTile)]
            

        n_particles = self.tprobDict.keys()
        for i in range(self.NUM_PARTICLES):
            rand = random.random()
            ind = int(random.random() * len(n_particles))
            n_particles[ind]
            if n_particles[ind] not in self.particles:
                self.particles.update({n_particles[ind] : 0})
            else:
                self.particles[n_particles[ind]] += 1
            
        self.newBelief()
  