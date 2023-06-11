import graph
from graph import Graph, graph_from_edgelist as graphFromList
from collections import deque
import graphviz
import sys
import getopt
import re
import os
import pdb
import networkx as nx
from networkx.algorithms import minimum_cut


def edmondsKarpAlgorithm(initial_graph,source,sink):
	"""
	This is the implementation of edmondsKaroAlgorithm.
	:param initial_graph
	:param source
	:param sink
	:return: max_flow,graph_modified and list of flow
	"""

	# Flow initialization to 0
	max_flow = 0
	n = len(initial_graph.vertices())
	flow_list = {}
	for e in initial_graph.edges():
		flow_list[e] = [0]

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
					flow_list[e].append(path_flow)
					break

			for e in initial_graph.incident_edges(v):
				if e.endpoints()[1] == u:
					e[4] -= path_flow
					break
			v = u

	return max_flow,initial_graph,flow_list

def bellmanFordAlgorithm(g, source, sink ):
	"""
	This function aim to find the shortest path using Bellman-Ford algorithm
	:param g: graph initial
	:param source:
	:param sink:
	:return: parent : the list of parents of vertices
	:return: dist[sink] : the final distance of sink
	"""
	list_vertices = g.vertices()
	n = len(list_vertices)
	dist = [float('inf')] * n
	dist[source.value()] = 0
	parent = [-1] * n
	for _ in range(n - 1):
			for e in g.edges():
				if e.value() > e.flow() and dist[e.endpoints()[0].value()] + e.cost() < dist[e.endpoints()[1].value()]:
					dist[e.endpoints()[1].value()] = dist[e.endpoints()[0].value()] + e.cost()
					parent[e.endpoints()[1].value()] = e.endpoints()[0]

	return parent, dist[sink.value()]
def bfs(g,source,sink,parent):
	"""

	:param g:
	:param source:
	:param sink:
	:param parent:
	:return: True if the sink is reached False if it is not
	"""

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

def bfs_cut_min(g, source, visited):
	"""
	this function specifies in the visited array whether the vertex is visited or not
	We use this function to compute the cut min
	:param g:
	:param source:
	:param visited:
	:return:
	"""
	queue = deque()
	queue.append(source)
	visited[source.value()] = True
	while queue:
		u = queue.popleft()
		for e in g.incident_edges(u):
			if  not visited[e.endpoints()[1].value()] and e.value() > e.flow():
				visited[e.endpoints()[1].value()] = True
				queue.append(e.endpoints()[1])
def min_cut(g,source):
	"""
	this function compute the cut min of some graph
	:param g:
	:param source:
	:return: visited edges and unvisited edges
	"""
	n = len(g.vertices())
	visited = [False] * n
	bfs_cut_min(g, source, visited)
	min_cut_edges = []
	visited_edges = set()
	unvisited_edges = set()

	for u in g.vertices():
		if visited[u.value()]:
			visited_edges.add(u)
		if not visited[u.value()]:
			unvisited_edges.add(u)
	return visited_edges,unvisited_edges
def visualizeAGraph(residual_graph,file_name,ind_name):
	"""
	this
	:param residual_graph:
	:param file_name: file_name of the image file
	:param ind_name: name that differentiates files resulting from a specific algorithm
	:return: void
	"""
	color_edge_red = {'color': 'red'}
	graph = graphviz.Digraph()
	for e in residual_graph.edges():
		if e[2] > 0:
			graph.node(e[0].tag())
			graph.node(e[1].tag())
			graph.edge(e[0].tag(),e[1].tag(),str(e[4])+"/"+str(e[2])+"/"+str(e[3]))
	output_directory = "out"
	file_name = file_name.split(".")[0]

	graph.render(filename=file_name+"_"+ind_name, directory=output_directory, format="pdf")

