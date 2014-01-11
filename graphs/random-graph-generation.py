
import random
import itertools

from timeit import Timer
import gc






# ********
#
# methods from generating directed, unconnected, cyclic (single) graph
#  - nodes as list
#  - edges as pair list
#
# ********

def random_listlist_graph_choice(no_nodes, no_edges):
    nodes = range(no_nodes)
    no_edges = min(no_edges, no_nodes**2)
    edges = set()
    while len(edges) < no_edges:
        edge = (random.choice(nodes), random.choice(nodes))
        edges.add(edge)
    return (nodes,edges)

def random_listlist_graph_choice_optimised(no_nodes, no_edges):
    nodes = range(no_nodes)
    no_edges = min(no_edges, no_nodes**2)
    edges = set()
    edges_add = edges.add
    random_choice = random.choice
    while len(edges) < no_edges:
        edge = (random_choice(nodes), random_choice(nodes))
        edges_add(edge)
    return (nodes,edges)

def random_listlist_graph_choice_alt(no_nodes, no_edges):
    nodes = range(no_nodes)
    no_edges = min(no_edges, no_nodes**2)
    edges = set()
    for n in xrange(no_edges):
        edge = (random.choice(nodes), random.choice(nodes))
        while edge in edges:
            edge = (random.choice(nodes), random.choice(nodes))
        edges.add(edge)
    return (nodes,edges)

def random_listlist_graph_choice_alt_optimised(no_nodes, no_edges):
    nodes = range(no_nodes)
    no_edges = min(no_edges, no_nodes**2)
    edges = set()
    edges_add = edges.add
    random_choice = random.choice
    for n in xrange(no_edges):
        edge = (random_choice(nodes), random_choice(nodes))
        while edge in edges:
            edge = (random_choice(nodes), random_choice(nodes))
        edges_add(edge)
    return (nodes,edges)

def random_listlist_graph_sample_naive(no_nodes, no_edges):
    nodes = range(no_nodes)
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    all_edges = [(x,y) for x in nodes for y in nodes]
    edges = random.sample(all_edges, no_edges)
    return (nodes,edges)

def random_listlist_graph_sample(no_nodes, no_edges):
    nodes = xrange(no_nodes)
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    encoded_edges = random.sample(xrange(max_no_edges), no_edges)
    edges = map(lambda edge: divmod(edge, no_nodes), encoded_edges)
    return (nodes,edges)

def random_listlist_graph_sample_lazy(no_nodes, no_edges):
    nodes = xrange(no_nodes)
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    encoded_edges = random.sample(xrange(max_no_edges), no_edges)
    edge_decoder = lambda edge: divmod(edge, no_nodes)
    edges = itertools.imap(edge_decoder, encoded_edges)
    return (nodes,edges)








# ********
#
# methods from generating directed, unconnected, cyclic (single) graph
#  - nodes as dictionary
#  - edges as adjacency list
#
# ********

def random_dictlist_graph_choice(no_nodes, no_edges):
    graph = {}
    for node in xrange(no_nodes):
        graph[node] = set([])
    nodes = xrange(no_nodes)
    for n in xrange(no_edges):
        from_node = random.choice(nodes)
        to_node = random.choice(nodes)
        while to_node in graph[from_node]:
            from_node = random.choice(nodes)
            to_node = random.choice(nodes)
        graph[from_node].add(to_node)
    return graph

def random_dictlist_graph_choice_optimised(no_nodes, no_edges):
    graph = {}
    for node in xrange(no_nodes):
        graph[node] = set([])
    nodes = xrange(no_nodes)
    random_choice = random.choice
    for n in xrange(no_edges):
        from_node = random_choice(nodes)
        to_node = random_choice(nodes)
        while to_node in graph[from_node]:
            from_node = random_choice(nodes)
            to_node = random_choice(nodes)
        graph[from_node].add(to_node)
    return graph

def random_dictlist_graph_sample(no_nodes, no_edges):
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    encoded_edges = random.sample(xrange(max_no_edges), no_edges)
    graph = {}
    for node in xrange(no_nodes):
        graph[node] = []
    for edge in encoded_edges:
        (node_from, node_to) = divmod(edge, no_nodes)
        graph[node_from].append(node_to)
    return graph

def random_dictlist_graph_sample_split_set(no_nodes, no_edges, weight=0.6):
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    if no_edges < max_no_edges*weight:
        existing_edges = random.sample(xrange(max_no_edges), no_edges)
        graph = {}
        for node in xrange(no_nodes):
            graph[node] = []
        for edge in existing_edges:
            (node_from,node_to) = divmod(edge, no_nodes)
            graph[node_from].append(node_to)
        return graph
    else:
        missing_edges = random.sample(xrange(max_no_edges), max_no_edges - no_edges)
        # convert missing_edges to a set for quick look-up
        missing_edges = set(missing_edges)
        graph = {}
        for node_from in xrange(no_nodes):
            graph[node_from] = []
            for node_to in xrange(no_nodes):
                if not node_from*no_nodes+node_to in missing_edges: 
	                graph[node_from].append(node_to)
        return graph

def random_dictlist_graph_sample_split_set_optimised(no_nodes, no_edges, weight=0.6):
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    if no_edges < max_no_edges*weight:
        existing_edges = random.sample(xrange(max_no_edges), no_edges)
        graph = {}
        for node in xrange(no_nodes):
            graph[node] = []
        for edge in existing_edges:
            (node_from,node_to) = divmod(edge, no_nodes)
            graph[node_from].append(node_to)
        return graph
    else:
        missing_edges = random.sample(xrange(max_no_edges), max_no_edges - no_edges)
        # convert missing_edges to a set for quick look-up
        missing_edges = set(missing_edges)
        graph = {}
        for node_from in xrange(no_nodes):
            node_edges = []
            node_edges_append = node_edges.append
            for node_to in xrange(no_nodes):
                if not node_from*no_nodes+node_to in missing_edges: 
	                node_edges_append(node_to)
            graph[node_from] = node_edges
        return graph

