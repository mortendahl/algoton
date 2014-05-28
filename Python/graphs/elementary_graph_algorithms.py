

class Graph:
    
    def __init__(self, graph=dict()):
        self._graph = graph

    def nodes(self):
        return self._graph.keys()
    
    def has_node(self, node):
        return self._graph.has_key(node)
        
    def neighbours(self, node):
        return self._graph.get(node, [])



#
# simple test graph: cyclic, unconnected
#
testgraph = Graph( {    0: [ 0, 1, 2, 3 ],
                        1: [ 1, 2, 4 ],
                        2: [ 1, 5 ],
                        3: [],
                        4: [],
                        5: [],
                        6: [ 7 ],
                        7: []         })








#
# from http://www.python.org/doc/essays/graphs.html
#
# input:
#  - graph: directed, may be cyclic (dict+list representation)
#  - start: root node to search from
#  - end:   target node to search for
#
# output:
#  - path:  an acyclic path (as list) or 'None' if no path exists
#
# notes:
#  - performs a depth-first search
#  - uses recursive calls
#  - an excessive amount of work is performed since it re-computes
#    everything for each adjacent node
#
def dfs_ss_any_pythondocs(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_node(start):
        return None
    for node in graph.neighbours(start):
        if node in path: continue
        newpath = dfs_ss_any_pythondocs(graph, node, end, path)
        if newpath:
            return newpath
    return None


#
# from http://www.python.org/doc/essays/graphs.html
#
# input:
#  - graph: directed, may be cyclic (dict+list representation)
#  - start: root node to search from
#  - end:   target node to search for
#
# output:
#  - paths: all acyclic paths (as list of lists)
#
# notes:
#  - performs a depth-first search
#  - uses recursive calls
#  - an excessive amount of work is performed since it re-computes
#    everything for each adjacent node
#  - a lot of copying takes place after each recursive call
#
def dfs_ss_all_pythondocs(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_node(start):
        return []
    paths = []
    for node in graph.neighbours(start):
        if node in path: continue
        newpaths = dfs_ss_all_pythondocs(graph, node, end, path)
        for newpath in newpaths:
            paths.append(newpath)
    return paths


#
# from http://www.python.org/doc/essays/graphs.html
#
# input:
#  - graph: directed, may be cyclic (dict+list representation)
#  - start: root node to search from
#  - end:   target node to search for
#
# output:
#  - path:  a shortest acyclic path (as list)
#
# notes:
#  - performs a depth-first search
#  - uses recursive calls
#  - an excessive amount of work is performed since it re-computes
#    everything for each adjacent node
#
def dfs_ss_shortest_pythondocs(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_node(start):
        return None
    shortest = None
    for node in graph.neighbours(start):
        if node in path: continue
        newpath = dfs_ss_shortest_pythondocs(graph, node, end, path)
        if newpath:
            if not shortest or len(newpath) < len(shortest):
                shortest = newpath
    return shortest











#
# input:
#  - parent: parent dictionary for all nodes
#  - start:  start node in path
#  - end:    end node in path
#
# output:
#  - path:   a path from 'start' to 'end' (as list) if it exists in parent (NOT graph)
#
# notes:
#  - see http://stackoverflow.com/questions/3705670/best-way-to-create-a-reversed-list-in-python
#
def path_from(parent, start, end):
    if not parent.has_key(end): return None
    path = [end]
    # add parents (in reverse order) by backtracking    
    node = end
    while parent[node] != None and node != start:
        node = parent[node]
        path.append(node)
    # if a 'start' has given but we didn't end up at it, it's because there's no path
    if start != None and node != start: return None
    return path[::-1]
    #return (path[::-1] if (not start) or (node == start) else None)


#
# input:
#  - parent: parent dictionary for all nodes
#  - end:    end node in path
#
# output:
#  - path:   a path from root to 'end' (as list)
#  
def path_from_root(parent, end):
    return path_from(parent, None, end)






#
# inspired by Cormen etc.
#  - untimed variant
#
# input:
#  - graph:    directed, may be cyclic (dict+list representation)
#  - start:    root node to search from
#
# output:
#  - parent:   parent relationship to 'start' for all nodes in graph
#
# notes:
#  - performs a depth-first search
#  - modified to avoid (non-tail-) recursive calls
#
def dfs_sm_any_cormen(graph, start):
    # set properties for start node
    parent = { start: None }
    # prepare loop variable
    greyed = set([start])
    path = [start]      # a list is efficient for a stack
    while path:
        # get deepest node in path
        node = path.pop()
        for adjacent in graph.neighbours(node):
            # skip if already discovered (grey)
            if adjacent in greyed: continue
            # if new then record parent relationship
            parent[adjacent] = node
            # ... mark it as discovered
            greyed.add(adjacent)
            # ... and make it the new pivot
            path = path + [node, adjacent]
            # abort for-loop to focus on new pivot
            break
    return parent


#
# inspired by Cormen etc. 
#  - untimed variant
#
# input:
#  - graph:    directed, connected, may be cyclic (dict+list representation)
#
# output:
#  - parent:   parent relationship to 'start' for all nodes in graph
#
# notes:
#  - performs a depth-first search
#  - modified to avoid (non-tail-) recursive calls
#
def dfs_sm_any_cormen_extended(graph, rootNodes=None):
    parent = dict()
    greyed = set()
    if not rootNodes: rootNodes = graph.nodes()
    for node in rootNodes:
        # skip if already discovered (grey)
        if node in greyed: continue 
        # if new then record it as a root
        parent[node] = None
        # ... mark it as discovered
        greyed.add(node)
        # ... and start depth-first search
        path = [node]
        while path:
            # get deepest node in path
            node = path.pop()
            for adjacent in graph.neighbours(node):
                # skip if already discovered (grey)
                if adjacent in greyed: continue
                # if new then record parent relationship
                parent[adjacent] = node
                # ... mark it as discovered
                greyed.add(adjacent)
                # ... and make it the new pivot
                path = path + [node, adjacent]
                # abort for-loop to focus on new pivot
                break
    return parent


#
# inspired by Cormen etc.
#  - unlike them we assume that the graph is connected (hence 'start' node)
#
# input:
#  - graph:      directed, connected, may be cyclic (dict+list representation)
#  - start:      root node to search from
#
# output:
#  - parent:     parent relationship to 'start' for all nodes in graph
#  - discovered: time slots for when each node was discovered (dictionary)
#  - finished:   time slots for when each node was fully processed (dictionary)
#
# notes:
#  - performs a depth-first search
#  - modified to avoid (non-tail-) recursive calls
#
def timeddfs_sm_any_cormen(graph, start):
    # set properties for start node
    time = 0
    parent = { start: None }
    discovered = { start: time }
    finished = {}
    # prepare loop variable
    greyed = set([start])
    path = [start]      # efficient stack
    while path:
        # get deepest node in path
        node = path.pop()
        isfinished = True
        for adjacent in graph.neighbours(node):
            # skip if already discovered (grey)
            if adjacent in greyed: continue
            # if new then record parent relationship
            parent[adjacent] = node
            # ... record its discovery time
            time = time + 1
            discovered[adjacent] = time
            # ... mark it as discovered
            greyed.add(adjacent)
            # ... make it the new pivot
            path = path + [node, adjacent]
            # ... and indicated that 'node' is not yet finished
            isfinished = False
            break
        if isfinished: 
            time = time + 1
            finished[node] = time
    return parent, discovered, finished


#
# from Cormen etc.
#
# input:
#  - graph:      directed, connected, may be cyclic (dict+list representation)
#
# output:
#  - forest:     trees covering all nodes in graph
#  - discovered: time slots for when each node was discovered (dictionary)
#  - finished:   time slots for when each node was fully processed (dictionary)
#
# notes:
#  - performs a depth-first search
#  - modified to avoid (non-tail-) recursive calls
#  - 'discovered' makes 'greyed' redundant
#  - experiment by using 'for-else' construct instead of 'isfinished' boolean
#
def timeddfs_sm_any_cormen_extended(graph, rootNodes=None):
    parent = dict()
    discovered = dict()
    finished = dict()
    time = 0
    greyed = set()
    if not rootNodes: rootNodes = graph.nodes()
    for root in rootNodes:
        # skip if already discovered (grey)
        if root in greyed: continue 
        # if new then record it as a root
        parent[root] = None
        # ... record its discovery time
        discovered[root] = time
        time += 1
        # ... mark it as discovered
        greyed.add(root)
        # ... and start depth-first search
        path = [root]
        while path:
            # get deepest node in path
            node = path.pop()
            #isfinished = True          # replaced by for-else
            for adjacent in graph.neighbours(node):
                # skip if already discovered (grey)
                if adjacent in greyed: continue
                # if new then record parent relationship
                parent[adjacent] = node
                # ... record its discovery time
                discovered[adjacent] = time
                time += 1               
                # ... mark it as discovered
                greyed.add(adjacent)
                # ... make it the new pivot
                path = path + [node, adjacent]
                # ... and indicated that 'node' is not yet finished
                #isfinished = False     # replaced by for-else
                break
            #if isfinished:             # replaced by for-else
            else:
                finished[node] = time
                time += 1
    return parent, discovered, finished









#
# from http://stackoverflow.com/questions/8922060/breadth-first-search-trace-path
#
# input:
#  - graph: directed, acyclic (dict+list representation)
#  - start: root node to search from
#  - end:   target node to search for
#
# output:
#  - path:  a shortest acyclic path (as list)
#
# notes:
#  - performs a breath-first search
#  - assumes acyclic input graph
#  - somewhat expensive queue.pop(0) operation since a list is used as queue (O(n))
#  - unnecessary work might be performed since 'node == end' check is not performed
#    when 'node' is first encountered (in for loop) but only later when it is popped
#  - large memory footprint as it stores the rim as full-length paths
#
def bfs_ss_shortest_stackoverflow(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # test if path was found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.neighbours(node):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


#
# slightly optimised version of the above
#
def bfs_ss_shortest_stackoverflow_optimised(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # test if path was found
        if node == end: 
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.neighbours(node):
            new_path = list(path)
            new_path.append(adjacent)
            # optimisation: return path when target is first encountered
            if adjacent == end: return new_path
            queue.append(new_path)










from collections import deque   # for efficient implementation of queue (doubly linked list)

#
# inspired by Cormen etc.
#  - unlike them we return the first path found
#
# input:
#  - graph: directed, may be cyclic (dict+list representation)
#  - start: root node to search from
#  - end:   target node to search for
#
# output:
#  - path:  a shortest acyclic path (as list)
#
# notes:
#  - performs a breath-first search
#  - somewhat expensive rim.pop(0) operation since a list is used as queue (O(n))
#  - unnecessary work might be performed since 'node == end' check is not performed
#    when 'node' is first encountered (in for loop) but only later when it is popped
#  - by having the 'parent' dictionary we do not need to store rim as full-length paths
#
def bfs_ss_shortest_cormen(graph, start, end):
    # to avoid cycles we grey out nodes that have already been discovered
    # - using a set gives us efficient look-up
    greyed = set([start])
    # to allow backtracking we record how each node was discovered 
    # - using a dictionary gives us efficient look-up
    parent = { start: None }
    # we store rim as a list
    # - not optimal since for BFS we need FIFO
    rim = [start]
    while rim:
        # get the next node where the rim should be expanded
        node = rim.pop(0)
        if node == end:
            # traverse parent map to get path
            return path_from_root(parent, node)
        for adjacent in graph.neighbours(node):
            if adjacent in greyed: continue
            parent[adjacent] = node
            greyed.add(adjacent)
            rim.append(adjacent)


#
# optimised version of the above
#
def bfs_ss_shortest_cormen_optimised(graph, start, end):
    # optimisation: no need to start the bigger machinery if already there
    if start == end:
        return [start]
    greyed = set([start])
    parent = { start: None }
    # optimisation: use a double linked list to store rim -- good for FIFO
    rim = deque([start])
    while rim:
        # optimisation: this is now fast (O(1))
        node = rim.popleft()
        for adjacent in graph.neighbours(node):
            if adjacent in greyed: continue
            elif adjacent == end:
                # we have found the target, traverse parent map to get path
                parent[adjacent] = node
                return path_from_root(parent, adjacent)
            else:
                parent[adjacent] = node
                greyed.add(adjacent)
                rim.append(adjacent)


#
# from Cormen etc.
#
# input:
#  - graph:    directed, may be cyclic (dict+list representation)
#  - start:    root node to search from
#
# output:
#  - parent:   parent relationship to 'start' for all nodes in graph
#  - distance: shortest distance to 'start' for all nodes in graph
#
# notes:
#  - performs a breath-first search
#       
def bfs_sm_shortest_cormen(graph, start):
    # set properties for start node
    parent = { start: None }
    distance = { start: 0 }
    # prepare loop variables
    greyed = set([start])
    rim = deque([start])    # efficient queue (doubly linked list)
    # loop until the rim covers every reachable node
    while rim:
        # get next node on the rim
        node = rim.popleft()
        # explore its adjacent nodes
        for adjacent in graph.neighbours(node):
            # skip if already discovered (grey)
            if adjacent in greyed: continue
            # if new then record properties
            parent[adjacent] = node
            distance[adjacent] = distance[node] + 1
            # mark it as discovered and extend rim
            greyed.add(adjacent)
            rim.append(adjacent)
    # return properties
    return parent, distance








#
# from Cormen etc.
#
# input:
#  - graph:    directed, acyclic (dict+list representation)
#
# output:
#  - ordering: topological ordering for the nodes (as list)
#
# notes:
#  - modified to avoid (non-tail-) recursive calls
#
def topological_sort(graph):
    _,_,f = timeddfs_sm_any_cormen_extended(graph)
    # sort the list by the values of the finished dictionary
    f_as_tuplelist = f.items()
    sortkey = lambda tuple: tuple[1]
    sorted_f = sorted(f_as_tuplelist, key=sortkey, reverse=True)
    # return only the keys
    return [k for (k,v) in sorted_f]








def transpose(graph):
    transposed = dict()
    for node in graph.nodes():
        transposed[node] = []
    for node in graph.nodes():
        for adjacent in graph.neighbours(node):
            transposed[adjacent].append(node)
    return Graph(transposed)


def forest(parent):
    roots = []
    graph = dict()
    for node in parent.iterkeys():
        graph[node] = []
    for (child,parent) in parent.iteritems():
        if parent == None: roots.append(child)
        if parent != None: graph[parent].append(child)
    return roots, Graph(graph)


def reachable(graph, root):
    reached = set([root])
    # prepare loop variable
    path = [root]
    while path:
        # get deepest node in path
        node = path.pop()
        for adjacent in graph.neighbours(node):
            # skip if already in 'reached'
            if adjacent in reached: continue
            # if new then record it
            reached.add(adjacent)
            # ... and make it the new pivot
            path = path + [node, adjacent]
            # abort for-loop to focus on new pivot
            break
    return reached


#
# from Cormen etc.
#
# input:
#  - graph:    directed, may be cyclic (dict+list representation)
#
# output:
#  - ordering: the strongly connected components in the graph (as list of sets)
#
# Notes on correctness:
#  - note that components in graph are the same as in transpose(graph), by def.
#  - basic argument is that when a node is picked in the second DFS, the traversal will 
#    visit all nodes in its component but will not visit nodes belonging to other components
#  - first case easy since by def. there is a path between all nodes in a component
#     - by induction no traversal has visited nodes in the component so no nodes greyed out
#  - second case more involved:
#     - assume that while traversing C -- in transposed(graph) -- there's an edge to C': C -> C'
#     - argue that all nodes in C' are greyed out already (so that they will be ignored)
#     - enough to show that EXISTS x' \in C' : ALL x \in C : f[x'] > f[x] (ie f(C') > f(C))
#     - but if C -> C' in transposed(graph) then C' -> C in graph, so in first DFS:
#        - if x' picked before any x \in C then all x \in C will be finished before x'
#          since C' -> C edge will mean visiting all x \in C not already greyed
#        - if some x \in C picked before x' then all x \in C not already greyed will be visited
#          yet no x \in C will be, since C' -> C imply C -/-> C' when C, C' are maximum
def strongly_connected_components(graph):
    # use first DFS to get finished times
    _,_,f1 = timeddfs_sm_any_cormen_extended(graph)
    # sort nodes according to finished time
    first = lambda (x,y): x
    second = lambda (x,y): y
    f1_sorted = sorted(f1.iteritems(), key=second, reverse=True)
    nodes_sorted = map(first, f1_sorted)
    # use second DFS to get component trees
    graph_t = transpose(graph)
    p2,_,_ = timeddfs_sm_any_cormen_extended(graph_t, nodes_sorted)
    # find roots and parent trees
    roots, trees = forest(p2)
    # compute components by reachability from each root
    components = []
    for root in roots:
        component = reachable(trees, root)
        components.append(component)
    return components








def timeddfs_sm_any_cormen_extended_finished(graph, rootNodes=None):
    finished = []
    greyed = set()
    if not rootNodes: rootNodes = graph.nodes()
    for root in rootNodes:
        # skip if already discovered (grey)
        if root in greyed: continue 
        # if new then mark it as discovered
        greyed.add(root)
        # ... and start depth-first search
        path = [root]
        while path:
            # get deepest node in path
            node = path.pop()
            for adjacent in graph.neighbours(node):
                # skip if already discovered (grey)
                if adjacent in greyed: continue
                # if new then mark it as discovered
                greyed.add(adjacent)
                # ... make it the new pivot
                path = path + [node, adjacent]
                # ... and indicated that 'node' is not yet finished
                break
            else:
                finished.append(node)
    return finished


def timeddfs_sm_any_cormen_extended_components(graph, rootNodes=None):
    components = []
    greyed = set()
    if not rootNodes: rootNodes = graph.nodes()
    for root in rootNodes:
        # skip if already discovered (grey)
        if root in greyed: continue 
        # if new then mark it as discovered
        greyed.add(root)
        # ... start a new component
        component = set([root])
        # ... and start depth-first search
        path = [root]
        while path:
            # get deepest node in path
            node = path.pop()
            for adjacent in graph.neighbours(node):
                # skip if already discovered (grey)
                if adjacent in greyed: continue
                # if new then mark it as discovered
                greyed.add(adjacent)
                # ... add to component
                component.add(adjacent)
                # ... make it the new pivot
                path = path + [node, adjacent]
                # ... and indicated that 'node' is not yet finished
                break
        components.append(component)
    return components


def strongly_connected_components_optimised(graph):
    # use first DFS to get finished times
    f = timeddfs_sm_any_cormen_extended_finished(graph)
    # use second DFS to get component trees
    graph_t = transpose(graph)
    f.reverse()		# in-place reversal 
    components = timeddfs_sm_any_cormen_extended_components(graph_t, f)
    return components







# ********
#
# performance tests
#
# ********
        
if __name__ == '__main__':

    from random_graph_generation import random_dictlist_graph_sample_split_set_optimised as random_dictlist_graph

    from timeit import Timer
    import gc




    randgraph_10x50 = Graph(random_dictlist_graph(10, 50))
    randgraph_20x100 = Graph(random_dictlist_graph(20, 100))

    print "\n*** Tests for 'pythondocs' DFS methods: ***\n"

    tests = [   ("randgraph_10x50", 0, 9),
                ("randgraph_20x100", 0, -1)    ]

    algos = [   "dfs_ss_any_pythondocs",
                "dfs_ss_all_pythondocs",
                "dfs_ss_shortest_pythondocs" ]

    for test in tests:
        graphName = test[0]
        start = test[1]
        end = test[2]
        print "* {0}, from {1} to {2} *".format(graphName, start, end)
        graph = locals()[graphName]
        for algo in algos:
            algocode = locals()[algo]
            time = Timer(lambda: algocode(graph, start, end)).timeit(number=3)
            print "{0:<55} : {1}".format(algo, time)
            gc.collect()
        print ""




    print "\n*** Tests for 'cormen' DFS methods: ***\n"

    randgraph_100x5000 = Graph(random_dictlist_graph(100, 5000))
    randgraph_10000x1000000 = Graph(random_dictlist_graph(10000,1000000))
    randgraph_20000x3500000 = Graph(random_dictlist_graph(20000,3500000))

    tests = [   ("randgraph_10x50", 0, 9),
                ("randgraph_20x100", 0, -1),

                ("randgraph_100x5000", 0, 4500),
                ("randgraph_10000x1000000", 0, 900000),
                ("randgraph_20000x3500000", 0, 3400000)     ]

    algos = [   "dfs_sm_any_cormen",
                "timeddfs_sm_any_cormen"    ]

    for test in tests:
        graphName = test[0]
        start = test[1]
        end = test[2]
        print "* {0}, from {1} to {2} *".format(graphName, start, end)
        graph = locals()[graphName]
        for algo in algos:
            algocode = locals()[algo]
            time = Timer(lambda: algocode(graph, start)).timeit(number=3)
            print "{0:<55} : {1}".format(algo, time)
            gc.collect()
        print ""




    print "\n*** Tests for 'cormen_extended' DFS methods: ***\n"

    algos = [   "dfs_sm_any_cormen_extended",
                "timeddfs_sm_any_cormen_extended"   ]

    for test in tests:
        graphName = test[0]
        start = test[1]
        end = test[2]
        print "* {0}, from {1} to {2} *".format(graphName, start, end)
        graph = locals()[graphName]
        for algo in algos:
            algocode = locals()[algo]
            time = Timer(lambda: algocode(graph, [0])).timeit(number=3)
            print "{0:<55} : {1}".format(algo, time)
            gc.collect()
        print ""
    print "\n"





    print "\n*** Tests for 'ss_cormen' BFS methods: ***\n"

    tests = [   ("randgraph_10x50", 0, 9),
                ("randgraph_20x100", 0, -1),

                ("randgraph_100x5000", 0, 4500),
                ("randgraph_10000x1000000", 0, 900000),
                ("randgraph_20000x3500000", 0, 3400000)     ]

    algos = [   "bfs_ss_shortest_cormen",
                "bfs_ss_shortest_cormen_optimised"          ]

    for test in tests:
        graphName = test[0]
        start = test[1]
        end = test[2]
        print "* {0}, from {1} to {2} *".format(graphName, start, end)
        graph = locals()[graphName]
        for algo in algos:
            algocode = locals()[algo]
            time = Timer(lambda: algocode(graph, start, end)).timeit(number=3)
            print "{0:<55} : {1}".format(algo, time)
            gc.collect()
        print ""
    print "\n"




    print "\n*** Tests for 'sm_cormen' BFS methods: ***\n"

    algos = [  "bfs_sm_shortest_cormen"  ]

    for test in tests:
        graphName = test[0]
        start = test[1]
        end = test[2]
        print "* {0}, from {1} to {2} *".format(graphName, start, end)
        graph = locals()[graphName]
        for algo in algos:
            algocode = locals()[algo]
            time = Timer(lambda: algocode(graph, start)).timeit(number=3)
            print "{0:<55} : {1}".format(algo, time)
            gc.collect()
        print ""
    print "\n"




    print "\n*** Tests for 'strongly_connected_components' methods: ***\n"

    tests = [   "randgraph_10x50",
                "randgraph_20x100",

                "randgraph_100x5000",
                "randgraph_10000x1000000",
                "randgraph_20000x3500000"     ]

    algos = [  "strongly_connected_components",
               "strongly_connected_components_optimised"  ]

    for test in tests:
        print "* {0} *".format(test)
        graph = locals()[test]
        for algo in algos:
            algocode = locals()[algo]
            time = Timer(lambda: algocode(graph)).timeit(number=3)
            print "{0:<55} : {1}".format(algo, time)
            gc.collect()
        print ""
    print "\n"
