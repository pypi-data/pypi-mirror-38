from beluga.visualization.datasources import Dill
from beluga.utils import keyboard
import matplotlib
ds = Dill('./data.dill')

solution_set = ds.get_solution()
last_continuation = solution_set[-1]

font = {'family' : 'normal',
        'weight' : 'bold',
        'size' : 18}

matplotlib.rc('font', **font)

for trajectory in last_continuation:
    # matplotlib.pyplot.plot(trajectory.y[:,1]*trajectory.aux['const']['re']/1000, trajectory.y[:,0]/1000)
    matplotlib.pyplot.plot(0*trajectory.y[:, 1] * trajectory.aux['const']['re'] / 1000, trajectory.y[:, 0] / 1000)

matplotlib.pyplot.xlabel('Downrange? [km]')
matplotlib.pyplot.ylabel('Altitude [km]')
matplotlib.pyplot.title('Altitude vs Downrange')
matplotlib.pyplot.grid()
matplotlib.pyplot.show()