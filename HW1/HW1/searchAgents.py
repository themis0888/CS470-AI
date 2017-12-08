
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
    print(state.getPacmanPosition())
    legal = state.getLegalPacmanActions()   #list of legal direction
    current = state.getPacmanState().configuration.direction    #where you're heading
    if current == Directions.STOP: current = Directions.NORTH   #when you're licking the wall, look north
    left = Directions.LEFT[current]
    if left in legal: return left
    if current in legal: return current
    if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
    if Directions.LEFT[left] in legal: return Directions.LEFT[left]
    
    return Directions.STOP

class RightTurnAgent(Agent):
  "An agent that turns right at every opportunity"
  
  def getAction(self, state):
    legal = state.getLegalPacmanActions()
    current = state.getPacmanState().configuration.direction
    if current == Directions.STOP: current = Directions.NORTH
    right = Directions.RIGHT[current]
    if right in legal: return right
    if current in legal: return current
    
    if Directions.LEFT[current] in legal: return Directions.LEFT[current]
    if Directions.RIGHT[right] in legal: return Directions.RIGHT[right]
    return Directions.STOP

class GreedyAgent(Agent):
  def __init__(self, evalFn="scoreEvaluation"):
    self.evaluationFunction = util.lookup(evalFn, globals())
    assert self.evaluationFunction != None
        
  def getAction(self, state):
    # Generate candidate actions
    legal = state.getLegalPacmanActions()
    if Directions.STOP in legal: legal.remove(Directions.STOP)
      
    successors = [(state.generateSuccessor(0, action), action) for action in legal] 
    scored = [(self.evaluationFunction(state), action) for state, action in successors]
    bestScore = max(scored)[0]
    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    return random.choice(bestActions)


#T_Node class
class T_Node:
  def __init__(self, data = -1, parent = 'root'):
    self.data = data
    self.children = []
    self.parent = parent

  def add_child(self, obj):
    self.children.append(obj)
    obj.parent = self
  def preorder(self, adj_list = {}):
    
    if self.data not in adj_list:
      adj_list[self.data] = []
    
    for i in range(len(self.children)):
      adj_list[self.data].append(self.children[i].data)
      self.children[i].preorder(adj_list)
      if self.children[i].data not in adj_list:
        adj_list[self.data] = []
      adj_list[self.children[i].data].append(self.data)
    return adj_list




#make T_Node list from graph (without making parent or sorting)
#dictionary -> list of T_Node
def g_process(graph):
  g_list = {}
  for i in graph:
    g_list[i] = T_Node(i)
  
  return g_list



# Read the wall data like TTTTFFFTTT and make adj_list
# text -> dictionary
def map_process(wall_text):

  map_matrix = wall_text.split('\n')
  cnt = 0
  adj_list = {}
  y_size = len(map_matrix) 
  if len(map_matrix[y_size-1]) != len(map_matrix[0]):
    map_matrix = map_matrix[:y_size-1]
    y_size -= 1
  y_size -= 1
  for i in range(1, y_size):
    for j in range(1, len(map_matrix[0])-1):
      if map_matrix[i][j] == 'F':

        cnt = 0
        adj_list[(j,y_size-i)] = set()
        if map_matrix[i-1][j] == 'F':
          adj_list[(j,y_size-i)].add((j,y_size-i+1))
          cnt += 1
        if map_matrix[i+1][j] == 'F':
          adj_list[(j,y_size-i)].add((j,y_size-i-1))
          cnt += 1
        if map_matrix[i][j-1] == 'F':
          adj_list[(j,y_size-i)].add((j-1,y_size-i))
          cnt += 1
        if map_matrix[i][j+1] == 'F': 
          adj_list[(j,y_size-i)].add((j+1,y_size-i))
          cnt += 1

  return adj_list



# Do the BFS search and make BFS tree. 
# dictionary, key -> Tree
def bfs(graph, start):
  visited, queue, entry = [], [start], set(graph)
  g = g_process(graph)
  BFSTree = g[start]
  while queue:
    vertex = queue.pop(0)
    if vertex not in visited:

      visited.append(vertex)
      temp_list = list(graph[vertex] - set(visited))
      queue.extend(temp_list)
      
      if temp_list != []:
        for i in temp_list:
          g[vertex].add_child(g[i])
          print('add children' + str(temp_list))

  return BFSTree


# Do the BFS search FOR PACMAN and make BFS tree. 
# dictionary, key -> Tree, list
def p_bfs(graph, start):
  visited, queue, entry = [], [start], set(graph)
  g = g_process(graph)
  BFSTree = g[start]
  while queue:
    vertex = queue.pop(0)
    if vertex not in visited:

      visited.append(vertex)
      temp_list = list(graph[vertex] - set(visited) - set(queue))

      #East West South North

      if (vertex[0]+1, vertex[1]) in temp_list:
        queue.append((vertex[0]+1, vertex[1]))
      if (vertex[0]-1, vertex[1]) in temp_list:
        queue.append((vertex[0]-1, vertex[1]))
      if (vertex[0], vertex[1]-1) in temp_list:
        queue.append((vertex[0], vertex[1]-1))
      if (vertex[0], vertex[1]+1) in temp_list:
        queue.append((vertex[0], vertex[1]+1))
      
      if temp_list != []:
        for i in temp_list:
          g[vertex].add_child(g[i])

  return BFSTree, visited


