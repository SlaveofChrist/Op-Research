from graph import Graph
from collections import deque

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
	This the link for seeing the pseudo-code : https://fr.wikipedia.org/wiki/Algorithme_d%27Edmonds-Karp
	:param initial_graph:
	:param residual_graph:
	:return:
	"""
	s = initial_graph.get_vertex("s")
	t = initial_graph.get_vertex("t")
	initial_graph_edges = initial_graph.edges()
	# residual_graph_edges = residual_graph.edges()

	capacities_dict = {}
	residual_capacities_dict = {}

	for e in initial_graph_edges:
		capacities_dict[e[0]] = {}
		residual_capacities_dict[e[0]] = {}

	# for e in residual_graph.edges():

	for e in initial_graph_edges:
		capacities_dict[e[0]][e[1]] = e[2]
		residual_capacities_dict[e[0]][e[1]] = 0

	# for e in residual_graph_edges:
	f = 0
	while True:
		max_flow, parents_dict = bfs(initial_graph,s,t,capacities_dict, residual_capacities_dict)
		if max_flow == 0:
			break
		f += max_flow
		v = t
		while v != s:
			u = parents_dict[v]
			residual_capacities_dict[u][v] += max_flow
			if v not in residual_capacities_dict.keys():
				residual_capacities_dict[v] = {}
				residual_capacities_dict[v][u] = 0
			if residual_capacities_dict[v].get(u) is None:
				residual_capacities_dict[v][u] = 0
			residual_capacities_dict[v][u] -= max_flow
			v = u
	return f,residual_capacities_dict
def bfs(initial_graph,s,t, capacities_dict, residual_capacities_dict):
	parents_dict = {}
	maximal_flow = {}
	for v in initial_graph.vertices():
		parents_dict[v] = None
		maximal_flow[v] = 10000000000
	queue = deque([])
	queue.append(s)
	while len(queue):
		u = queue.popleft()
		for v in initial_graph.adjacents(u):
			if capacities_dict[u][v] - residual_capacities_dict[u][v] > 0 and parents_dict[v] is None:
				parents_dict[v] = u
				maximal_flow[v] = min([maximal_flow[u], capacities_dict[u][v] - residual_capacities_dict[u][v] ])
				if v != t:
					queue.append(v)
				else:
					return maximal_flow[t],parents_dict
	return 0,parents_dict

def main():
	g_initial = Graph(True)
	s = g_initial.insert_vertex("s", 0)
	b = g_initial.insert_vertex("b", 1)
	c = g_initial.insert_vertex("c", 2)
	d = g_initial.insert_vertex("d", 3)
	e = g_initial.insert_vertex("e", 4)
	f = g_initial.insert_vertex("f", 5)
	t = g_initial.insert_vertex("t", 6)

	g_initial.insert_edge(s, d, 3)
	g_initial.insert_edge(s, b, 3)
	g_initial.insert_edge(c, s, 3)
	g_initial.insert_edge(c,d, 1)
	g_initial.insert_edge(c, e, 2)
	g_initial.insert_edge(b, c, 4)
	g_initial.insert_edge(e, b, 1)
	g_initial.insert_edge(e, t, 1)
	g_initial.insert_edge(d, e, 2)
	g_initial.insert_edge(d, f, 6)
	g_initial.insert_edge(f, t, 9)

	flow,residual_graph = edmondsKarpAlgorithm(g_initial)

	print(flow)
	print(residual_graph)

    # g_flow, residual_g = buildResidualGraphAndFlow(0, g_initial)


if __name__ == "__main__":
    main()
