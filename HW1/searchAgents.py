# searchAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

##this is example agents
class LeftTurnAgent(Agent):
  "An agent that turns left at every opportunity"

  def getAction(self, state):
    pos = state.getPacmanPosition()
    print(pos)
    legal = state.getLegalPacmanActions()
    current = state.getPacmanState().configuration.direction
    if current == Directions.STOP: current = Directions.NORTH
    left = Directions.LEFT[current]
    if left in legal: return left
    if current in legal: return current
    if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
    if Directions.LEFT[left] in legal: return Directions.LEFT[left]
    return Directions.STOP

class GreedyAgent(Agent):
  def __init__(self, evalFn="scoreEvaluation"):
    self.evaluationFunction = util.lookup(evalFn, globals())
    assert self.evaluationFunction != None

  def getAction(self, state):
    pos = state.getPacmanPosition()
    print(pos)
    # Generate candidate actions
    legal = state.getLegalPacmanActions()
    if Directions.STOP in legal: legal.remove(Directions.STOP)

    successors = [(state.generateSuccessor(0, action), action) for action in legal]
    scored = [(self.evaluationFunction(state), action) for state, action in successors]
    bestScore = max(scored)[0]
    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    return random.choice(bestActions)

class BFSAgent(Agent):
  """
    Your BFS agent (question 1)
  """
  def __init__(self):
      self.turnCounter = -1
      self.initialPosition = (0,0)
      self.searchTree = []
      self.parentinfo = dict()
      self.solutionTable = dict()
      self.actualMovePath = []
      self.actualActions = []

  def getAction(self, gameState):

    """
      Returns the BFS searching action using gamestate.getLegalActions()

      legal moves can be accessed like below
      legalMoves = gameState.getLegalActions()
      this method returns current legal moves that pac-man can have in curruent state
      returned results are list, combination of "North","South","West","East","Stop"
      we will not use stop action for this project

      Please write code that Pacman traverse map in BFS order.
      Because Pac-man does not have any information of map, it should move around in order to get
      information that is needed to reach to the goal.

      Also please print order of x,y cordinate of location that Pac-man first visit in result.txt file with format
      (x,y)
      (x1,y1)
      (x2,y2)
      .
      .
      .
      (xn,yn)
      note that position that Pac-man starts is considered to be (0,0)

      this method is called until Pac-man reaches to goal
      return value should be one of the direction Pac-man can move ('North','South'....)
    """
    "*** YOUR CODE HERE ***"
    if self.turnCounter == -1:
        self.initialPosition = gameState.getPacmanPosition()
        goal = self.BFS(gameState, self.initialPosition)
        actualmovepath = self.buildActualMovePath()
        actualmovepath = self.makeRelative(actualmovepath)
        self.buildSolutionTable(actualmovepath)
        self.searchTree = self.makeRelative(self.searchTree)

        with open("result.txt", "w") as f:
            for node in self.searchTree:
                f.write(str(node))
                f.write("\n")

        self.turnCounter += 1

    action = self.actualActions[self.turnCounter]
    self.turnCounter += 1
    return action

  def BFS(self, gameState, initial):
    walls = gameState.getWalls()
    foods = gameState.getFood()
    S = set()
    Q = util.Queue()
    S.add(initial)
    Q.push(initial)
    while not Q.isEmpty == True:
        current = Q.pop()
        self.searchTree.append(current)
        x = current[0]
        y = current[1]
        if foods[x][y] == True: # current loc has food
            #print("Found the food!")
            #print(current)
            return current
        for n in self.Adjacent(current, gameState):
            n_x = n[0]
            n_y = n[1]
            if walls[n_x][n_y] == False:
                if not n in S:
                    self.parentinfo[n] = current
                    S.add(n)
                    Q.push(n)

  def Adjacent(self, pos, gameState):
    """
    Gets a position and returns available adjacent grids
    where there are no walls.
    """
    walls = gameState.getWalls()
    foods = gameState.getFood()
    Width = walls.width
    Height = walls.height
    x = pos[0]
    y = pos[1]
    neighbors = []
    if x == Width - 1 and y == Height - 1: # right top
        neighbors.append((x-1,y))
        neighbors.append((x,y-1))
    elif x == Width -1 and y == 0: # right bottom
        neighbors.append((x-1,y))
        neighbors.append((x,y+1))
    elif x == Width -1: # right side
        neighbors.append((x-1,y))
        neighbors.append((x,y-1))
        neighbors.append((x,y+1))
    elif x == 0 and y == Height - 1: # left top
        neighbors.append((x+1,y))
        neighbors.append((x,y-1))
    elif x == 0 and y == 0: # left bottom
        neighbors.append((x+1,y))
        neighbors.append((x,y+1))
    elif x == 0: # left side
        neighbors.append((x+1,y))
        neighbors.append((x,y-1))
        neighbors.append((x,y+1))
    elif y == Height -1: # top side
        neighbors.append((x+1,y))
        neighbors.append((x-1,y))
        neighbors.append((x,y-1))
    elif y == 0: # bottom side
        neighbors.append((x+1,y))
        neighbors.append((x-1,y))
        neighbors.append((x,y+1))
    else: # in the middle
        neighbors.append((x+1,y))
        neighbors.append((x-1,y))
        neighbors.append((x,y-1))
        neighbors.append((x,y+1))
    return neighbors

  def addTuple(self, A, B):
      Ax = A[0]
      Ay = A[1]
      Bx = B[0]
      By = B[1]
      return (Ax+Bx,Ay+By)

  def substractTuple(self, B, A):
      Bx = B[0]
      By = B[1]
      Ax = A[0]
      Ay = A[1]
      return (Bx-Ax,By-Ay)

  def calculateAction(self, state2, state1):
      """Calculate the action to take to go from state1 to state2"""
      diff = self.substractTuple(state2, state1)
      x = diff[0]
      y = diff[1]
      if x > 0 and y == 0:
          return Directions.EAST
      elif x < 0 and y == 0:
          return Directions.WEST
      elif x == 0 and y < 0:
          return Directions.SOUTH
      elif x == 0 and y > 0:
          return Directions.NORTH

  def makeRelative(self, listOfPosition):
      """
        Convert grid coordinate to relative coordinate with (0,0)
        as Pacman's starting point
      """
      rel_path = []
      for pos in listOfPosition:
          rel_path.append(self.substractTuple(pos, self.initialPosition))
      return rel_path

  def buildSolutionTable(self, rel_path):
      """
      Builds solution table. It contains the actions to take to go through the solution path.
      It also fills up the self.actualActions list, which will be used by Pacman agent.
      """
      for i in range(len(rel_path)):
          if i == len(rel_path) - 1:
              self.solutionTable[rel_path[i]] = Directions.STOP
              self.actualActions.append(Directions.STOP)
          else:
              action = self.calculateAction(rel_path[i+1],rel_path[i])
              self.solutionTable[rel_path[i]] = action
              self.actualActions.append(action)
              #print(rel_path[i])
              #print(action)

  def getParentChain(self, node):
      """In the searchTree, get all parent of node in list"""
      parentChain = []
      current = node
      parentChain.append(current)
      while not current == self.initialPosition:
          parent = self.parentinfo[current]
          parentChain.append(parent)
          current = parent
      return parentChain

  def moveThroughSearchTree(self, nodeA, nodeB):
      """In the searchTree, find the path for moving from nodeA to nodeB"""
      path = []
      shorterChain = []
      longerChain = []
      nearestCommonParent = tuple()
      parentChainA = self.getParentChain(nodeA)
      parentChainB = self.getParentChain(nodeB)
      if len(parentChainA) <= len(parentChainB):
          shorterChain = parentChainA
          longerChain = parentChainB
      else:
          shorterChain = parentChainB
          longerChain = parentChainA
      for node1 in shorterChain:
          for node2 in longerChain:
              if node2 == node1:
                  nearestCommonParent = node1
                  break
          else:
              continue
          break
      parentChainA = parentChainA[:parentChainA.index(nearestCommonParent)+1]
      parentChainB = parentChainB[:parentChainB.index(nearestCommonParent)]
      parentChainB.reverse()
      path = parentChainA + parentChainB
      return path

  def buildActualMovePath(self):
      searchTree = self.searchTree
      actualMovePath = []
      if len(searchTree) == 1:
          return searchTree
      else:
          for i in range(len(searchTree)):
              if i == len(searchTree)-1:
                  movepath = searchTree[i]
                  actualMovePath.append(movepath)
              else:
                  movepath = self.moveThroughSearchTree(searchTree[i],searchTree[i+1])
                  actualMovePath += movepath[:-1]
      return actualMovePath

