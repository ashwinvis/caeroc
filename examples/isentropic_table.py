import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from caeroc.formulae.isentropic import Isentropic

isen = Isentropic()

N = 10
mach = np.linspace(0., 2., N)
isen.data['M']=mach

for i in xrange(N):
    isen.p_p0(mach[i])
    isen.rho_rho0(mach[i])
    isen.t_t0(mach[i])
    isen.a_a0(mach[i])
    isen.A_At(mach[i])

df = pd.DataFrame(isen.data)
print df

# Plotting
fig,ax = plt.subplots()
ax.plot(df)
fig.show()

