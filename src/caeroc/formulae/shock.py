import numpy as np

try:
    from .._skaero.gasdynamics.shocks import _ShockClass
except ImportError:
    from skaero.gasdynamics.shocks import _ShockClass

from ..logger import logger
from ..util.decorators import storeresult
from .base import FormulaeBase


class NormalShock(FormulaeBase, _ShockClass):
    """Normal shock relations"""

    def __init__(self, **kwargs):
        if "gamma" in kwargs:
            self.gamma = kwargs["gamma"]
        else:
            self.gamma = kwargs["gamma"] = 1.4

        if "M_1" not in kwargs:
            self.M_1 = kwargs["M_1"] = self.get_M_1(**kwargs)

        if "beta" not in kwargs:
            # Strong shock solution
            kwargs["beta"] = np.pi / 2

        self.keys = [
            "M_1",
            "M_2",
            "p2_p1",
            "rho2_rho1",
            "T2_T1",
            "p02_p01",
            "rho02_rho01",
            "T02_T01",
        ]

        super().__init__(**kwargs)

    def get_M_1(
        self,
        M_2=None,
        p2_p1=None,
        rho2_rho1=None,
        T2_T1=None,
        p02_p01=None,
        p2_p01=None,
        **kwargs,
    ):
        """
        Computes Mach number when one of the arguments are specified

        """
        try:
            g = self.gamma
        except KeyError:
            g = kwargs["gamma"]

        if p2_p1 is not None:
            M_1 = np.sqrt((p2_p1 - 1) * (g + 1.0) / 2.0 / g + 1.0)
        elif rho2_rho1 is not None:
            M_1 = np.sqrt(2.0 * rho2_rho1 / (g + 1.0 - rho2_rho1 * (g - 1.0)))
        elif T2_T1 is not None:
            a = 2.0 * g * (g - 1.0)
            b = 4.0 * g - (g - 1.0) * (g - 1.0) - T2_T1 * (g + 1.0) * (g + 1.0)
            c = -2.0 * (g - 1.0)
            M_1, M_11 = np.roots([a, b, c])
        elif p02_p01 is not None:
            raise NotImplementedError
        elif p2_p01 is not None:
            raise NotImplementedError
        elif "M" in kwargs.keys():
            return kwargs["M"]
        else:
            logger.error("Insufficient data to calculate Mach number")

        return M_1

    def calculate(
        self,
        M_1=None,
        M_2=None,
        p2_p1=None,
        rho2_rho1=None,
        T2_T1=None,
        p02_p01=None,
        rho02_rho01=None,
        T02_T01=None,
    ):
        """
        Calculate all possible data and store
        using keywords and values in the dictionary `data`.

        Parameters
        ----------
        theta_deg or theta_rad : float
            Turn angle or deflection angle, optional but specify one.

        M_1: float
            Mach number of inflow

        """
        if M_1 is not None:
            self.M_1 = M_1
        elif any([v is not None for v in (p2_p1, rho2_rho1, T2_T1)]):
            self.M_1 = self.get_M_1(p2_p1, rho2_rho1, T2_T1)
        else:
            logger.error(
                "Insufficient data: M_1 or p2_p1 or rho2_rho1 "
                "or T2_T1 must be specified."
            )

        super().__init__(M_1=self.M_1, beta=np.pi / 2, gamma=self.gamma)
        for key in self.keys:
            self.store(key, getattr(self, key))

        return self.data


class ObliqueShock(NormalShock):
    def __init__(self, gamma=1.4):
        self.keys = [
            "M_1",
            "M_2",
            "M_1n",
            "M_2n",
            "theta",
            "p2_p1",
            "rho2_rho1",
            "T2_T1",
        ]
        self.gamma = gamma

    def beta(self, m1, d, g=1.4, i=0):
        p = -(m1 * m1 + 2.0) / m1 / m1 - g * np.sin(d) * np.sin(d)
        q = (2.0 * m1 * m1 + 1.0) / np.pow(m1, 4.0) + (
            (g + 1.0) * (g + 1.0) / 4.0 + (g - 1.0) / m1 / m1
        ) * np.sin(d) * np.sin(d)
        r = -np.cos(d) * np.cos(d) / np.pow(m1, 4.0)

        a = (3.0 * q - p * p) / 3.0
        b = (2.0 * p * p * p - 9.0 * p * q + 27.0 * r) / 27.0

        test = b * b / 4.0 + a * a * a / 27.0

        if test > 0.0:
            return -1.0
        elif test == 0.0:
            x1 = np.sqrt(-a / 3.0)
            x2 = x1
            x3 = 2.0 * x1
            if b > 0.0:
                x1 *= -1.0
                x2 *= -1.0
                x3 *= -1.0

        if test < 0.0:
            phi = np.acos(np.sqrt(-27.0 * b * b / 4.0 / a / a / a))
            x1 = 2.0 * np.sqrt(-a / 3.0) * np.cos(phi / 3.0)
            x2 = 2.0 * np.sqrt(-a / 3.0) * np.cos(phi / 3.0 + np.pi * 2.0 / 3.0)
            x3 = 2.0 * np.sqrt(-a / 3.0) * np.cos(phi / 3.0 + np.pi * 4.0 / 3.0)
            if b > 0.0:
                x1 *= -1.0
                x2 *= -1.0
                x3 *= -1.0

        s1 = x1 - p / 3.0
        s2 = x2 - p / 3.0
        s3 = x3 - p / 3.0

        if s1 < s2 and s1 < s3:
            t1 = s2
            t2 = s3
        elif s2 < s1 and s2 < s3:
            t1 = s1
            t2 = s3
        else:
            t1 = s1
            t2 = s2

        b1 = np.asin(np.sqrt(t1))
        b2 = np.asin(np.sqrt(t2))

        betas = b1
        betaw = b2
        if b2 > b1:
            betas = b2
            betaw = b1

        if i == 0:
            return betaw
        if i == 1:
            return betas

    def mach1n_mach2n(self, M1, beta, gamma=1.4):
        M1n = M1 * np.sin(beta)
        M2n = np.sqrt(
            (1.0 + 0.5 * (gamma - 1.0) * M1n**2)
            / (gamma * M1n**2 - 0.5 * (gamma - 1.0))
        )
        return M1n, M2n

    def mach2(self, M1, theta, gamma=1.4):
        beta = self.beta(M1, theta)
        M1n, M2n = self.M1nM2n(M1, beta, gamma)
        M2 = M2n / np.sin(beta - theta)
        return M2

    def p2_p1(self, M1, theta, gamma=1.4):
        beta = self.beta(M1, theta)
        M1n = M1 * np.sin(beta)
        p2_p1 = 1.0 + 2.0 * gamma / (gamma + 1.0) * (M1n**2 - 1.0)
        return p2_p1
