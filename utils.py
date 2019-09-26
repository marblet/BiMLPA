import networkx as nx
from sklearn.metrics import normalized_mutual_info_score as NMI
from community import draw_community, number_of_communities


def relabeling(G):
    node2label = nx.get_node_attributes(G, 'label')
    labels = [list(l.keys()) for l in node2label.values()]
    for l in labels:
        l.sort()
    labels = list(map(str, labels))
    labels_set = set(labels)
    labels_dict = dict({s: i for i, s in enumerate(labels_set, start=1)})

    new_labels = {v: labels_dict[labels[i]] for i, v in enumerate(node2label)}
    nx.set_node_attributes(G, new_labels, 'label')


def calc_NMI(G):
    # top と bottom 両方を計算して返す
    top = {n: d for n, d in G.nodes(data=True) if d['bipartite'] == 0}
    bottom = {n: d for n, d in G.nodes(data=True) if d['bipartite'] == 1}
    pred_top  = []
    truth_top = []
    for n, d in top.items():
        pred_top.append(d['label'])
        truth_top.append(d['community'])
    pred_bottom  = []
    truth_bottom = []
    for n, d in bottom.items():
        pred_bottom.append(d['label'])
        truth_bottom.append(d['community'])
    return NMI(truth_top, pred_top), NMI(truth_bottom, pred_bottom)


def output_community(G, filename):
    top = {n: d['label'] for n, d in G.nodes(data=True) if d['bipartite']==0}
    bottom = {n: d['label'] for n, d in G.nodes(data=True) if d['bipartite']==1}

    top_max = max(top.values())
    bottom_max = max(bottom.values())

    top_com_list = [[] for _ in range(top_max)]
    for k, v in top.items():
        top_com_list[v-1].append(k)
    top_com_list = [str(com)[1:-1]+'\n' for com in top_com_list if len(com)>0]

    bottom_com_list = [[] for _ in range(bottom_max)]
    for k, v in bottom.items():
        bottom_com_list[v-1].append(k)
    bottom_com_list = [str(com)[1:-1]+'\n' for com in bottom_com_list if len(com)>0]
    with open(filename, 'w') as f:
        f.writelines(top_com_list)
        f.writelines(bottom_com_list)
