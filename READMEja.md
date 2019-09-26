# BiMLPA
[マルチラベル伝搬法を用いた二部ネットワークからのコミュニティ抽出(JSAI 2019)](https://confit.atlas.jp/guide/event-img/jsai2019/4B2-J-3-02/public/pdf?type=in)

二部ネットワークにおける，多対多対応のコミュニティ抽出を行うプログラムです．

## 使い方

```python
import networkx as nx

from bimlpa import *
from community import *
from generator import generate_network
from utils import calc_NMI, relabeling

if __name__ == "__main__":

    # ネットワークを作成します．
    G = generate_network('dataset/southernwomen.net')

    # BiMLPA, BiMLPA_SqrtDeg, BiMLPA_EdgeProbから1つ選び，
    # コミュニティ抽出を実行します．この例では，BiMLPA_SqrtDegを用いて，
    # パラメータを theta=0.3, lambda=7 に設定しています．
    bimlpa = BiMLPA_SqrtDeg(G, 0.3, 7)
    bimlpa.start()

    # BiMLPAを実行すると，伝搬された結果(ラベル)がノードの属性'label'に格納されます．
    print(nx.get_node_attributes(G, 'label'))

    # relabelingを用いると，同じラベル集合をコミュニティとし，番号を振ることができます．
    relabeling(G)
    print(nx.get_node_attributes(G, 'label'))

    # コミュニティ構造がわかっている場合，ノードの属性'community'に正しいコミュニティ番号を振ることで，
    # calc_NMI を用いて， Normalized Mutual Information score を計算することができます．
    community = {i+1: 0 for i in range(9)}
    community.update({i+10: 1 for i in range(9)})
    community.update({i+19: 2 for i in range(6)})
    community.update({i+25: 3 for i in range(3)})
    community.update({i+28: 4 for i in range(5)})
    nx.set_node_attributes(G, name='community', values=community)
    print('NMI : ', calc_NMI(G))

    # ネットワークの可視化も可能です．
    draw_networkx(G)
    # posを指定することもできます．
    pos = nx.spring_layout(G)
    draw_networkx(G, pos)
```
