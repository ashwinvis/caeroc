import numpy as np
from skaero.gasdynamics.isentropic import (IsentropicFlow, PrandtlMeyerExpansion,
                                           mach_from_area_ratio, mach_from_nu)
from ..util.decorators import storeresult
from ..logger import logger
from .base import FormulaeBase


class Isentropic(FormulaeBase, IsentropicFlow):
    """Isentropic flow relations for quasi 1D flows"""

    def __init__(self, gamma=1.4):
        self.keys = ['M', 'p_p0', 'rho_rho0', 'T_T0',
                     'Mt', 'p_pt', 'rho_rhot', 'T_Tt', 'A_Astar']
        super(Isentropic, self).__init__(gamma=gamma)

    @storeresult
    def p_p0(self, M, *args, **kwargs):
        """
        Parameters
        ----------
        M : array_like
            Mach number.
        store : bool
            If set as true stores the result in self.data. Optional.

        Notes
        -------
        .. math::
           \dfrac{p}{p_0} = \dfrac{T}{T_0} ^ (\gamma / (\gamma - 1))

        """
        return super(Isentropic, self).p_p0(M)

    @storeresult
    def rho_rho0(self, M, *args, **kwargs):
        """
        Parameters
        ----------
        M : array_like
            Mach number.
        store : bool
            If set as true stores the result in self.data. Optional.

        Notes
        -------
        ..  math::
            \dfrac{\rho}{\rho_0} = \dfrac{T}{T_0} ^ (1 / (\gamma - 1))

        """
        return super(Isentropic, self).rho_rho0(M)

    @storeresult
    def T_T0(self, M, *args, **kwargs):
        """
        Parameters
        ----------
        M : array_like
            Mach number.
        store : bool
            If set as true stores the result in self.data. Optional.

        Notes
        -------
        ..  math::
            \dfrac{T}{T_0} = (1+(\gamma-1)/2 * M^2) ^ {-1}

        """
        return super(Isentropic, self).T_T0(M)

    @storeresult
    def Mt(self, M, *args, **kwargs):
        """
        Parameters
        ----------
        M : array_like
            Mach number.
        store : bool
            If set as true stores the result in self.data. Optional.

        Notes
        -------
        ..  math::
            M^* = ((\gamma + 1)/(\gamma - 1) * (1./M^2/(\gamma -1) + 0.5))^(-0.5)

        """
        return ((self.gamma + 1) / (self.gamma - 1) *
                (1. / M ** 2 / (self.gamma -1) + 0.5)) ** (-0.5)

    @storeresult
    def p_pt(self, M, *args, **kwargs):
        """
        Parameters
        ----------
        M : array_like
            Mach number.
        store : bool
            If set as true stores the result in self.data. Optional.

        """
        g = self.gamma
        return super(Isentropic, self).p_p0(M) * np.power((g / 2. + .5),
                                                          g / (g - 1.))

    @storeresult
    def rho_rhot(self, M, *args, **kwargs):
        """
        Parameters
        ----------
        M : array_like
            Mach number.
        store : bool
            If set as true stores the result in self.data. Optional.

        """
        g = self.gamma
        return super(Isentropic, self).rho_rho0(M) * np.power((g /2. + .5),
                                                              1. / (g - 1.))

    @storeresult
    def T_Tt(self, M, *args, **kwargs):
        """
        Parameters
        ----------
        M : array_like
            Mach number.
        store : bool
            If set as true stores the result in self.data. Optional.

        """
        g = self.gamma
        return super(Isentropic, self).T_T0(M) * (g / 2. + .5)

    @storeresult
    def A_Astar(self, M, *args, **kwargs):
        """
        Parameters
        ----------
        M : array_like
            Mach number.
        store : bool
            If set as true stores the result in self.data. Optional.

        Notes
        ------
        .. math::
           \dfrac{A}{A^*} = \dfrac{1}{M}
                            \sqrt{\dfrac{2}{(gamma+1} / \dfrac{T}{T_0}(M)
                                     } ^ {(gamma+1)/(gamma-1)}

        """
        return super(Isentropic, self).A_Astar(M)

    @storeresult
    def M(self, p_p0=None, rho_rho0=None,
          T_T0=None, A_Astar=None, *args, **kwargs):
        """
        Computes Mach number when one of the arguments are specified

        """
        g = self.gamma
        if p_p0 is not None:
            M = np.sqrt(2. * ((1./np.power(p_p0, (g-1.)/g)) - 1.) / (g-1.))
        elif rho_rho0 is not None:
            M = np.sqrt(2. * ((1./np.power(rho_rho0, (g-1.))) - 1.) / (g-1.))
        elif T_T0 is not None:
            M = np.sqrt(2. * ((1./T_T0)-1.)/(g-1.))
        elif A_Astar is not None:
            Msub, Msup = mach_from_area_ratio(A_Astar)
            M = np.array([Msub, Msup])
        elif 'M' in kwargs.keys():
            return kwargs['M']
        else:
            logger.error('Insufficient data to calculate Mach number')

        return M

    def calculate(self, M=None, p_p0=None, rho_rho0=None,
                  T_T0=None, A_Astar=None):
        """
        Wrapper function to calculate all possible data and store
        using keywords and values in the dictionary `data`.

        Parameters
        ----------
        M, p_p0, rho_rho0, t_t0, A_At : array_like
            Input parameters to calculate, optional but specify one.

        """
        if M:
            mach = M
        else:
            kwargs = {'p_p0': p_p0, 'rho_rho0': rho_rho0, 'T_T0': T_T0,
                      'A_Astar': A_Astar, 'store': False}
            mach = self.M(**kwargs)

        for key in self.keys:
            property_func = getattr(self, key)
            property_func(M=mach, store=True)

        return self.data


class Expansion(FormulaeBase, PrandtlMeyerExpansion):
    """Isentropic expansion fan flow relations"""

    def __init__(self, gamma=1.4):
        self.keys = ['M_1', 'M_2', 'nu_1', 'nu_2', 'theta',
                     'p2_p1', 'rho2_rho1', 'T2_T1']
        self.gamma = gamma

    def calculate(self, theta_deg=None, theta_rad=None,
                  M_1=None, nu_1=None):
        """
        Calculate all possible data and store
        using keywords and values in the dictionary `data`.

        Parameters
        ----------
        theta_deg or theta_rad : float
            Turn angle or deflection angle, optional but specify one.

        M_1 or nu_1 : float
            Mach number or Prandtl-Meyer angle (in radians) of inflow

        """
        if theta_deg:
            self.theta = np.radians(theta_deg)
        elif theta_rad:
            self.theta = theta_rad
        else:
            logger.error('Insufficient data: Turn angle must be specified.')

        if M_1 is None:
            if nu_1 is not None:
                M_1 = mach_from_nu(nu=nu_1, gamma=self.gamma)
            else:
                logger.error('Insufficient data: M_1 or nu_1' +
                             'must be specified.')

        self.M_1 = M_1
        super(Expansion, self).__init__(M_1=self.M_1, theta=self.theta)
        for key in self.keys:
            self.store(key, getattr(self, key))

        return self.data
