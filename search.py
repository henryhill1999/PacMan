import itertools
from Queue import PriorityQueue
from Edge import Edge
from Node import Node
from copy import copy, deepcopy

# implement basic manhattan distance heuristic
def heuristic(node, pManCrd, scene):
    minHorizontal = min(abs(node.crd[0]-pManCrd[0]), len(scene[0])-abs(node.crd[0]-pManCrd[0]))
    return minHorizontal + abs(node.crd[1]-pManCrd[1])

# implement heuristic search to find the 
    # quickest path between the ghost and pacman
def findOptimalPath(ghostCrd, pManCrd, scene):
    global graph 

    drc = isAdjacent(Node(pManCrd),Node(ghostCrd),scene)
    if drc:
        return [(Node(ghostCrd),drc),(Node(ghostCrd),None)]
    
    graph = generateStateGraph(ghostCrd, pManCrd, scene)
    
    frontier = PriorityQueue()
    
    # create start node
    start = graph[repr(Node(ghostCrd))]
    start.g = 0
    
    # create frontier
    frontier.put(start)
    
    # keep track of visited states and previous min cost with 
        # dictionary
    visited = {repr(start):start}
    
    while not frontier.empty():
        current_node = frontier.get()
        
        # if node has already been pruned, ignore
        if current_node.pruned:
            continue

        # check if node represents solution
        if current_node == Node(pManCrd):
            # reconstruct path using parent attribute
            path = []
            dest = current_node
            while dest.parent:
                path.append((dest.parent,[e.drc for e in dest.parent.edges if e.adjNode == dest][0]))
                dest = path[-1][0]
                
            return list(reversed(path))
        # expand node by generating child nodes from legal moves
        for edge in current_node.edges:
            c = edge.adjNode
            c.edges = graph[str(c)].edges
            if any(c == edge.adjNode for edge in graph[repr(Node(pManCrd))].edges):
                
                if c.crd[1] == pManCrd[1]:
                    minDist = min((abs(c.crd[0]-pManCrd[0]),'LEFT'),
                              (len(scene[0])-abs(c.crd[0]-pManCrd[0]),'RIGHT'))
                    
                else:
                    if c.crd[1] < pManCrd[1]:
                        minDist = (pManCrd[1]-c.crd[1],'DOWN')
                    
                    else:
                        minDist = (c.crd[1]-pManCrd[1],'UP')
                
                c.edges.add(Edge(graph[repr(Node(pManCrd))], *minDist))
                
            c.g = current_node.g+edge.weight
            c.h = heuristic(c, pManCrd,scene)

            c.f = c.g+c.h
            
            c.parent = current_node
            
            # ignore if visited or path is not more efficient
                # if path is more efficient, prune previous node
            if repr(c) in visited:
                if c.g >= visited[repr(c)].g:
                    continue
                else:
                    visited[repr(c)].pruned = True
            # add to visited nodes
            visited[repr(c)] = c
            
            # add to frontier
            frontier.put(c)
            
def generateStateGraph(ghostCrd, pManCrd, scene):
    # first identify points of intersection
    nodes = findIntersections(scene)
    
    nodes[repr(Node(ghostCrd))] = Node(ghostCrd)
    nodes[repr(Node(pManCrd))] = Node(pManCrd)

    for n in nodes:
        nodes[n].edges = findAdjacentNodes(nodes[n],nodes,scene)
    
    return nodes

def findAdjacentNodes(node, nodes, scene):
    xi = node.crd[0]
    yi = node.crd[1]
    
    w = len(scene[0])
    h = len(scene)
    
    adjacent = set()
    
    if yi % 1 == 0:
        yi = int(yi)
        
        xf = floor(xi + 1) % w
        while scene[yi][xf] and not repr(Node([xf, yi])) in nodes:
            xf = (xf + 1) % w
        if scene[yi][xf % w]:
            adjacent.add(Edge(Node([xf,yi]), abs(xf-node.crd[0]),'RIGHT'))
            
        xf = ceil(xi - 1) % w
        while scene[yi][xf] and not repr(Node([xf, yi])) in nodes:
            xf = (xf - 1) % w
            
        if scene[yi][xf]:
            adjacent.add(Edge(Node([xf,yi]), abs(xf-node.crd[0]),'LEFT'))

    if xi % 1 == 0:
        xi = int(xi)
        
        yf = floor(yi + 1) % h
        while scene[yf][xi] and not repr(Node([xi, yf])) in nodes:
            yf = (yf + 1) % h
            
        if scene[yf][xi]:
            adjacent.add(Edge(Node([xi,yf]), abs(yf-node.crd[1]),'DOWN'))
            
        yf = ceil(yi - 1) % h
        while scene[yf][xi] and not repr(Node([xi, yf])) in nodes:
            yf = (yf - 1) % h
            
        if scene[yf][xi]:
            adjacent.add(Edge(Node([xi,yf]), abs(yf-node.crd[1]),'UP'))
    return adjacent
    
def isAdjacent(a,b,scene):
    w = len(scene[0])
    h = len(scene)
    
    if a.crd[0] % 1 == 0 and a.crd[0] == b.crd[0]:
        
        yi = a.crd[1]
        yf = b.crd[1]
        
        step = 1 if yi < yf else -1
        
        for i in range(floor(yi),ceil(yf),step):
            if not scene[floor(i) if step > 0 else ceil(i)][int(a.crd[0])]:
                return False
                
        return 'UP' if step > 0 else 'DOWN'
        
    elif a.crd[1] % 1 == 0 and a.crd[1] == b.crd[1]:  
        xi = a.crd[0]
        xf = b.crd[0]
        if abs(xf-xi) <= w/2:
            
            step = 1 if xi < xf else -1
            
            for i in range(floor(xi),ceil(xf),step):
                if not scene[int(a.crd[1])][floor(i) if step > 0 else ceil(i)]:
                    return False
            return 'LEFT' if step > 0 else 'RIGHT'
        else:
            step = -1 if xi < xf else 1
            for i in range(floor(xi),step*w+ceil(xf),step):
                if not scene[int(a.crd[1])][floor(i)%w if step > 0 else ceil(i)%w]:
                    return False
                
            return 'LEFT' if step > 0 else 'RIGHT'
            
        
    return False
        
    
#return coordinates for every point which is an intersection
    # intersection is defined as being a path block which is
    # adjacent to at least on pair of path blocks which are 
    # not opposite each other
    # i.e. reaching this block gives one the option to turn
def findIntersections(scene):
    w = len(scene[0])
    h = len(scene)

    return {repr(crd):Node(crd) for crd in 
        filter(lambda crd : isIntersection(scene,crd),
               (list(x) for x in itertools.product(range(w),range(h))))}

def isIntersection(scene, coord):
    x,y = coord
    if not scene[y][x]:
        return False
    
    w = len(scene[0])
    h = len(scene)
    adjacent = [scene[(y+1) % h][x % w],
                scene[y % h][(x+1) % w],
                scene[(y-1) % h][x % w],
                scene[y % h][(x-1) % w]]
    

    return any(adjacent[i] and adjacent[(i+1)%4] for i in range(4))
