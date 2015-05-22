import numpy as np

class FormulaeBase(object):
    """Data management class for all flow quantities"""
    def __init__(self):
        # self.keys = []
        self.data = {}
        self.minima = {} 
        self.maxima = {}
        self.gamma = 1.4
        self._init_dataminmax()

    def _init_dataminmax(self):
        """
        Initializes the data dictionary and the theoretical minima and maxima 
        for flow quantities.
        """
        keys = self.keys
        if keys.__len__() is 0:
            raise ValueError('Unintialized list of keys')

        key_mach = ['M','M1', 'M2', 'M1n', 'M2n']
        key_ratio = ['p_p0','rho_rho0','t_t0']
        key_ang = ['pm', 'theta']
        inf = 1e5

        for k in keys:
            self.data[k] = []

            if k in key_mach:
                self.minima[k] = 0.
                self.maxima[k] = 5.
            elif k in key_ratio:
                self.minima[k] = 0.
                self.maxima[k] = 1.
            elif k in key_ang:
                self.minima[k] = 0.
                if k is 'theta':
                    self.maxima[k] = np.pi/2
                else:
                    self.maxima[k] = (np.sqrt((self.gamma+1.) /
                                      (self.gamma-1.))-1) * np.pi/2
            elif k is 'A_At':
                self.minima[k] = 1.
                self.maxima[k] = inf
            else:
                self.minima[k] = 0.
                self.maxima[k] = inf

    def store(self, key, val):
        if key not in self.keys:
            raise ValueError('Unknown key: %s'%key)

        self._check_limits(key, val)
        self.data[key].append(val)

    def _check_limits(self, key, val):
        """Checks if the computed value is within the theoretical limits"""

        minimum = self.minima[key] 
        maximum = self.maxima[key] 
        if val < minimum or val > maximum:
            raise ValueError('%s must be between %f and %f'%(key,minimum,maximum))

