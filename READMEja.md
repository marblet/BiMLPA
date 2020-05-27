# BiMLPA
"BiMLPA: Community Detection in Bipartite Networks by Multi-Label Propagation", NetSci-X 2020 https://link.springer.com/chapter/10.1007/978-3-030-38965-9_2

[マルチラベル伝搬法を用いた二部ネットワークからのコミュニティ抽出(JSAI 2019)](https://confit.atlas.jp/guide/event-img/jsai2019/4B2-J-3-02/public/pdf?type=in)

二部ネットワークにおける，多対多対応のコミュニティ抽出を行うプログラムです．

## インストール 

pip経由でインストールする場合:
```bash
sudo pip install bimlpa
```

レポジトリからlatest versionをインストールしたい場合:
```bash
sudo pip install git+https://github.com/marblet/BiMLPA
```

## 使い方

```python
from BiMLPA import *
import networkx as nx

G = generate_network('BiMLPA/test/southernwomen.net')

# The parameters are set to theta=0.3, lambda=7
bimlpa = BiMLPA_SqrtDeg(G, 0.3, 7)
bimlpa.start()
relabeling(G)
top_coms, bottom_coms = output_community(G)

# If the community structure is known, the normalized mutual information score can be calculated
# using calc_NMI by assigning the correct community number to the attribute 'community' of the node.
community = {i+1: 0 for i in range(9)}
community.update({i+10: 1 for i in range(9)})
community.update({i+19: 2 for i in range(6)})
community.update({i+25: 3 for i in range(3)})
community.update({i+28: 4 for i in range(5)})
nx.set_node_attributes(G, name='community', values=community)

print('NMI : ', calc_NMI(G))
```
