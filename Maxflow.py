import graph
from graph import Graph, graph_from_edgelist as graphFromList
from collections import deque
import graphviz
import sys
import getopt
import re
import os
import pdb

def buildResidualGraphAndFlow(flow, G):
	"""
	This function creates Residual Graph and the graph on which the flow is applied.
	:param flow: value of flow
	:param G : initial Graph
	:return: a residual graph and graph on which the flow is applied
	"""
	edges_initial = G.edges()

	graph_flow = Graph(True)


	for e in edges_initial:
		u = graph_flow.insert_vertex(e[0].tag(), e[0].value())
		v = graph_flow.insert_vertex(e[1].tag(), e[1].value())
		graph_flow.insert_edge(u, v, flow)

	residual_graph = Graph(True)
	for e in edges_initial:
		u = residual_graph.insert_vertex(e[0].tag(), e[0].value())
		v = residual_graph.insert_vertex(e[1].tag(), e[1].value())
		residual_graph.insert_edge(u, v, e[2]-flow)

	return graph_flow, residual_graph

def edmondsKarpAlgorithm(initial_graph):
	"""
	This is the implementation of edmondsKaroAlgorithm.
	This is the link for seeing the pseudo-code : https://fr.wikipedia.org/wiki/Algorithme_d%27Edmonds-Karp
	:param initial_graph:
	:param residual_graph:
	:return: max_flow
	"""
	# s = initial_graph.get_vertex("s").value()
	# t = initial_graph.get_vertex("t").value()
	# initial_graph_edges = initial_graph.edges()
	# # residual_graph_edges = residual_graph.edges()
	# n_vertices = len(initial_graph.vertices())
	# capacities_matrix = [[0 for _ in range(n_vertices)]for _ in range(n_vertices)]
	# flow_matrix = [[0 for _ in range(n_vertices)]for _ in range(n_vertices)]
	# #residual_graph = {}
	#
	# for e in initial_graph_edges:
	# 	orig = e[0].value()
	# 	dest = e[1].value()
	# 	capacities_matrix[orig][dest] = e[2]
	# 	# residual_graph[e[0]][e[1]] = e[2]
	# 	flow_matrix[e[0].value()][e[1].value()] = 0
	#
	# f = 0
	# while True:
	# 	max_flow, parents_dict = bfs(s,t,capacities_matrix, flow_matrix)
	# 	if max_flow == 0:
	# 		break
	# 	f += max_flow
	# 	v = t
	# 	while v != s:
	# 		u = parents_dict[v]
	# 		flow_matrix[u][v] += max_flow
	# 		flow_matrix[v][u] -= max_flow
	# 		v = u
	# return f,flow_matrix

	# Initialisation du flot à 0
	max_flow = 0
	source = initial_graph.get_vertex("s")
	sink = initial_graph.get_vertex("t")
	n = len(initial_graph.vertices())
	# As long as there is an increasing path in the residual graph
	while True:
		parent = [-1] * n
		if not bfs(initial_graph, source, sink, parent):
			break
		# Find the minimum residual capacity of the path increasing
		path_flow = float("Inf")
		s = sink
		while s != source:
			for e in initial_graph.incident_edges(parent[s.value()]):
				if e.endpoints()[1] == s:
					path_flow = min(path_flow, e.value() - e.flow())
					break
			s = parent[s.value()]
		# Update of the flow and the residual graph
		max_flow += path_flow
		v = sink
		while v != source:
			u = parent[v.value()]
			for e in initial_graph.incident_edges(u):
				if e.endpoints()[1] == v:
					e[4] += path_flow
					break

			for e in initial_graph.incident_edges(v):
				if e.endpoints()[1] == u:
					e[4] -= path_flow
					break
			v = u
	return max_flow

def bellmanFordAlgorithm(g, source, sink ):
	"""
	This function aim to find the shortest path using Bellman-Ford algorithm
	:param graph:
	:param s:
	:param t:
	:return: path : the shortest path
	:return: dist[i] : the final distance of every node from s
	"""

	list_vertices = g.vertices()
	n = len(list_vertices)
	dist = [float('inf')] * n
	dist[source.value()] = 0
	parent = [-1] * n
	for _ in range(n - 1):
			for e in g.edges():
				if e.value() > 0 and dist[e.endpoints()[0].value()] + e.cost() < dist[e.endpoints()[1].value()]:
					dist[e.endpoints()[1].value()] = dist[e.endpoints()[0].value()] + e.cost()
					parent[e.endpoints()[1].value()] = e.endpoints()[0]

	# pdb.set_trace()
	path = []
	u = sink
	while u != source:
		path.append(u)
		u = parent[u.value()]
	path.reverse()

	return path, dist[sink.value()]
