'''
Pull data points from the original figure and replot
'''

import numpy as np
import sciris as sc
import pylab as pl

steal = True

xy = ['x','y']


#%% Get the data
if steal:
    import datathief as dt

    filename = 'fig_perf_datathief.png'
    xlim = [2, 5]
    ylim = [0, 2]
    kw = dict(filename=filename, xlim=xlim, ylim=ylim)
    old = dt.datathief(**kw, dcol=[0,1,0])
    new = dt.datathief(**kw, dcol=[0,1,1])

    # Convert to exponent
    for k in xy:
        for d in [old,new]:
            d[k] = 10**d[k]

else:
    old = sc.objdict(dict(
        x = np.array([  100.        ,   200.06255142,   500.58964911,  1001.49242415, 2003.61129602,  5013.36741188, 10029.87075624]),
        y = np.array([    2.29609478,     4.34064817,     8.83370006,    18.09847247,   32.86543969,    89.82984898,   175.60686295])
    ))
    new = sc.objdict(dict(
        x = np.array([   100.        ,    200.06255142,    500.58964911,    997.02182042, 2003.61129602,   5013.36741188,  10029.87075624,  19976.44181779, 50208.49482466, 100000.        ]),
        y = np.array([     1.1745432 ,      1.14346839,      1.33408024,      1.38883035,    1.75606863,      2.35849328,      3.82156834,      5.75208543,    14.60438457, 25.81879406])
    ))

f = 100/70
for d in [old, new]:
    d.y *= f # Convert to 100 years from the original 70

line_old = old.x/3.3e3*f
line_new = new.x/210e3*f



#%% Plot
sc.options(dpi=200)

pl.figure(figsize=(6,4))
pl.loglog(old.x, old.y, 'o', label='Object-based implementation')
pl.loglog(new.x, new.y, 'o', label='Array-based implementation')
pl.plot(old.x, line_old, label='Object-based time (3,000 agent-years/s)')
pl.plot(new.x, line_new, label='Array-based time (3,000 agent-years/s)')
pl.xlabel('Number of agents in simulation')
pl.ylabel('CPU time (s)')
pl.legend()
for k in xy:
    sc.commaticks(axis=k)

sc.figlayout()
pl.show()