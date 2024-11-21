from numbers import Number

import numpy as np

from ..logger import logger


class FormulaeBase:
    """Data management class for all flow quantities"""

    def __init__(self, *args, **kwargs):
        # self.keys = []
        self.data = {}
        self.minima = {}
        self.maxima = {}
        self._init_dataminmax()
        try:
            super().__init__(*args, **kwargs)
        except ValueError as e:
            logger.critical(e)

    def _init_dataminmax(self):
        """
        Initializes the data dictionary and the theoretical minima and maxima
        for flow quantities.
        """
        keys = self.keys
        if len(keys) == 0:
            raise ValueError("Unintialized list of keys")

        key_mach = ["M", "M_1", "M_2", "M_1n", "M_2n"]
        key_ratio = ["p_p0", "rho_rho0", "T_T0"]
        key_ang = ["nu", "theta"]
        inf = 1e10

        for k in keys:
            self.data[k] = []

            if k in key_mach:
                self.minima[k] = 0.0
                self.maxima[k] = 5.0
            elif k in key_ratio:
                self.minima[k] = 0.0
                self.maxima[k] = 1.0
            elif k in key_ang:
                self.minima[k] = 0.0
                if k == "theta":
                    self.maxima[k] = np.pi / 2
                else:
                    self.maxima[k] = (
                        (np.sqrt((self.gamma + 1.0) / (self.gamma - 1.0)) - 1)
                        * np.pi
                        / 2
                    )
            elif k == "A_At":
                self.minima[k] = 1.0
                self.maxima[k] = inf
            else:
                self.minima[k] = 0.0
                self.maxima[k] = inf

    def store(self, key, val):
        if key not in self.keys:
            raise ValueError(f"Unknown key: {key} not in {self.keys}")

        self._check_limits(key, val)
        self.data[key].append(val)

    def _check_limits(self, key, val):
        """Checks if the computed value is within the theoretical limits"""

        minimum = self.minima[key]
        maximum = self.maxima[key]
        if isinstance(val, np.ndarray) or isinstance(val, Number):
            if np.all(val < minimum) or np.all(val > maximum):
                logger.error(f"{key} = {val} must be between {minimum} and {maximum}")
        else:
            logger.critical(f"{val} is not a number.")
