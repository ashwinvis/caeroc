import unittest

import numpy as np

import caeroc.formulae as fml


class TestIsentropic(unittest.TestCase):

    def setUp(self):
        self.mode = fml.isentropic.Isentropic(1.5)

    def test_basic(self):
        """Test all class methods in Isentropic class"""
        isen = self.mode
        isen.Mt(M=0.5)
        isen.rho_rho0(M=0.5, store=True)
        isen.p_pt(M=0.5, store=False)
        isen.calculate(A_Astar=2.0)

    def test_calculate(self):
        isen = self.mode
        isen.calculate(M=2)
        self.assertAlmostEqual(isen.data["p_p0"][0], 0.125)
        self.assertAlmostEqual(isen.data["rho_rho0"][0], 0.25)
        self.assertAlmostEqual(isen.data["p_pt"][0], 0.24414062)
        self.assertAlmostEqual(isen.data["rho_rhot"][0], 0.390625)
        self.assertAlmostEqual(isen.data["A_Astar"][0], 1.61908616)

    def test_calculate_array_like(self):
        x = np.linspace(0, 5, 500, endpoint=True)
        self.mode.calculate(M=x)


if __name__ == "main":
    unittest.main()
