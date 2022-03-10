import json
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
i = 1
with open("data/graph-UFRGS-PPGC-2017-2020.json", "r") as fp:
    graph = json.load(fp)
    for node in graph["nodes"]:
        G.add_node(node["id"])
        #G.nodes

    for edge in graph["links"]:
        G.add_edge(edge["source"], edge["target"], value=edge["value"])

print(nx.info(G))
print("Density:", nx.density(G))

#dc = nx.degree_centrality(G)
#for n in sorted(dc, key=dc.get):
#    print(n, ":", dc[n])

#cc = nx.closeness_centrality(G)
#for n in sorted(cc, key=cc.get):
#    print(n, ":", cc[n])

#bc = nx.betweenness_centrality(G)
#for n in sorted(bc, key=bc.get):
#    print(n, ":", bc[n])

#ec = nx.eigenvector_centrality(G)
#for n in sorted(ec, key=ec.get):
#    print(n, ":", ec[n])

with open("data/graph-UFRGS-PPGC-2017-2020-export.json", "w") as fp:
    json.dump(nx.node_link_data(G), fp, indent=2)

# #Color nodes and visualize network
# plt.figure(1)
# #Simple 1-line code: nx.draw_networkx(G)
# color_map = []
# size_map = []
# for i in G.nodes:
#     size_map.append(G.nodes[i]['size']*3)
#     if G.nodes[i]['group_id'] == 1:
#         color_map.append('red')
#     elif G.nodes[i]['group_id'] == 2:
#         color_map.append('blue')
#     else:
#         color_map.append('green')

#nx.draw_networkx(G, 
#        node_color=color_map, 
#        node_size=size_map, 
#        pos=nx.spring_layout(G, iterations=100, weight="value", k=1/math.sqrt(len(G.nodes)/5)), 
#        arrows=False, with_labels=False)
#plt.show()
