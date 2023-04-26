# from graph import Graph
#
# g_initial = Graph(True)
# s = g_initial.insert_vertex("s",0)
# u = g_initial.insert_vertex("u",1)
# v = g_initial.insert_vertex("v",2)
# t = g_initial.insert_vertex("t",3)
#
# g_initial.insert_edge(s,u,4)
# g_initial.insert_edge(s,v,2)
# g_initial.insert_edge(u,v,3)
# g_initial.insert_edge(v,t,6)
# g_initial.insert_edge(u,t,1)
#
# print(g_initial._outgoing.values())
test = {}
test['a'] = {}
test['b'] = {}
test ['c'] = {}

test ['a']['d'] = 1
test ['b']['e'] = 2
test ['c']['f'] = 3

cap = []
cap[0][0] = 2


# for k,v in test.items():
#     for val1,val2 in v.items():
#         print("la valeur de la cle {} est : {} qui contient lui même comme valeur : {} ".format(k,val1,val2))

visited = {node : False for node in test}
print(visited)
print(min(float("Inf"),1))
print(cap)