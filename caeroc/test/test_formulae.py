import unittest
import caeroc.formulae as fml


class TestFormulae(unittest.TestCase):

    def test_isentropic_functions(self):
        """Test all class methods in Isentropic class"""
        isen = fml.isentropic.Isentropic(1.4)
        isen.Mt(M=0.5)
        isen.rho_rho0(M=0.5, store=True)
        isen.p_pt(M=0.5, store=False)
        isen.calculate(A_Astar=2.)

    def test_isentropic_calculate(self):
        isen = fml.isentropic.Isentropic(1.5)
        isen.calculate(M=2)
        self.assertAlmostEqual(isen.data['p_p0'][0], 0.125)
        self.assertAlmostEqual(isen.data['rho_rho0'][0], 0.25)
        self.assertAlmostEqual(isen.data['p_pt'][0], 0.24414062)
        self.assertAlmostEqual(isen.data['rho_rhot'][0], 0.390625)
        self.assertAlmostEqual(isen.data['A_Astar'][0], 1.61908616)


if __name__ == 'main':
    unittest.main()
