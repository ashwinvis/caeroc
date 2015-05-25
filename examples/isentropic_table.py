import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from caeroc.formulae.isentropic import Isentropic

isen = Isentropic()

M_max = 2.0
N = int(M_max*100)
mach = list(np.linspace(0.1, M_max, N))
isen.data['M']=mach

for i in xrange(N):
    isen.p_p0(mach[i])
    isen.rho_rho0(mach[i])
    isen.t_t0(mach[i])
    isen.a_at(mach[i])
    isen.p_pt(mach[i])
    isen.rho_rhot(mach[i])
    isen.t_tt(mach[i])

data = {} 
for k in isen.keys:
    if isen.data[k]: # Data is not empty
        data[k] = isen.data[k]

df = pd.DataFrame(data)
print df

# Plotting
plt.style.use('ggplot')
ax = df.plot(x='M')
fig = plt.gcf()
fig.show()
