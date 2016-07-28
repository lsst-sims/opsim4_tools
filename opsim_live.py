import collections
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import SALPY_scheduler
import sys

PROJECTION = "aitoff"
NUM_FIELDS = 10

LSST_FOV_RADIUS = math.radians(1.75)
LSST_FOV = LSST_FOV_RADIUS * 2.0

ALPHA = 0.4
FILTER_DICT = collections.OrderedDict([('u', [0, 0, 1, 1]), ('g', [0, 1, 1, 1]),
                                       ('r', [0, 1, 0, 1]), ('i', [1, .5, 0, 1]),
                                       ('z', [1, 0, 0, 1]), ('y', [1, 0, 1, 1])])

def axisSetup(ax):
    ax.grid(True)
    #ax.xaxis.set_ticklabels([])

manager = SALPY_scheduler.SAL_scheduler()
manager.setDebugLevel(0)
manager.salTelemetrySub("scheduler_observationTest")
obs = SALPY_scheduler.scheduler_observationTestC()
print("After setting up subscriber")

plt.ion()

fig, ax1 = plt.subplots(subplot_kw={"projection": PROJECTION})
ax1.grid()

#ax1.grid(True)
#ax1.xaxis.set_ticklabels([])

ax1.get_xaxis().set_visible(False)
ax1.grid(True)

for i, (band_filter, filter_color) in enumerate(FILTER_DICT.items()):
    fig.text(0.41 + i * 0.035, 0.15, band_filter, color=filter_color)

fig.show()

try:
    print("Starting topic loop.")
    field_list = []
    while True:
        rcode = manager.getNextSample_observationTest(obs)
        if rcode == 0 and obs.num_exposures != 0 and obs.filter != '':
            plt.cla()

            ra = np.radians(obs.ra)
            dec = np.radians(obs.dec)
            color = FILTER_DICT[obs.filter]
            zenith_ra = np.radians(obs.observation_start_lst)
            ra = -(ra - zenith_ra - np.pi) % (np.pi * 2.) - np.pi

            ellipse = patches.Ellipse((ra, dec), LSST_FOV / np.cos(dec), LSST_FOV, edgecolor='k',
                                      facecolor=color)

            field_list.append(ellipse)

            for field in field_list:
                ax1.add_patch(field)
            axisSetup(ax1)
            fig_title = "Night {}, MJD {}".format(obs.night, obs.observation_start_mjd)
            plt.text(0.5, 1.18, fig_title, horizontalalignment='center', transform=ax1.transAxes)
            plt.draw()
            plt.pause(0.00000001)

            field_list[-1].set_alpha(ALPHA)
            field_list[-1].set_edgecolor('none')
            if len(field_list) > NUM_FIELDS:
                field_list.pop(0)

except KeyboardInterrupt:
    manager.salShutdown()
    sys.exit(0)
