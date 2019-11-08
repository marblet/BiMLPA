from collections import defaultdict, Counter
from itertools import combinations


# calculate the modularity based on labels assigned each node
def guimera_modularity(G):
    top = {v: d for v, d in G.nodes(data=True) if d['bipartite'] == 0}
    bottom = {v: d for v, d in G.nodes(data=True) if d['bipartite'] == 1}
    top_coms = defaultdict(set)
    bottom_coms = defaultdict(set)
    for v, d in top.items():
        top_coms[d['label']].add(v)
    for v, d in bottom.items():
        bottom_coms[d['label']].add(v)

    node2degree = dict(G.degree())
    E = G.number_of_edges()
    Q_top = 0
    Q_bottom = 0
    Mb = 0
    for v in bottom:
        Mb += node2degree[v] * (node2degree[v] - 1)
    for _, nodes in top_coms.items():
        for pair in combinations(nodes, 2):
            i, j = pair
            tmpQ = len(set(G.neighbors(i)) & set(G.neighbors(j))) / Mb
            tmpQ -= node2degree[i] * node2degree[j] / (E * E)
            Q_top += tmpQ

    Mt = 0
    for v in top:
        Mt += node2degree[v] * (node2degree[v] - 1)
    for _, nodes in bottom_coms.items():
        for pair in combinations(nodes, 2):
            i, j = pair
            tmpQ = len(set(G.neighbors(i)) & set(G.neighbors(j))) / Mt
            tmpQ -= node2degree[i] * node2degree[j] / (E * E)
            Q_bottom += tmpQ

    return Q_top*2, Q_bottom*2


def murata_modularity(G):
    top = {v: d for v, d in G.nodes(data=True) if d['bipartite'] == 0}
    bottom = {v: d for v, d in G.nodes(data=True) if d['bipartite'] == 1}
    top_coms = defaultdict(set)
    bottom_coms = defaultdict(set)

    for v, d in top.items():
        top_coms[d['label']].add(v)
    for v, d in bottom.items():
        bottom_coms[d['label']].add(v)

    topC_to_bottomC = dict()
    topC_to_V = dict()
    bottomC_to_topC = dict()
    bottomC_to_V = dict()

    for c, v in top_coms.items():
        c_count = Counter()
        for u in v:
            for neig in G.neighbors(u):
                c_count.update({G.nodes[neig]['label']: 1})
        topC_to_bottomC[c] = c_count
        topC_to_V[c] = sum(c_count.values())
    for c, v in bottom_coms.items():
        c_count = Counter()
        for u in v:
            for neig in G.neighbors(u):
                c_count.update({G.nodes[neig]['label']: 1})
        bottomC_to_topC[c] = c_count
        bottomC_to_V[c] = sum(c_count.values())

    E = G.number_of_edges()
    Q_top = 0
    Q_bottom = 0
    # top -> bottom
    for Ck, coms in topC_to_bottomC.items():
        Cl = max(coms, key=coms.get)
        Q_top += (coms[Cl] / (2 * E) - topC_to_V[Ck] * bottomC_to_V[Cl] / (4 * E * E))
    # bottom -> top
    for Ck, coms in bottomC_to_topC.items():
        Cl = max(coms, key=coms.get)
        Q_bottom += (coms[Cl] / (2 * E) - bottomC_to_V[Ck] * topC_to_V[Cl] / (4 * E * E))
    return Q_top + Q_bottom


def suzuki_modularity(G):
    top = {v: d for v, d in G.nodes(data=True) if d['bipartite'] == 0}
    bottom = {v: d for v, d in G.nodes(data=True) if d['bipartite'] == 1}
    top_coms = defaultdict(set)
    bottom_coms = defaultdict(set)

    for v, d in top.items():
        top_coms[d['label']].add(v)
    for v, d in bottom.items():
        bottom_coms[d['label']].add(v)

    topC_to_bottomC = dict()
    topC_to_V = dict()
    bottomC_to_topC = dict()
    bottomC_to_V = dict()

    for c, v in top_coms.items():
        c_count = Counter()
        for u in v:
            for neig in G.neighbors(u):
                c_count.update({G.nodes[neig]['label']: 1})
        topC_to_bottomC[c] = c_count
        topC_to_V[c] = sum(c_count.values())
    for c, v in bottom_coms.items():
        c_count = Counter()
        for u in v:
            for neig in G.neighbors(u):
                c_count.update({G.nodes[neig]['label']: 1})
        bottomC_to_topC[c] = c_count
        bottomC_to_V[c] = sum(c_count.values())

    E = G.number_of_edges()
    Q_top = 0
    Q_bottom = 0
    # top -> bottom
    for Ck, coms in topC_to_bottomC.items():
        Ck_to_V = topC_to_V[Ck]
        for Cl, cnt in coms.items():
            tmpQ = cnt/E - Ck_to_V * bottomC_to_V[Cl] / (E*E)
            tmpQ *= (cnt / Ck_to_V)
            Q_top += tmpQ
    # bottom -> top
    for Ck, coms in bottomC_to_topC.items():
        Ck_to_V = bottomC_to_V[Ck]
        for Cl, cnt in coms.items():
            tmpQ = cnt/E - Ck_to_V * topC_to_V[Cl]/(E*E)
            tmpQ *= (cnt / Ck_to_V)
            Q_bottom += tmpQ
    Q = (Q_top + Q_bottom) / 2
    return Q
