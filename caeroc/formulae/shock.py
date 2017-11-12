import numpy as np
from skaero.gasdynamics.shocks import _ShockClass
from .base import FormulaeBase


class NormalShock(FormulaeBase, _ShockClass):
    """Normal shock relations"""

    def __init__(self, gamma=1.4):
        self.keys = ['M_1', 'M_2',
                     'p2_p1', 'rho2_rho1', 'T2_T1',
                     'p02_p01', 'rho02_rho01', 'T02_T01']
        self.gamma = gamma

    def M_1(self, M_2=None, p2_p1=None, rho2_rho1=None, T2_T1=None,
            p02_p01=None, p2_p01=None):
        """
        Computes Mach number when one of the arguments are specified

        """
        g = self.gamma
        if p2_p1 is not None:
            M_1 = np.sqrt((p2_p1 - 1) * (g + 1.) / 2. /  g + 1.)
        elif rho2_rho1 is not None:
            M_1 = np.sqrt(2. * rho2_rho1 / (g + 1. - rho2_rho1 * (g - 1.)))
        elif T2_T1 is not None:
            a = 2. * g * (g - 1.)
            b = 4. * g - (g - 1.) * (g - 1.)- T2_T1 * (g + 1.) * (g + 1.)
            c = -2. * (g - 1.)
            M_1, M_11 = np.roots([a, b, c])
        elif p02_p01 is not None:
            raise NotImplementedError
        elif p2_p01 is not None:
            raise NotImplementedError
        elif 'M' in kwargs.keys():
            return kwargs['M']
        else:
            raise ValueError('Insufficient data to calculate Mach number')

        return M


    def calculate(self, M_1=None, M_2=None,
                  p2_p1=None, rho2_rho1=None, T2_T1=None,
                  p02_p01=None, rho02_rho01=None, T02_T01=None):
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
        if M_1 is None:
            pass
        elif any([v is not None for v in (p2_p1, rho2_rho1, T2_T1)]):
            M_1 = self.M_1(p2_p1, rho2_rho1, T2_T1)
        else:
            raise ValueError('Insufficient data: M_1 or nu_1' +
                             'must be specified.')

        self.M_1 = M_1
        super(Expansion, self).__init__(M_1=self.M_1, theta=self.theta)
        for key in self.keys:
            self.store(key, getattr(self, key))

        return self.data


class ObliqueShock(NormalShock):

    def __init__(self, gamma=1.4):
         self.keys = ['M_1', 'M_2', 'M_1n', 'M_2n', 'theta',
                      'p2_p1', 'rho2_rho1', 'T2_T1']
         self.gamma = gamma

    def beta(self,m1,d,g=1.4,i=0):
        p=-(m1*m1+2.)/m1/m1-g*np.sin(d)*np.sin(d)
        q=(2.*m1*m1+1.)/ np.pow(m1,4.)+((g+1.)*(g+1.)/4.+
                                          (g-1.)/m1/m1)*np.sin(d)*np.sin(d)
        r=-np.cos(d)*np.cos(d)/np.pow(m1,4.)

        a=(3.*q-p*p)/3.
        b=(2.*p*p*p-9.*p*q+27.*r)/27.

        test=b*b/4.+a*a*a/27.

        if (test>0.0):
            return -1.0
        elif (test==0.0):
          x1=np.sqrt(-a/3.)
          x2=x1
          x3=2.*x1
          if(b>0.0):
            x1*=-1.
            x2*=-1.
            x3*=-1.

        if(test<0.0):
          phi=np.acos(np.sqrt(-27.*b*b/4./a/a/a))
          x1=2.*np.sqrt(-a/3.)*np.cos(phi/3.)
          x2=2.*np.sqrt(-a/3.)*np.cos(phi/3.+np.pi*2./3.)
          x3=2.*np.sqrt(-a/3.)*np.cos(phi/3.+np.pi*4./3.)
          if(b>0.0):
            x1*=-1.
            x2*=-1.
            x3*=-1.

        s1=x1-p/3.
        s2=x2-p/3.
        s3=x3-p/3.

        if(s1<s2 and s1<s3):
          t1=s2
          t2=s3
        elif(s2<s1 and s2<s3):
          t1=s1
          t2=s3
        else:
          t1=s1
          t2=s2

        b1=np.asin(np.sqrt(t1))
        b2=np.asin(np.sqrt(t2))

        betas=b1
        betaw=b2
        if(b2>b1):
          betas=b2
          betaw=b1

        if(i==0):
            return betaw
        if(i==1):
            return betas

    def mach1n_mach2n(self, M1, beta ,gamma=1.4):
        M1n = M1 * np.sin(beta)
        M2n = np.sqrt((1. + .5 * (gamma - 1.) * M1n**2) /
                      (gamma * M1n**2 - .5 * (gamma - 1.)))
        return M1n, M2n

    def mach2(self,M1,theta,gamma=1.4):
        beta = self.beta(M1, theta)
        M1n, M2n = self.M1nM2n(M1, beta, gamma)
        M2 = M2n / np.sin(beta-theta)
        return M2

    def p2_p1(self,M1,theta,gamma=1.4):
        beta = self.beta(M1, theta)
        M1n = M1 * np.sin(beta)
        p2_p1 = 1.+2.*gamma/(gamma + 1.)*(M1n**2-1.)
        return p2_p1
