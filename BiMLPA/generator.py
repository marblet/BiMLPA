import networkx as nx


def generate_network(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    u_list = []
    v_list = []
    for l in lines:
        u, v = list(map(int, l.split()))
        u_list.append(u)
        v_list.append(v)
    u_max = max(u_list)
    v_min = min(v_list)
    if u_max < v_min:
        padding = 0
    elif v_min == 0:
        padding = u_max + 1
    else:
        padding = u_max

    G = nx.Graph()
    u_set = list(set(u_list))
    v_set = list(map(lambda x: x+padding, set(v_list)))

    G.add_nodes_from(u_set, bipartite=0)
    G.add_nodes_from(v_set, bipartite=1)

    for i in range(len(u_list)):
        G.add_edge(u_list[i], v_list[i]+padding)
    return G


def generate_network_with_name(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    u_list = []
    v_list = []
    for l in lines:
        l = l[:-1]
        u, v = l.split('\t')
        u_list.append(u)
        v_list.append(v)

    G = nx.Graph()
    u_set = list(set(u_list))
    v_set = list(set(v_list))

    G.add_nodes_from(u_set, bipartite=0)
    G.add_nodes_from(v_set, bipartite=1)

    for i in range(len(u_list)):
        G.add_edge(u_list[i], v_list[i])
    return G
