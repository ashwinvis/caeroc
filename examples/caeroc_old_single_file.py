"""
Compressible Aerodynamics calculator
"""

import math as Math

import matplotlib.pyplot as plt
import numpy as np


class Body:
    def __init__(self, N, length, bodytype=None):
        self.N = N
        self.L = length
        if bodytype is "airfoil":
            self.X, self.Y, self.angle = self.airfoil()
        else:
            self.X, self.Y, self.angle = self.circle()
        plt.plot(self.X, self.Y)
        plt.axis([-length, length, -length, length])
        self._non_dimensionalize(length)

    def nozzle(self):
        """Converging/Diverging Nozzle"""
        pass

    def lavalnozzle(self):
        """Conv. and Div. Nozzle"""
        pass

    def airfoil(self):
        """Biconvex airfoil"""
        L = self.L
        N = self.N
        R = 210
        theta_arc = np.arcsin(L / 2 / R) * 2
        pi = np.pi
        theta_up = np.linspace((pi + theta_arc) / 2, +(pi - theta_arc) / 2, N)
        # theta_up = theta[::-1]
        theta_down = np.linspace((3 * pi - theta_arc) / 2, +(3 * pi + theta_arc) / 2, N)

        X_up = R * np.cos(theta_up)
        Y_up = R * np.sin(theta_up)
        X_down = R * np.cos(theta_down)
        Y_down = R * np.sin(theta_down)

        shift_r = X_up[0]
        X_up -= shift_r
        X_down -= shift_r
        shift_up = Y_up[0]
        shift_down = Y_down[0]
        Y_up = Y_up - shift_up
        Y_down = Y_down - shift_down

        X = np.concatenate((X_up, X_down))
        Y = np.concatenate((Y_up, Y_down))
        slope_up = np.gradient(Y_up, 1) / np.gradient(X_up, 1)
        slope_down = np.gradient(Y_down, 1) / np.gradient(X_down, 1)
        angle = np.arctan(np.concatenate((slope_up, slope_down)))
        return X, Y, angle

    def circle(self):
        theta = np.linspace(0, 2 * np.pi, self.N)
        R = self.L / 2
        X = R * np.cos(theta)
        Y = R * np.sin(theta)
        angle = theta - np.pi / 2
        return X, Y, angle

    def duct(self):
        """Constant area duct/pipe for Fanno & Rayleigh flows"""
        pass

    def _non_dimensionalize(self, scale):
        """Non dimensionalize all geometric parameters with the scale"""
        self.L = self.L / scale
        self.X = self.X / scale
        self.Y = self.Y / scale


class Isentropic:
    def p_p0(self, M, gamma=1.4):
        return self.t_t0(M, gamma) ** (-gamma / (gamma - 1))

    def t_t0(self, M, gamma=1.4):
        return 1 + (gamma - 1) / 2 * M**2


class Expansion(Isentropic):
    """Isentropic Expansion fan flow relations"""

    def M2(self, M1, theta, gamma=1.4):
        if M1 < 0:
            raise ValueError("Subsonic flow.")
        if theta < 0 or theta > np.pi / 2:
            raise ValueError("Incorrect deflection angle. Cannot calculate!")
        pm1 = self.pm(M1, gamma)
        pm2 = pm1 + theta

        mnew = 2.0
        m = 0.0
        while np.abs(mnew - m) > 0.00001:
            m = mnew
            fm = self.pm(m, gamma) - pm2  # *np.pi/180.
            fdm = np.sqrt(m**2 - 1.0) / (1.0 + 0.5 * (gamma - 1.0) * m**2) / m
            mnew = m - fm / fdm

        M2 = m
        return M2

    def pm(self, M1, gamma=1.4):
        if M1 > 1.0:
            g = gamma
            m = M1
            n = np.sqrt((g + 1.0) / (g - 1.0)) * np.arctan(
                np.sqrt((g - 1.0) / (g + 1.0) * (m * m - 1.0))
            )
            n = n - np.arctan(np.sqrt(m * m - 1.0))
            # n = n * 180./np.pi
        elif M1 == 1:
            n = 0.0
        else:
            n = None

        numax = (np.sqrt((gamma + 1.0) / (gamma - 1.0)) - 1) * 90.0
        if n <= 0.0 or n >= numax:
            raise ValueError("Prandtl-Meyer angle out of bounds")
        return n


