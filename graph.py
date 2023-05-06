import random


class Graph:
    """
  Representation of a simple graph using an adjacency map.
  This class handles { undirected, directed } x { unweighted, weighted } graphs.
  Vertices can have a weight as in Dijkstra algorithm
	"""

    # ------------------------- nested Vertex class -------------------------
    class Vertex:
        """
	  Lightweight vertex structure for a graph
		"""
        __slots__ = '_tag', '_value'

        def __init__(self, t, x=None):
            """
		  Do not call this constructor directly. Use Graph's insert_vertex(x)
			"""
            self._tag = t
            self._value = x

        def tag(self):
            """
		  Return the tag associated with this vertex
			"""
            return self._tag

        def value(self):
            """
		  Return the value associated with this vertex
			"""
            return self._value

        def setValue(self, val):
            """
		  Set the value of this vertex to val
			"""
            self._value = val

        def __hash__(self):
            return hash(id(self))

        def __str__(self):
            return str(self._tag)

        def __repr__(self):
            return str(self._tag)

        # ------------------ To make the vertices comparable -----------------
        def __lt__(self, e):
            return self._value < e._value

        def __le__(self, e):
            return self._value <= e._value

        def __gt__(self, e):
            return self._value > e._value

        def __ge__(self, e):
            return self._value >= e._value

        def __eq__(self, e):
            return self._value == e._value

        def __ne__(self, e):
            return self._value != e._value

        # ------------------------- nested Edge class -------------------------

    class Edge:
        """
	  Lightweight edge structure for a graph
		"""
        __slots__ = '_origin', '_destination', '_value', '_cost', '_flow'

        def __init__(self, u, v, x, cost=0, flow=0):
            """
		  Do not call constructor directly. Use Graph's insert_edge(u,v,x)
			"""
            self._origin = u
            self._destination = v
            self._value = x
            self._cost = cost
            self._flow = flow

        def endpoints(self):
            """
		  Return (u,v) tuple for vertices u and v
			"""
            return (self._origin, self._destination)

        def opposite(self, v):
            """
		  Return the vertex that is opposite v on this edge
			"""
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v must be a Vertex')
            return self._destination if v is self._origin else self._origin

        def value(self):
            """
		  Return value associated with this edge
			"""
            return self._value

        def cost(self):
            """
            Return the cost associated with this edge
            """
            return self._cost
        def flow(self):
            """
            Return the flow associated with this edge
            """
            return self._flow

        def __hash__(self):
            return hash((self._origin, self._destination))

        def __repr__(self):
            return '({0},{1}){2},{3}'.format(self._origin, self._destination,
                                         self._value if self._value is not None else "", self._cost if self._cost is not None else "")

        def __str__(self):
            return '({0},{1}){2},{3}'.format(self._origin, self._destination,
                                         self._value if self._value is not None else "", self._cost if self._cost is not None else "")

        def __getitem__(self, index):
            """
			this function defines the behavior that we get when we type edge[index]
			edge being an object of Edge class
			:param index:
			"""
            if index == 0:
                return self._origin
            if index == 1:
                return self._destination
            if index == 2:
                return self._value
            if index == 3:
                return self._cost
            if index == 4:
                return self._flow

        def __setitem__(self, index, value):
            """
            this function defines the behavior that we get when we type edge[index]
            edge being an object of Edge class
            :param index:
            """

            if index == 0:
                self._origin = value
            if index == 1:
                self._destination = value
            if index == 2:
                self._value = value
            if index == 3:
                self._cost = value
            if index == 4:
                self._flow = value

        # ------------------ To make the edges comparable -----------------
        def __neg__(self):
            return Graph.Edge(self._origin, self._destination, - self._value)

        def __lt__(self, e):
            return self._value < e._value

        def __le__(self, e):
            return self._value <= e._value

        def __gt__(self, e):
            return self._value > e._value

        def __ge__(self, e):
            return self._value >= e._value

        def __eq__(self, e):
            return self._value == e._value

        def __ne__(self, e):
            return self._value != e._value

    # ------------------------- Graph methods -------------------------
    def __init__(self, directed=False):
        """
	  Create an empty graph (undirected, by default)
	  Graph is directed if optional paramter is set to True.
		"""
        self._outgoing = {}
        # only create second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing

    def _validate_vertex(self, v):
        """
	  Verify that v is a Vertex of this graph
		"""
        if not isinstance(v, self.Vertex):
            raise TypeError('Vertex expected')
        if v not in self._outgoing:
            raise ValueError('Vertex does not belong to this graph.')

    def get_vertex(self, tag):
        """
	  Return the first vertex having the given tag.
	  This is only a convenience method to grab a vertex
	  after the graph has been constructed. You should not
	  use it in graph algorithms.
		"""
        for v in self._outgoing.keys():
            if v.tag() == tag:
                return v
        return None

    def random_vertex(self):
        '''
	  Return a vertex from the graph picked randomly
	  (useful for Prim algorithm)
		'''
        return random.choice(list(self._outgoing.keys()))

    def is_directed(self):
        """
	  Return True if this is a directed graph; False if undirected.
	  Property is based on the original declaration of the graph, not its contents
		"""
        return self._incoming is not self._outgoing  # directed if maps are distinct

    def vertex_count(self):
        """
	  Return the number of vertices in the graph
		"""
        return len(self._outgoing)

    def vertices(self):
        """
	  Return an iteration of all vertices of the graph
		"""
        return self._outgoing.keys()

    def edge_count(self):
        """
	  Return the number of edges in the graph
		"""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        """
	  Return a set of all edges of the graph
		"""
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        """
	  Return the edge from u to v, or None if not adjacent
		"""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """
	  Return number of (outgoing) edges incident to vertex v in the graph.
	  If graph is directed, optional parameter used to count incoming edges
		"""
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def adjacents(self, v):
        """
	  Return an iteration of all adjacents vertices of vertex v
		"""
        return self._outgoing[v].keys()

    def incident_edges(self, v):
        """
	  Return all (outgoing) edges incident to vertex v in the graph.
	  If graph is directed, optional parameter used to request incoming edges
		"""
        self._validate_vertex(v)
        adj = self._outgoing
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, t=None, x=None):
        """
	  Insert and return a new Vertex with tag t and value x
		"""
        v = self.Vertex(t, x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None, cost=None):
        """
	  Insert and return a new Edge from u to v with value x.
	  Raise a ValueError if u and v are not vertices of the graph.
	  Raise a ValueError if u and v are already adjacent
		"""
        if self.get_edge(u, v) is not None:
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, x, cost)
        e_i = self.Edge(v,u,0,cost)
        self._outgoing[u][v] = e
        self._outgoing[v][u] = e_i
        self._incoming[v][u] = e

    def _print_edge(self, e):
        return '{0} -{2},{4}-{3} {1}'.format(e._origin, e._destination, e._value if e._value is not None else "",
                                         ">" if self.is_directed() else "", e._cost if e._cost is not None else "" )

    def __str__(self):
        result = ""
        for u in self._outgoing:
            for v in self._outgoing[u]:
                result += self._print_edge(self._outgoing[u][v]) + "\n"
        return result

    def outgoing(self):
        """
        Return the dictionnary outgoing associated with the graph
        :return:
        """
        return self._outgoing


def graph_from_edgelist(E, directed=False):
    """
  Make a graph instance based on a sequence of edge tuples.
  Edges can be either of from (origin,destination) or
  (origin,destination,value). Vertex set is presume to be those
  incident to at least one edge. Vertex labels are assumed to be hashable
	"""
    g = Graph(directed)
    V = set()
    for e in E:
        V.add(e[0])
        V.add(e[1])

    verts = {}
    i = 0
    for v in V:
        verts[v] = g.insert_vertex(v,i)
        i += 1

    for e in E:
        src = e[0]
        dest = e[1]
        value = e[2]  if len(e) > 2 else None
        cost = e[3]
        g.insert_edge(verts[src], verts[dest], value, cost)

    return g
