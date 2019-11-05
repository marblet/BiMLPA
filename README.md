# BiMLPA

This is the implementation of BiMLPA.
BiMLPA is to detect the many-to-many correspondence community in bipartite networks using multi-label propagation algorithm.
日本語版READMEは[こちら](https://github.com/hbkt/BiMLPA/blob/master/READMEja.md)

## Installation 

In order to install the package just download (or clone) the current project and copy the demon folder in the root of your application.

Alternatively use pip:
```bash
sudo pip install bimlpa
```

If you like to install the latest version of the package from the repository use:
```bash
sudo pip install git+https://github.com/hbkt/BiMLPA
```


## Usage

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