class ObliqueShock:
    def beta(self, m1, d, g=1.4, i=0):
        p = -(m1 * m1 + 2.0) / m1 / m1 - g * Math.sin(d) * Math.sin(d)
        q = (2.0 * m1 * m1 + 1.0) / Math.pow(m1, 4.0) + (
            (g + 1.0) * (g + 1.0) / 4.0 + (g - 1.0) / m1 / m1
        ) * Math.sin(d) * Math.sin(d)
        r = -Math.cos(d) * Math.cos(d) / Math.pow(m1, 4.0)

        a = (3.0 * q - p * p) / 3.0
        b = (2.0 * p * p * p - 9.0 * p * q + 27.0 * r) / 27.0

        test = b * b / 4.0 + a * a * a / 27.0

        if test > 0.0:
            return -1.0
        elif test == 0.0:
            x1 = Math.sqrt(-a / 3.0)
            x2 = x1
            x3 = 2.0 * x1
            if b > 0.0:
                x1 *= -1.0
                x2 *= -1.0
                x3 *= -1.0

        if test < 0.0:
            phi = Math.acos(Math.sqrt(-27.0 * b * b / 4.0 / a / a / a))
            x1 = 2.0 * Math.sqrt(-a / 3.0) * Math.cos(phi / 3.0)
            x2 = 2.0 * Math.sqrt(-a / 3.0) * Math.cos(phi / 3.0 + np.pi * 2.0 / 3.0)
            x3 = 2.0 * Math.sqrt(-a / 3.0) * Math.cos(phi / 3.0 + np.pi * 4.0 / 3.0)
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

        b1 = Math.asin(Math.sqrt(t1))
        b2 = Math.asin(Math.sqrt(t2))

        betas = b1
        betaw = b2
        if b2 > b1:
            betas = b2
            betaw = b1

        if i == 0:
            return betaw
        if i == 1:
            return betas

    def M1nM2n(self, M1, beta, gamma=1.4):
        M1n = M1 * np.sin(beta)
        M2n = np.sqrt(
            (1.0 + 0.5 * (gamma - 1.0) * M1n**2)
            / (gamma * M1n**2 - 0.5 * (gamma - 1.0))
        )
        return M1n, M2n

    def M2(self, M1, theta, gamma=1.4):
        beta = self.beta(M1, theta)
        M1n, M2n = self.M1nM2n(M1, beta, gamma)
        M2 = M2n / np.sin(beta - theta)
        return M2

    def p2_p1(self, M1, theta, gamma=1.4):
        beta = self.beta(M1, theta)
        M1n = M1 * np.sin(beta)
        p2_p1 = 1.0 + 2.0 * gamma / (gamma + 1.0) * (M1n**2 - 1.0)
        return p2_p1


class AirfoilChara:
    def __init__(self, N, Mach, AngleOfAttack):
        self.cp_lin = np.empty(N)
        self.cp_shock = np.empty(N)
        self.M1 = Mach
        self.AoA = AngleOfAttack * np.pi / 180

        self.obs = ObliqueShock()
        self.exp = Expansion()

    def calc_cp_lin(self, angle):
        N = angle.size / 2
        angle = angle - self.AoA
        self.cp_lin[:N] = 2 * angle[:N] / np.sqrt(self.M1**2 - 1)
        self.cp_lin[N:] = 2 * -angle[N:] / np.sqrt(self.M1**2 - 1)

    def calc_cp_shock(self, angle, debug=False):
        gamma = 1.4
        N = angle.size

        M1 = self.M1
        M2 = np.zeros(N)
        p2_p1 = np.zeros(N)

        # Oblique shock
        angle = angle - self.AoA
        M2[0] = self.obs.M2(M1, angle[0])
        M2[N / 2] = self.obs.M2(M1, -angle[N / 2])
        p2_p1[0] = self.obs.p2_p1(M1, angle[0])
        p2_p1[N / 2] = self.obs.p2_p1(M1, -angle[N / 2])

        # Expanded flow
        for i in range(0, N / 2 - 1):
            j = i + 1
            k = N / 2 + i
            L = N / 2 + i + 1
            if debug:
                print("M2=", M2[i], M2[k], "   p2/p1=", p2_p1[i], p2_p1[k])

            dangle = angle[i] - angle[j]
            M2[j] = self.exp.M2(M2[i], dangle)
            dangle = -(angle[k] - angle[l])
            M2[L] = self.exp.M2(M2[k], dangle)

            p2_p1[j] = self.exp.p_p0(M2[j]) / self.exp.p_p0(M2[i]) * p2_p1[i]
            p2_p1[L] = self.exp.p_p0(M2[L]) / self.exp.p_p0(M2[k]) * p2_p1[k]

        self.cp_shock = 2 * (p2_p1 - 1) / (gamma * M1**2)
        if debug:
            for i in range(0, N / 2 - 1):
                k = N / 2 + i
                print("Cp=", self.cp_shock[i], self.cp_shock[k])


if __name__ == "__main__":
    N = 100
    length = 70.0
    airfoil = Body(N, length, "airfoil")
    chara = AirfoilChara(2 * N, Mach=2, AngleOfAttack=1.5)

    # plt.subplot(111)
    plt.plot(airfoil.X, airfoil.Y)
    plt.axis([0, 1, -0.3, 0.3])
    plt.show()

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True)

    chara.calc_cp_lin(airfoil.angle)
    ax1.set_title("$C_p$ : Linear theory")
    ax1.grid(True)
    ax1.plot(airfoil.X[:N], chara.cp_lin[:N], "r.-")
    ax1.plot(
        airfoil.X[N:],
        chara.cp_lin[N:],
        ".-",
    )

    chara.calc_cp_shock(airfoil.angle, debug=True)
    ax2.set_title("$C_p$ : Nonlinear theory")
    ax2.grid(True)
    ax2.plot(airfoil.X[0:N], chara.cp_shock[0:N], "r.-")
    ax2.plot(airfoil.X[N : 2 * N], chara.cp_shock[N : 2 * N], ".-")
    fig.show()
