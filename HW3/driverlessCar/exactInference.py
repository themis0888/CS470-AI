#20120888

'''
Licensing Information: Please do not distribute or publish solutions to this
project. You are free to use and extend Driverless Car for educational
purposes. The Driverless Car project was developed at Stanford, primarily by
Chris Piech (piech@cs.stanford.edu). It was inspired by the Pacman projects.
'''
from engine.const import Const
import util, math


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
				dist = self.getDist(agentY-util.rowToY(row), agentX-util.colToX(col))
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

	def getDist(self,x,y):
		return math.sqrt(x**2 + y**2)