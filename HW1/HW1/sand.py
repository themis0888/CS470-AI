
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
		print(bfs_path(bfs_list, path[i], path[i+1])[1:])
	return fin_path


def aStar(start, goal, maps):

    path = util.Stack()

    "*** YOUR CODE HERE ***"
    closedSet = set()
    openSet = {start}
    
    start.G = 0
    start.F = manhattanDistance(start.position, goal.position)

    while openSet:
        keylst = []
        for i in openSet:
            keylst.append(i.G+i.H)
        key = min(keylst)
        for i in openSet:
            if i.G + i.H == key:
                current = i

        if current == goal:
            break
        openSet.remove(current)
        closedSet.add(current)
        
        for neighbor in getChildren(current, maps):
            if neighbor in closedSet: 
                continue

            if not neighbor in openSet: 
                openSet.add(neighbor)

            tentative_gScore = current.G + 1
            if tentative_gScore > neighbor.G:
                continue 

            neighbor.parent = current
            neighbor.G = tentative_gScore
            neighbor.F = neighbor.G + manhattanDistance(neighbor.position, goal.position)

    pointer = goal
    while pointer != start:
        path.push(pointer)
        pointer = pointer.parent
    path.push(start)

    return path

graph = {'A': set(['B', 'C']),
		 'B': set(['A', 'D', 'E']),
		 'C': set(['A', 'F']),
		 'D': set(['B']),
		 'E': set(['B', 'F']),
		 'F': set(['C', 'E'])}

graph2 = {'A': ['B', 'C'],
		 'B': ['A', 'D', 'E'],
		 'C': ['A', 'F'],
		 'D': ['B'],
		 'E': ['B', 'F'],
		 'F': ['C', 'E']}


AA = bfs(graph, 'A')


t_mat = 'TTTTTT\nTTTFFT\nTTFFFT\nTFFTTT\nTTTTTT'
print(t_mat)
tt = map_process(t_mat)
t = p_bfs(tt, (3,3))

print(bfs_traversal(tt, (3,3)))
f = open('pac_world.txt',"r")
line = f.read()
ttt = map_process(line)
fin_path = bfs_traversal(ttt, (9,1))
print(p_bfs(ttt,(9,1)))