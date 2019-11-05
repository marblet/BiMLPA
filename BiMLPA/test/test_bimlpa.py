import unittest
from BiMLPA import *


class BiMLPATestCase(unittest.TestCase):

    def test_bimlpa_SqrtDeg(self):

        G = generate_network('southernwomen.net')
        bimlpa = BiMLPA_SqrtDeg(G, 0.3, 7)
        bimlpa.start()
        relabeling(G)
        top, bottom = output_community(G)
        self.assertIsInstance(top, list)
        self.assertIsInstance(bottom, list)

    def test_bimlpa(self):

        G = generate_network_withName('southernwomen.net')
        bimlpa = BiMLPA(G, 0.3, 7)
        bimlpa.start()
        relabeling(G)
        top, bottom = output_community(G)
        self.assertIsInstance(top, list)
        self.assertIsInstance(bottom, list)

    def test_bimlpa_BiMLPA_EdgeProb(self):
        G = generate_network('southernwomen.net')
        bimlpa = BiMLPA_EdgeProb(G, 0.3, 7)
        bimlpa.start()
        relabeling(G)
        top, bottom = output_community(G)
        self.assertIsInstance(top, list)
        self.assertIsInstance(bottom, list)


if __name__ == '__main__':
    unittest.main()
