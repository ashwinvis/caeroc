import numpy as np

class Isentropic:
    def p_p0(self,M, gamma=1.4):
        return self.t_t0(M, gamma) ** (-gamma / (gamma - 1))
        
    def t_t0(self,M,gamma=1.4):
        return (1+(gamma-1)/2 * M**2)
        

class Expansion(Isentropic):
    """Isentropic Expansion fan flow relations"""
    def M2(self, M1, theta, gamma=1.4):
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
            #n = n * 180./np.pi
        elif M1==1:
            n = 0.
        else:
            n = None
            
        numax=(np.sqrt((gamma+1.)/(gamma-1.))-1)*90.
        if(n<=0.0 or n>=numax):
            raise ValueError("Prandtl-Meyer angle out of bounds")            
        return n

