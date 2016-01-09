import numpy as np
import skaero.gasdynamics.isentropic as sk
from caeroc.formulae.base import FormulaeBase
from caeroc.util.decorators import storeresult

class Isentropic(FormulaeBase, sk.IsentropicFlow):
    """Isentropic flow relations for quasi 1D flows"""

    def __init__(self, gamma=1.4):
        self.keys = ['M','p_p0', 'rho_rho0', 'T_T0',
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
        return super(Isentropic,self).p_p0(M)
        
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
        return super(Isentropic,self).rho_rho0(M)

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
        return super(Isentropic,self).T_T0(M)
        
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
        return super(Isentropic,self).p_p0(M) * np.power((g / 2. + .5),
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
        return super(Isentropic,self).rho_rho0(M) * np.power((g /2. + .5),
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
        return super(Isentropic,self).T_T0(M) * (g / 2. + .5)
    
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
        return super(Isentropic,self).A_Astar(M)

    @storeresult
    def M(self, p_p0=None, rho_rho0=None, T_T0=None, A_Astar=None, *args, **kwargs):
        """
        Computes Mach number when one of the arguments are specified

        """
        g = self.gamma
        if p_p0 is not None:
            M = np.sqrt(2. * ((1./np.power(p_p0, (g-1.)/g)) - 1.) / (g-1.))
        elif rho_rho0 is not None:
            M = np.sqrt(2. * ((1./np.power(rho_rho0, (g-1.))) - 1.) / (g-1.))
        elif T_T0 is not None:
            M = np.sqrt(2. * ((1./t_t0)-1.)/(g-1.))
        elif A_Astar is not None:
            Msub, Msup = sk.mach_from_area_ratio(A_Astar)
            M = np.array([Msub, Msup])
        else:
            raise ValueError('Insufficient data to calculate Mach number')

        return M
            
    def calculate(self, M=None, p_p0=None, rho_rho0=None, T_T0=None, A_Astar=None):
        """
        Wrapper function to calculate all possible data and store
        using keywords and values in the dictionary kwargs.

        Parameters
        ----------
        M, p_p0, rho_rho0, t_t0, A_At : array_like
            Input parameters to calculate, optional but specify one.
        
        """
        if M:
            mach = M
            self.store('M', mach)
        else:
            kwargs = {'p_p0':p_p0, 'rho_rho0':rho_rho0, 'T_T0':T_T0,
                    'A_Astar':A_Astar, 'store':True}
            mach = self.M(**kwargs)
        
        if mach is None:
            raise ValueError('Cannot calculate data without one of these inputs:' +
                             'M, p_p0, rho_rho0, T_T0, A_Astar')

        self.p_p0(mach, True)
        self.rho_rho0(mach, True)
        self.T_T0(mach, True)
        self.p_pt(mach, True)
        self.rho_rhot(mach, True)
        self.T_Tt(mach, True)
        self.A_Astar(mach, True)
        self.Mt(mach, True)

        return self.data

class Expansion(FormulaeBase, sk.PrandtlMeyerExpansion):
    """Isentropic expansion fan flow relations"""

    def __init__(self, gamma=1.4):
        self.keys = ['M1','M2','pm']
        self.isen = Isentropic(gamma=gamma)
        super(Expansion, self).__init__()

    def mach1(self, p_p0=None, rho_rho0=None, t_t0=None,
              A_At=None, pm=None, store=True):
        if pm is not None:
            self.store('pm', pm) 
            mnew=2.0
            m=0.0
            while( abs(mnew-m) > 1e-5):
              m=mnew
              fm=(self.pm(m,gamma) - pm)#*3.14159265359/180.
              fdm=np.sqrt(m**2 - 1.) / (1 + 0.5*(gamma-1.) * m**2)/m
              mnew=m-fm/fdm               
            M1 = m
        else:
            M1 = self.isen.M(p_p0, rho_rho0, t_t0,
                             A_At, gamma, store=False)
        
        if store:
            self.store('M1',M1)            
            
        return M1       
     
    def mach2(self, M1, theta, gamma=1.4):
        if M1<0:
            raise ValueError('Subsonic flow.')
        if theta < 0 or theta > np.pi/2:
            raise ValueError('Incorrect deflection angle. Cannot calculate!')
        pm1 = self.pm(M1, gamma)
        pm2 = pm1 + theta

        mnew = 2.0
        m = 0.0
        while(np.abs(mnew - m) > 0.00001):
          m=mnew
          fm=(self.pm(m,gamma)-pm2)#*np.pi/180.
          fdm=np.sqrt(m**2 - 1.)/(1. + 0.5*(gamma-1.)*m**2)/m
          mnew=m-fm/fdm
          
        M2 = m
        return M2
       
    def pm(self,M1, gamma=1.4):
        if M1>1.:
            g = gamma
            m = M1
            n = (np.sqrt((g + 1.) / (g - 1.)) *
                 np.arctan(np.sqrt((g - 1.) / (g + 1.) * (m * m - 1.))))
            n = n - np.arctan(np.sqrt(m * m - 1.))
        elif M1==1:
            n = 0.
        else:
            n = None
            
        numax=(np.sqrt((gamma+1.)/(gamma-1.))-1)*90.
        if(n<=0.0 or n>=numax):
            raise ValueError("Prandtl-Meyer angle out of bounds")            
        return n