def execute():
	"""
	 The purpose of this function is to execute
	 the appropriate algorithm according to the argument on the standard input.
	"""
	try:
		opts, args = getopt.getopt(sys.argv[1:], "mfM", ["mincut","maxflow","mincostmaxflow"])
	except getopt.GetoptError as err:
		print(err)
		print("Nom du programme <{-i | --input}> nom du fichier à lire ")
		sys.exit(2)
	g, source, sink = 0,0,0
	for o,a in opts:
		#pdb.set_trace()
		if o in ("-m", "--mincut"):
			edges = []
			with open(args[0],"r") as file_to_read:
				input_to_parse = file_to_read.read() ## splitlines
			tab_to_parse = input_to_parse.splitlines()
			for i in range(1, len(tab_to_parse)):
				edges.append(tab_to_parse[i].strip())
			g, source, sink = parseInputFile((edges, tab_to_parse[0].strip()))
			max_flow, gr, flow_list = edmondsKarpAlgorithm(g, source, sink)
			part1, part2 = min_cut(gr, source)
			print_arcs_min_cut(gr.edges(), part1, part2)


		elif o in ("-f", "--maxflow"):
			edges = []
			with open(args[0], "r") as file_to_read:
				input_to_parse = file_to_read.read()  ## splitlines
			tab_to_parse = input_to_parse.splitlines()
			for i in range(1, len(tab_to_parse)):
				edges.append(tab_to_parse[i].strip())
			g, source, sink = parseInputFile((edges, tab_to_parse[0].strip()))

			max_flow, gr, flow_list = edmondsKarpAlgorithm(g, source, sink)
			print(max_flow)
			print_flow_list(flow_list)

		elif o in ("-M", "--mincostmaxflow"):
			edges = []
			with open(args[0], "r") as file_to_read:
				input_to_parse = file_to_read.read()  ## splitlines
			tab_to_parse = input_to_parse.splitlines()
			for i in range(1, len(tab_to_parse)):
				edges.append(tab_to_parse[i].strip())
			g, source, sink = parseInputFile((edges, tab_to_parse[0].strip()))

			flow, cost, flow_list, gr = minCostMaxFlow(g, source, sink)
			print("flow : {}; cost = {}".format(flow, cost))
			print_flow_list(flow_list)



def parseInputFile(file_input):
	"""
	The purpose of this function is to parse the file supplied to stdin
	:param file_input: tuple of
	:return the graph
	"""

	complement_informations = file_input[1].split()
	edges = file_input[0]
	edges_list = []
	for s in edges:
		tab = s.split()
		edges_list.append((tab[0], tab[1], int(tab[2]), int(tab[3])))
	return graphFromList(detect_double_sens(edges_list,complement_informations), True)
def detect_double_sens(E,complement_informations):
	"""

	:param E: array of tuple of edges
	:param complement_informations:
	:return: E,complement_informations
	"""
	array_double_sens = []
	for edge1 in E:
		for edge2 in E:
			if edge1 != edge2 and edge1[0] == edge2[1] and edge1[1] == edge2[0]:
				array_double_sens.append(edge1)

	if array_double_sens != []:
		tamp = []
		tamp.append((array_double_sens[1][0], array_double_sens[1][1]+ "_" + array_double_sens[1][0],
					 array_double_sens[1][2], array_double_sens[1][3]))
		tamp.append((array_double_sens[1][1]+ "_" + array_double_sens[1][0], array_double_sens[1][1],
					 array_double_sens[1][2], 0))
		for e in E:
			if e == array_double_sens[1]:
				E.remove(e)
				E.append(tamp[0])
				E.append(tamp[1])
				break
	return E,complement_informations


def minCostMaxFlow(g,source,sink):
	"""
	this function aim to compute the flow max with the min cost
	:param g:
	:param source:
	:param sink:
	:return: flow : the max_flow, cost, list of flows and the graph modified
	"""
	flow = 0
	cost = 0
	flow_list = {}
	for e in g.edges():
		flow_list[e] = [0]

	while True:
		parent, path_cost = bellmanFordAlgorithm(g, source, sink)

		if path_cost == float('inf'):
			break
		s = sink
		path_flow = float('inf')
		while s != source:
			for e in g.incident_edges(parent[s.value()]):
				if e.endpoints()[1] == s:
					path_flow = min(path_flow, e.value() - e.flow())
					break
			s = parent[s.value()]

		v = sink
		while v != source:
			u = parent[v.value()]
			for e in g.incident_edges(u):
				if e.endpoints()[1] == v:
					e[4] += path_flow
					flow_list[e].append(path_flow)
					break

			for e in g.incident_edges(v):
				if e.endpoints()[1] == u:
					e[4] -= path_flow
					break
			v = u

		flow += path_flow
		cost += path_cost * path_flow


	return flow,cost,flow_list,g
def print_flow_list(flow_list):
	print("Liste de valeurs parcourant chaque arc\n[\n")
	for key,value in flow_list.items():
		if key[2] > 0:
			print("{} : {}\n".format(key,value))
	print("]")

def print_arcs_min_cut(edges, part1, part2):
	edges_tuple = []
	for e in edges:
		if e[2] > 0:
			edges_tuple.append((e.endpoints()[0],e.endpoints()[1]))

	cut_edges = [(u, v) for u, v in edges_tuple if u in part1 and v in part2]
	print("Arêtes de la coupe minimale:")
	for u, v in cut_edges:
		print(f"{u} -> {v}")
def main():
	execute()

if __name__ == "__main__":
    main()
