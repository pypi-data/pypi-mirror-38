import matplotlib.pyplot as plt
import numpy as np

from beluga.ivpsol import Trajectory

from beluga.liepack.domain.hspaces import HLie
from beluga.liepack.domain.liegroups import RN
from beluga.liepack.field import VectorField
from beluga.ivpsol import Flow
from beluga.ivpsol import RKMK

y0 = np.array([1, 0], dtype=np.float64)
tspan = [0, 2*np.pi]
maxstep = 1

def eom_func(t, y):
    return (-y[1], y[0])

dim = y0.shape[0]
y = HLie(RN(dim), y0)
vf = VectorField(y)
vf.set_equationtype('general')
vf.set_fm2g(eom_func)
ts = RKMK()
ts.setmethod('rk45')
f = Flow(ts, vf, variablestep=True)
ti, yi = f(y, tspan[0], tspan[-1], maxstep)
gamma = Trajectory(ti, np.vstack([_.data for _ in yi]))

plt.plot(gamma.t, gamma.y[:,0])
plt.show()