# dictionary, key, key -> list(the shortest path)
def bfs_path(graph, start, goal):
  queue = [(start, [start])]
  while queue:
    (vertex, path) = queue.pop(0)
    for next in graph[vertex]:
      if next not in path:
        if next == goal:
          return path + [next]
        else:
          queue.append((next, path + [next]))



# dictionary, key -> list list list...
# stupid bfs pacman moving 
def bfs_traversal(graph, start):
  fin_path = [start]
  Tree, path = p_bfs(graph,start)
  bfs_list = Tree.preorder()
  for i in range(len(path)-1):
    fin_path.extend(bfs_path(bfs_list, path[i], path[i+1])[1:])
  return fin_path

class BFSAgent(Agent):
  """
    Your BFS agent (question 1)
  """
  def __init__(self):
    self.counter = -1
    self.d_counter = 1
    self.path = []
    self.dest = []
    self.start = (0, 0)

  
  def preprocess(self, gameState):
    line = str(gameState.getWalls())
    ttt = map_process(line)
    start = gameState.getPacmanPosition()
    fin_path = bfs_traversal(ttt, start)
    dest_lst = p_bfs(ttt, start)[1]
    self.start = start
    for i in range(len(dest_lst)):
      dest_lst[i] = (dest_lst[i][0] - start[0], dest_lst[i][1] - start[1])
    return fin_path, dest_lst
  

    
  def getAction(self, gameState):

    "*** YOUR CODE HERE ***"
    #if counter == -1:
    """
    do Preprocessing here
    1 Make Search Tree: BFS -> searchtree
    2 Convert relative coordinates
    3 print result.txt
    4 build finalActions list
    counter += 1
    """
    #At the very first turn, just read the map and do preprocess
    Direction = Directions.STOP
    if self.counter == -1:
      self.path, self.dest = self.preprocess(gameState)
      self.counter += 1

    #And then, do the search
    else:
      current = gameState.getPacmanPosition()
      f = open('result.txt', 'w')

      for i in range(self.d_counter+1):
        f.write(str(self.dest[i])+'\n')

      if self.path[self.counter+1][0] - self.path[self.counter][0] == 1:
        Direction = Directions.EAST
      elif self.path[self.counter+1][0] - self.path[self.counter][0] == -1:
        Direction = Directions.WEST
      elif self.path[self.counter+1][1] - self.path[self.counter][1] == 1:
        Direction = Directions.NORTH
      elif self.path[self.counter+1][1] - self.path[self.counter][1] == -1:
        Direction = Directions.SOUTH
      self.counter += 1   #every time when you move, increase the counter
      
      #When you find a new node, increase d_counter so let the program write the new node on the file
      if str((current[0]-self.start[0], current[1]-self.start[1])) == str(self.dest[self.d_counter]):
        self.d_counter += 1

    
    return Direction

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
    It is different from raw and column of matrix.

    """
    def __init__(self, value, position):
        self.value = value
        self.position = position
        self.parent = None
        self.H = float('inf')
        self.G = float('inf')
        self.F = float('inf')
        self.is_this_working = 'Yep'

    def move_cost(self):
        return 1

def getChildren(position, maps):
    """
    Return the children that can move legally

    """
    x, y = position.position
    links = [maps[len(maps)-1 - d[1]][d[0]] for d in [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]]
    return [link for link in links if link.value != True]


# Node, Node, maps -> stack(path)
# Do astar search. You can understand this code with reading wikipedia
def aStar(start, goal, maps):

    c_Set = set()
    o_Set = set()

    o_Set.add(start)

    cameFrom = maps

    start.G = 0
    start.H = manhattanDistance(start.position, goal.position)

    while o_Set:

        key = float('inf')

        for i in o_Set:
            if (i.G+i.H) < key:
                current = i
                key = (i.G+i.H)

        if current == goal:
            return make_path(start, goal)

        o_Set.remove(current)
        c_Set.add(current)
        
        for neighbor in getChildren(current, cameFrom):
            if neighbor in c_Set: 
                continue

            if not neighbor in o_Set: 
                o_Set.add(neighbor)

            t_G = current.G + abs(current.position[0] + 
                current.position[1] - neighbor.position[0] - neighbor.position[1])
            if t_G >= neighbor.G:
                continue 

            neighbor.parent, neighbor.G = current, t_G
            neighbor.H = neighbor.G + manhattanDistance(neighbor.position, goal.position)

    return False


# Node, Node -> stack(path)
# Just path making function.
def make_path(start, goal):
    path = util.Stack()
    index = goal
    lst = []
    while index != start:
        lst.append(index)
        index = index.parent
    for i in range(len(lst)):
        path.push(lst[i])

    path.push(start)
    
    return path

