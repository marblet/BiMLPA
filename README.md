# BiMLPA

This is the implementation of BiMLPA.
BiMLPA is to detect the many-to-many correspondence community in bipartite networks using multi-label propagation algorithm.
日本語版READMEは[こちら](https://github.com/hbkt/BiMLPA/blob/master/READMEja.md)

## Usage

```python
import networkx as nx

from bimlpa import *
from community import *
from generator import generate_network
from utils import calc_NMI, relabeling

if __name__ == "__main__":

    # You can generate the network from the adjacency list format file
    G = generate_network('dataset/southernwomen.net')

    # The parameters are set to theta=0.3, lambda=7
    bimlpa = BiMLPA_SqrtDeg(G, 0.3, 7)
    bimlpa.start()

    # After BiMLPA is executed, the propagated result (label) is stored in the node attribute 'label'.
    print(nx.get_node_attributes(G, 'label'))

    # You can assign the unique community identifier using relabeling
    relabeling(G)
    print(nx.get_node_attributes(G, 'label'))

    # If the community structure is known, the normalized mutual information score can be calculated
    # using calc_NMI by assigning the correct community number to the attribute 'community' of the node.
    community = {i+1: 0 for i in range(9)}
    community.update({i+10: 1 for i in range(9)})
    community.update({i+19: 2 for i in range(6)})
    community.update({i+25: 3 for i in range(3)})
    community.update({i+28: 4 for i in range(5)})
    nx.set_node_attributes(G, name='community', values=community)
    print('NMI : ', calc_NMI(G))

    # You can draw the network
    pos = nx.spring_layout(G)
    draw_networkx(G, pos)
```
