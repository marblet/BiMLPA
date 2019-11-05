import networkx as nx
import numpy as np

from collections import Counter
from math import sqrt
from random import choice


class BiMLPA(object):
    def __init__(self, G, threshold, max_prop_label, max_MM_iter=100, max_MS_iter=100):
        self.G = G
        self.threshold = threshold
        self.max_prop_label = max_prop_label
        self.max_MM_iter = max_MM_iter
        self.max_MS_iter = max_MS_iter

    def _initialize(self):
        G = self.G
        top = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}
        bottom = set(G) - top
        if len(top) >= len(bottom):
            self.red = top
            self.blue = bottom
        else:
            self.red = bottom
            self.blue = top
        for i, v in enumerate(self.red):
            G.nodes[v]['label'] = {i+1: 1}
        for v in self.blue:
            G.nodes[v]['label'] = {}

    def _label_to_list(self, propagaters):
        # propagaterが持つラベル数をmax_prop_label以下に
        # ラベルの重みの降順でソート
        node2label  = dict(nx.get_node_attributes(self.G, 'label'))
        for node in propagaters:
            label = node2label[node]
            l = list(label.keys())
            r = list(label.values())
            if len(label) > self.max_prop_label:
                index = np.argsort(r)[::-1][:self.max_prop_label]
                new_label = [[l[i] for i in index], [r[j] for j in index]]
            else:
                new_label = [l, r]
            node2label[node] = new_label
        return node2label

    def _sum_label_ratio(self, label_freq, u, node2label):
        neighbor = self.G.neighbors(u)
        for v in neighbor:
            label_index, label_ratio = node2label[v]
            for i in range(len(label_index)):
                label_freq.update({label_index[i]: label_ratio[i]})

    def _propagate_multi_labels(self, receivers):
        G = self.G
        convergence = True
        propagaters = set(G) - set(receivers)
        node2label  = self._label_to_list(propagaters)

        # 各ノード、neighborからラベルを取得しthresholdを超えたラベルのみ取得
        for u in receivers:
            old_label = node2label[u]
            label_freq = Counter()
            self._sum_label_ratio(label_freq, u, node2label)

            freq_max = max(label_freq.values())
            new_labels = {label: freq for label, freq in label_freq.items() if freq/freq_max >= self.threshold}
            freq_sum = sum(new_labels.values())
            new_labels = {label: new_labels[label]/freq_sum for label in new_labels}
            G.nodes[u]['label'] = new_labels
            if convergence and (old_label.keys() != new_labels.keys()):
                convergence = False
        return convergence

    def _propagate_single_label(self, receivers):
        G = self.G
        convergence = True
        propagaters = set(G) - set(receivers)
        node2label  = self._label_to_list(propagaters)

        for u in receivers:
            old_label = node2label[u]
            label_freq = Counter()
            self._sum_label_ratio(label_freq, u, node2label)

            freq_max = max(label_freq.values())
            candidate = [label for label, freq in label_freq.items() if freq == freq_max]
            new_label = {choice(candidate): 1}
            G.nodes[u]['label'] = new_label
            if convergence and old_label != new_label:
                convergence = False
        return convergence

    def _multi_multi_LP(self):
        # Multi Multi LP
        for _ in range(self.max_MM_iter):
            conv_blue = self._propagate_multi_labels(self.blue)
            conv_red  = self._propagate_multi_labels(self.red)
            if conv_blue and conv_red:
                break

    def _multi_single_LP(self):
        # Multi Single LP
        for _ in range(self.max_MS_iter):
            conv_blue = self._propagate_multi_labels(self.blue)
            conv_red  = self._propagate_single_label(self.red)
            if conv_blue and conv_red:
                break

    def start(self):
        self._initialize()
        self._multi_multi_LP()
        self._multi_single_LP()


class BiMLPA_SqrtDeg(BiMLPA):
    def __init__(self, G, threshold, max_prop_label, max_MM_iter=100, max_MS_iter=100):
        super().__init__(G, threshold, max_prop_label, max_MM_iter, max_MS_iter)
        self.node2degree = dict(G.degree())

    def _label_to_list(self, propagaters):
        node2label  = dict(nx.get_node_attributes(self.G, 'label'))
        for node in propagaters:
            d_sqrt = sqrt(self.node2degree[node])
            label = node2label[node]
            l = list(label.keys())
            r = list(label.values())
            if len(label) > self.max_prop_label:
                index = np.argsort(r)[::-1][:self.max_prop_label]
                new_label = [[l[i] for i in index], [r[j]/d_sqrt for j in index]]
            else:
                r = [ratio/d_sqrt for ratio in r]
                new_label = [l, r]
            node2label[node] = new_label
        return node2label


class BiMLPA_EdgeProb(BiMLPA):
    def __init__(self, G, threshold, max_prop_label, max_MM_iter=100, max_MS_iter=100):
        super().__init__(G, threshold, max_prop_label, max_MM_iter, max_MS_iter)
        self.node2degree = dict(G.degree())
        self.M = G.number_of_edges()

    def _sum_label_ratio(self, label_freq, u, node2label):
        neighbor = self.G.neighbors(u)
        d_u = self.node2degree[u]
        for v in neighbor:
            label_index, label_ratio = node2label[v]
            d_v = self.node2degree[v]
            for i in range(len(label_index)):
                label_freq.update({label_index[i]: label_ratio[i]*(1-d_u*d_v/self.M)})
