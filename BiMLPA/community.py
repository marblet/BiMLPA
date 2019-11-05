import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt


def draw_community(G, pos=None):
    if pos is None:
        top = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}
        bottom = set(G) - top
        bottom = list(bottom)
        bottom.sort()

        c = Counter(nx.get_node_attributes(G, 'label').values())
        num_of_label = max(nx.get_node_attributes(G, 'label').values()) + 1

        pos = dict()
        pos_label = [0] * num_of_label
        for i in range(1, num_of_label):
            pos_label[i] = pos_label[i-1] + c[i-1]
        for v in top:
            label = G.nodes[v]['label']
            pos[v] = (label + pos_label[label], 1)
            pos_label[label] += 1
        pos_label = [0] * num_of_label
        for i in range(1, num_of_label):
            pos_label[i] = pos_label[i-1] + c[i-1]
        for v in bottom:
            label = G.nodes[v]['label']
            pos[v] = (label + pos_label[label], 0)
            pos_label[label] += 1

    color = [d['label'] for node, d in G.nodes(data=True)]

    nx.draw_networkx(G, pos, node_color=color)
    plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.tick_params(length=0)

    plt.show()


def number_of_communities(G):
    c_top = Counter([d['label'] for n, d in G.nodes(data=True) if d['bipartite'] == 0])
    c_bottom = Counter([d['label'] for n, d in G.nodes(data=True) if d['bipartite'] == 1])
    return len(c_top), len(c_bottom)