def bfs(g,source,sink,parent):
	# s
	# n = len(capacities_matrix)
	# parents = [-1] * n
	# maximal_flow = [-1] * n
	# for v in range(n):
	# 	parents[v] = -1
	# 	maximal_flow[v] = float("inf")
	#
	# parents[s] = -2
	#
	# queue = deque([])
	# queue.append(s)
	#
	# while len(queue):
	# 	u = queue.popleft()
	# 	for v in range(n):
	# 		if capacities_matrix[u][v] - flow_matrix[u][v] > 0 and parents[v] == -1:
	# 			parents[v] = u
	# 			maximal_flow[v] = min(maximal_flow[u], capacities_matrix[u][v] - flow_matrix[u][v])
	# 			if v != t:
	# 				queue.append(v)
	# 			else:
	# 				return maximal_flow[t],parents
	# return 0,parents

	queue = deque()
	queue.append(source)
	visited = set()
	visited.add(source)
	while queue:
		u = queue.popleft()
		for e in g.incident_edges(u):
			if e.endpoints()[1] not in visited and e.value() > e.flow():
				visited.add(e.endpoints()[1])
				parent[e.endpoints()[1].value()] = u
				if e.endpoints()[1] == sink:
					return True
				queue.append(e.endpoints()[1])
	return False

def visualizeAGraph(residual_graph):
	color_edge_red = {'color': 'red'}
	graph = graphviz.Digraph()
	for key in residual_graph.keys():
		graph.node(key.tag())
	for key,val in residual_graph.items():
		for key1,val2 in val.items():
			if val2 > 0:
				graph.edge(key.tag(),key1.tag(),str(val2))
			else:
				graph.edge(key.tag(), key1.tag(), str(val2),**color_edge_red)
	graph.render()
def recuperateFileFromInput():
	"""
	 this function aim to recuperate the graphviz file from input and extract the edges from this file
	 in the list form
	"""
	try:
		opts, args = getopt.getopt(sys.argv[1:], "i", ["input"])
	except getopt.GetoptError as err:
		print(err)
		print("Nom du programme <{-i | --input}> nom du fichier à lire ")
		sys.exit(2)
	if opts[0][0] == "-i":
		with open(args[0],"r") as file_to_read:
			input_to_parse = file_to_read.read()

		tab_to_parse = input_to_parse.split("\n")
	edges = []
	for i in range(5, len(tab_to_parse)):
		if tab_to_parse[i] == "":
			break
		edges.append(tab_to_parse[i].strip())
	return edges

def parseInputFile():
	"""
	This function parse the edges extracted to the structure of Graph Class oin the order to
	use the algorithms which permit us to compute the maw flow with the minimal cost
	"""
	edges = recuperateFileFromInput()
	pattern = r'^\s*(\w+) -> (\w+) \[label = <<font color=\"\w+\">(\d+)<\/font>,<font color=\"\w+\">(\W{0,1}\d+)<\/font>>\]'
	regex_compile = re.compile(pattern)
	edges_list = []
	for s in edges:
		result = regex_compile.search(s)
		if result:
			edges_list.append((result.group(1), result.group(2), int(result.group(3)), int(result.group(4))))
	return graphFromList(edges_list, True)

def main():
	# g_initial = Graph(True)
	g_initial = parseInputFile()
	s = g_initial.get_vertex("s")
	t = g_initial.get_vertex("t")
	print(bellmanFordAlgorithm(g_initial,s,t))

	# s = g_initial.insert_vertex("s", 0)
	# b = g_initial.insert_vertex("b", 1)
	# c = g_initial.insert_vertex("c", 2)
	# d = g_initial.insert_vertex("d", 3)
	# e = g_initial.insert_vertex("e", 4)
	# f = g_initial.insert_vertex("f", 5)
	# t = g_initial.insert_vertex("t", 6)
	# #
	# g_initial.insert_edge(s, d, 3)
	# g_initial.insert_edge(s, b, 3)
	# g_initial.insert_edge(c, s, 3)
	# g_initial.insert_edge(c,d, 1)
	# g_initial.insert_edge(c, e, 2)
	# g_initial.insert_edge(b, c, 4)
	# g_initial.insert_edge(e, b, 1)
	# g_initial.insert_edge(e, t, 1)
	# g_initial.insert_edge(d, e, 2)
	# g_initial.insert_edge(d, f, 6)
	# g_initial.insert_edge(f, t, 9)
	# s = g_initial.insert_vertex('s',0)
	# v = g_initial.insert_vertex('v',1)
	# u = g_initial.insert_vertex('u',2)
	# t = g_initial.insert_vertex('t',3)
	#
	# g_initial.insert_edge(s,u,4)
	# g_initial.insert_edge(s,v,2)
	# g_initial.insert_edge(u,v,3)
	# g_initial.insert_edge(u,t,1)
	# g_initial.insert_edge(v,t,6)

	# flow = edmondsKarpAlgorithm(g_initial)
	# print(flow)
	# print(flow)




	#visualizeAGraph(residual_graph)

    # g_flow, residual_g = buildResidualGraphAndFlow(0, g_initial)


if __name__ == "__main__":
    main()
