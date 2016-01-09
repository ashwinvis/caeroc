import unittest
import caeroc.formulae as fml

class TestFormulae(unittest.TestCase):

    def test_isentropic(self):
        """Test all class methods in Isentropic class"""
        isen = fml.isentropic.Isentropic(1.4)
        isen.calculate(rho_rho0=0.5)
        # isen.calculate(A_Astar=2.)
        isen.calculate(M=2)

if __name__ == 'main':
    unittest.main()

