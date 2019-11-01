import unittest
from BiMLPA import *


class BiMLPATestCase(unittest.TestCase):

    def test_bimlpa_SqrtDeg(self):

        g = generate_network('southernwomen.net')
        bimlpa = BiMLPA_SqrtDeg(g, 0.3, 7)
        bimlpa.start()
        relabeling(g)
        top, bottom = output_community(g)
        self.assertIsInstance(top, list)
        self.assertIsInstance(bottom, list)

    def test_bimlpa(self):

        g = generate_network_withName('southernwomen.net')
        bimlpa = BiMLPA(g, 0.3, 7)
        bimlpa.start()
        relabeling(g)
        top, bottom = output_community(g)
        self.assertIsInstance(top, list)
        self.assertIsInstance(bottom, list)

    def test_bimlpa_BiMLPA_EdgeProb(self):
        g = generate_network('southernwomen.net')
        bimlpa = BiMLPA_EdgeProb(g, 0.3, 7)
        bimlpa.start()
        relabeling(g)
        top, bottom = output_community(g)
        self.assertIsInstance(top, list)
        self.assertIsInstance(bottom, list)


if __name__ == '__main__':
    unittest.main()
