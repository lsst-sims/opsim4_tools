import argparse
import collections
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import SALPY_scheduler
import sys

PROJECTION = "polar"
NUM_FIELDS = 10

LSST_FOV_RADIUS = math.radians(1.75)
LSST_FOV = LSST_FOV_RADIUS * 2.0

ALPHA = 0.4
FILTER_DICT = collections.OrderedDict([('u', [0, 0, 1, 1]), ('g', [0, 1, 1, 1]),
                                       ('r', [0, 1, 0, 1]), ('i', [1, .5, 0, 1]),
                                       ('z', [1, 0, 0, 1]), ('y', [1, 0, 1, 1])])

PI_OVER_2 = np.pi / 2.0

def axisSetup(ax):
    ax.grid(True)
    #ax.xaxis.set_ticklabels([])

def run(opts):
    manager = SALPY_scheduler.SAL_scheduler()
    manager.setDebugLevel(0)
    manager.salTelemetrySub("scheduler_observation")
    obs = SALPY_scheduler.scheduler_observationC()
    if opts.verbose > 0:
        print("After setting up subscriber")

    plt.ion()

    fig, ax1 = plt.subplots(subplot_kw={"projection": PROJECTION})
    #ax1.grid()
    #print(type(ax1))
    ax1.grid(True)
    #ax1.set_rgrids([0.3333, 0.66666, 1.0], ["60", "30", "0"])
    #ax1.yaxis.set_ticklabels([])

    #ax1.get_xaxis().set_visible(False)
    #ax1.grid(True)

    for i, (band_filter, filter_color) in enumerate(FILTER_DICT.items()):
        fig.text(0.1 + i * 0.035, 0.05, band_filter, color=filter_color)

    fig.show()
    num_obs = 0
    try:
        if opts.verbose > 0:
            print("Starting topic loop.")
        field_list = []

        while True:
            rcode = manager.getNextSample_observation(obs)
            if opts.verbose > 1:
                print("A: {}, {}, {}".format(rcode, obs.num_exposures, obs.filter))
            if rcode == 0 and obs.num_exposures != 0 and obs.filter != '':
                plt.cla()

                az = np.radians(obs.azimuth)
                #alt = np.sin(math.radians(obs.dec))
                alt = 1.0 - math.radians(obs.altitude) / PI_OVER_2
                color = FILTER_DICT[obs.filter]
                ellipse = patches.Ellipse((az, alt), LSST_FOV / alt, LSST_FOV, edgecolor='k',
                                          facecolor=color)

                field_list.append(ellipse)

                for field in field_list:
                    ax1.add_patch(field)
                #axisSetup(ax1)
                fig_title = "Night {}, MJD {}".format(obs.night, obs.observation_start_mjd)
                plt.text(-0.3, 1.0, fig_title, transform=ax1.transAxes)
                plt.draw()
                plt.pause(0.0001)

                field_list[-1].set_alpha(ALPHA)
                field_list[-1].set_edgecolor('none')
                if len(field_list) > NUM_FIELDS:
                    field_list.pop(0)
                num_obs += 1
                if opts.verbose > 1:
                    print("Observation number {}".format(num_obs))

    except KeyboardInterrupt:
        manager.salShutdown()
        if opts.verbose > 0:
            print("Total observations received: {}".format(num_obs))
        sys.exit(0)

if __name__ == "__main__":

    description = ["Python script to live view a running simulation or a survey database."]

    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("-v", "--verbose", dest="verbose", action='count', default=0,
                        help="Set the verbosity of the program.")
    parser.set_defaults()
    args = parser.parse_args()

    run(args)