class AstarAgent(Agent):
  """
    Your astar agent (question 2)

    An astar agent chooses actions via an a* function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.

  """
  def __init__(self):
    self.path = None
    self.isCallAstar = False

  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses the best movement according to the a* function.

    The return value of a* function is paths made up of Stack. The top
    is the starting point, and the bottom is goal point.

    """

    if self.isCallAstar is False:
        layout = gameState.getWalls()

        # print(layout)

        maps = [[0 for col in range(layout.width)] for row in range(layout.height)]

        for raw in range(layout.height):
            for col in range(layout.width):
                maps[raw][col] = Node(layout[col][layout.height-1 - raw], (col, layout.height-1 - raw))

        # the position of pac-man
        start = gameState.getPacmanPosition()

        # the position of food
        goal = gameState.getFood().asList()[0]

        # print(grid[layout.height-1 - start[1]][start[0]].position)
        # print(grid[layout.height-1 - goal[1]][goal[0]].position)

        self.path = aStar(maps[layout.height-1 - start[1]][start[0]], maps[layout.height-1 - goal[1]][goal[0]], maps)

        self.isCallAstar = True

    if len(self.path.list) < 2:
        self.isCallAstar = False
        return 'Stop'
    else:
        move = self.whatMove(self.path)
        self.path.pop()

    "Add more of your code here if you want to"

    return move

  def whatMove(self, path):
    current = path.pop()
    next = path.pop()
    path.push(next)
    path.push(current)

    if(current.position[0] == next.position[0]):
        if current.position[1] < next.position[1]: return 'North'
        else: return 'South'
    else:
        if current.position[0] < next.position[0]: return 'East'
        else: return 'West'

class Node:
    """
    The value is presence of wall, so it is True or False.
    The parent is previous position. The point is the position of Node.
    It is different from row and column of matrix.

    """
    def __init__(self, value, position):
        self.value = value
        self.position = position
        self.parent = None
        self.H = float("inf")
        self.G = float("inf")

    def move_cost(self):
        return 1

def getChildren(position, maps):
    """
    Return the children that can move legally

    """
    x, y = position.position
    links = [maps[len(maps)-1 - d[1]][d[0]] for d in [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]]
    return [link for link in links if link.value != True]

def aStar(start, goal, maps):
    """
    The a* function consists of three parameters. The first is the starting
    point of pac-man, the second is the point of food, the last is the presence
    of wall in the map. The map consists of nodes.

    Return the coordinates on the Stack where top is the starting point and bottom is
    the goal point.

    For example, if the starting point is (9, 1) and the goal point is (1, 8), you
    return the path like this.


    (9, 1) <- top
    (8, 1)

    ...

    (1, 7)
    (1, 8) <- bottom
    """
    path = util.Stack()

    "*** YOUR CODE HERE ***"
    closedSet = set() # The set of nodes already evaluated
    openSet = set() # The set of currently discovered nodes that are not evaluated yet.
    openSet.add(start)
    print(start)
    start.G = 0
    start.H = manhattanDistance(start.position, goal.position)

    while not len(openSet) == 0:
        #print("---------Nahaha---------")
        #for n in closedSet:
        #    print(n.parent)
        current = extractMin(openSet) # Here I have to make!!!!
        if current == goal:
            break
        openSet.remove(current)
        closedSet.add(current)
        neighbors = getChildren(current, maps)
        for neighbor in neighbors:
            if neighbor in closedSet: # Ignore the one already evaluated
                continue
            if not neighbor in openSet: # Discover a new node
                openSet.add(neighbor)

            tentative_gScore = current.G + 1
            if tentative_gScore > neighbor.G:
                continue # This is not a better path

            # This path is the best until now. Record it!
            neighbor.parent = current
            neighbor.gScore = tentative_gScore
            neighbor.fScore = neighbor.gScore + manhattanDistance(neighbor.position, goal.position)

    pointer = goal
    while not pointer == start:
        path.push(pointer)
        pointer = pointer.parent
    path.push(start)
    return path

def extractMin(set):
    """
    Extract an object with the minimum key in a set
    The set must be a set of Node
    """
    keyset = []
    result = None
    for e in set:
        keyset.append(e.G+e.H)
    key = min(keyset)
    for e in set:
        if e.G+e.H == key:
            return e