def random_dictlist_graph_sample_split_sorted(no_nodes, no_edges, weight=0.6):
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    if no_edges < max_no_edges*weight:
        existing_edges = random.sample(xrange(max_no_edges), no_edges)
        graph = {}
        for node in xrange(no_nodes):
            graph[node] = []
        for edge in existing_edges:
            # decode edge into from and to node
            (node_from, node_to) = divmod(edge, no_nodes)
            graph[node_from].append(node_to)
        return graph
    else:
        missing_edges = random.sample(xrange(max_no_edges), max_no_edges - no_edges)
        missing_edges = sorted(missing_edges, reverse=True)
        graph = {}
        next_missing_edge = missing_edges.pop() if missing_edges else None
        for node_from in xrange(no_nodes):
            graph[node_from] = []
            for node_to in xrange(no_nodes):
                if node_from*no_nodes+node_to == next_missing_edge: 
                    next_missing_edge = missing_edges.pop() if missing_edges else None
                    continue
                graph[node_from].append(node_to)
        return graph

def random_dictlist_graph_sample_split_sorted_optimised(no_nodes, no_edges, weight=0.6):
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    if no_edges < max_no_edges*weight:
        existing_edges = random.sample(xrange(max_no_edges), no_edges)
        graph = {}
        for node in xrange(no_nodes):
            graph[node] = []
        for edge in existing_edges:
            # decode edge into from and to node
            (node_from, node_to) = divmod(edge, no_nodes)
            graph[node_from].append(node_to)
        return graph
    else:
        missing_edges = random.sample(xrange(max_no_edges), max_no_edges - no_edges)
        missing_edges = sorted(missing_edges, reverse=True)
        graph = {}
        next_missing_edge = missing_edges.pop() if missing_edges else None
        for node_from in xrange(no_nodes):
            node_edges = []
            node_edges_append = node_edges.append
            for node_to in xrange(no_nodes):
                if node_from*no_nodes+node_to == next_missing_edge: 
                    next_missing_edge = missing_edges.pop() if missing_edges else None
                    continue
                node_edges_append(node_to)
            graph[node_from] = node_edges
        return graph

def random_dictlist_graph_sample_split_sorted_alt(no_nodes, no_edges, weight=0.6):
    max_no_edges = no_nodes**2
    no_edges = min(no_edges, max_no_edges)
    if no_edges < max_no_edges*weight:
        existing_edges = random.sample(xrange(max_no_edges), no_edges)
        graph = {}
        for node in xrange(no_nodes):
            graph[node] = []
        for edge in existing_edges:
            # decode edge into from and to node
            (node_from, node_to) = divmod(edge, no_nodes)
            graph[node_from].append(node_to)
        return graph
    else:
        missing_edges = random.sample(xrange(max_no_edges), max_no_edges - no_edges)
        graph = {}
        for node in xrange(no_nodes):
            graph[node] = []
        missing_edges = sorted(missing_edges, reverse=True)
        # linear scan of *all* edges (adding all non-missing)
        edge = 0
        while missing_edges:
            # efficient since list is sorted in reverse order
            next_missing_edge = missing_edges.pop()
            while edge < next_missing_edge:
                # decode edge into from and to node
                (node_from,node_to) = divmod(edge, no_nodes)
                graph[node_from].append(node_to)
                edge += 1
            edge += 1
        while edge < max_no_edges:
            (node_from,node_to) = divmod(edge, no_nodes)
            graph[node_from].append(node_to)
            edge += 1       
        return graph








# ********
#
# performance tests
#
# ********


print "\n*** Tests for 'random_listlist' methods: ***\n"

tests = [  	(200,3000), (2000,30000), (2000,1000000), (2000,3000000)	]
algos = [	"random_listlist_graph_choice",
			"random_listlist_graph_choice_optimised",
			"random_listlist_graph_choice_alt",
			"random_listlist_graph_choice_alt_optimised",
	#		"random_listlist_graph_sample_naive",
			"random_listlist_graph_sample",
			"random_listlist_graph_sample_lazy" ]

for test in tests:
	print test
	for algo in algos:
		algocode = locals()[algo]
		time = Timer(lambda: algocode(*test)).timeit(number=3)
		print "{0:<55} : {1}".format(algo, time)
		gc.collect()
	print ""

print "\n*** Tests for 'random_dictlist' methods: ***\n"

tests = [ 	(200,3000), (2000,30000), (2000,1000000), (2000,3000000) ]
#tests = [ 	(2000,2000000), (2000,3500000), (2000,3999000), (10000,4000000)	]

algos = [	"random_dictlist_graph_choice",
			"random_dictlist_graph_choice_optimised",
			"random_dictlist_graph_sample",
			"random_dictlist_graph_sample_split_set",
			"random_dictlist_graph_sample_split_sorted",
			"random_dictlist_graph_sample_split_sorted_optimised",
		 	"random_dictlist_graph_sample_split_sorted_alt"			]

for test in tests:
	print test
	for algo in algos:
		algocode = locals()[algo]
		time = Timer(lambda: algocode(*test)).timeit(number=3)
		print "{0:<55} : {1}".format(algo, time)
		gc.collect()
	print ""
