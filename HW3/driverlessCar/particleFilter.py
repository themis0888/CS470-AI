#20120888

'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
from engine.const import Const
import util
import random
import math


# Class: Particle Filter
# ----------------------
# Maintain and update a belief distribution over the probability of a car
# being in a tile using a set of particles.
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
			dist = self.getDist(agentY-util.rowToY(row), agentX-util.colToX(col))
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

	def getDist(self,x,y):
		return math.sqrt(x**2 + y**2)

	def newBelief(self):
		row, col = self.belief.getNumRows(), self.belief.getNumCols()
		self.belief = util.Belief(row, col, 0)
		for tile in self.particles:
			prob = self.particles[tile]
			self.belief.grid[tile[0]][tile[1]] = prob
		self.belief.normalize()

	def spread(self):
		tprob = util.loadTransProb()
		for (old, new) in tprob:
			if old not in self.tprobDict:
				self.tprobDict.update({old : dict()})
			self.tprobDict[old][new] = tprob[(old, new)]
		
		n_particles = self.tprobDict.keys()
		for i in range(self.NUM_PARTICLES):
			ind = int(len(n_particles) * random.random())
			n_particles[ind]
			if n_particles[ind] not in self.particles:
				self.particles.update({n_particles[ind] : 0})
			else:
				self.particles[n_particles[ind]] += 1
			
		self.newBelief()
  