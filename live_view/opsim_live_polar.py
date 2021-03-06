from __future__ import division
import argparse
import collections
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import SALPY_scheduler
import sys

PROJECTION = "polar"
NUM_FIELDS = 10

CANVAS_BACKGROUND_COLOR = (0.75, 0.75, 0.75)

LSST_FOV_RADIUS = math.radians(1.75)
LSST_FOV = LSST_FOV_RADIUS * 2.0
MOON_SCALE = 6.0
MOON_DIA = math.radians(0.5 * MOON_SCALE)

ALPHA = 0.5
FILTER_DICT = collections.OrderedDict([('u', [0, 1, 1, 1]), ('g', [0, 1, 0, 1]),
                                       ('r', [1, 1, 0, 1]), ('i', [1, .5, 0, 1]),
                                       ('z', [1, 0, 0, 1]), ('y', [1, 0, 1, 1])])
MOON_ALPHA = 0.05

ASTRO_TWILIGHT = -18.0

PI_OVER_2 = np.pi / 2.0

TWILIGHT_COLOR = (0.35, 0, 1)

def normalize_color(color):
    if color > 1:
        return 1
    if color < 0:
        return 0
    return color

def axisSetup(ax, bgcolor=TWILIGHT_COLOR):
    try:
        ax.set_facecolor(bgcolor)
    except AttributeError:
        ax.set_axis_bgcolor(bgcolor)
    ax.set_rgrids([0.3333, 0.66666], [u"60\u00b0", u"30\u00b0"], color='w')
    ax.set_theta_zero_location("N")
    ax.grid(True, color='w', linewidth=1)

def run(opts):
    manager = SALPY_scheduler.SAL_scheduler()
    manager.setDebugLevel(0)
    manager.salTelemetrySub("scheduler_observation")
    obs = SALPY_scheduler.scheduler_observationC()
    if opts.verbose > 0:
        print("After setting up subscriber")

    plt.ion()

    fig, ax1 = plt.subplots(subplot_kw={"projection": PROJECTION})
    fig.set_facecolor(CANVAS_BACKGROUND_COLOR)
    axisSetup(ax1)

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
                alt = 1.0 - math.radians(obs.altitude) / PI_OVER_2
                color = FILTER_DICT[obs.filter]
                ellipse = patches.Ellipse((az, alt), LSST_FOV / alt, LSST_FOV, edgecolor='k',
                                          facecolor=color)

                field_list.append(ellipse)

                for field in field_list:
                    ax1.add_patch(field)

                if obs.moon_alt > -0.25 * MOON_SCALE:
                    moon_az = np.radians(obs.moon_az)
                    moon_alt = 1.0 - math.radians(obs.moon_alt) / PI_OVER_2
                    alpha = np.max([obs.moon_phase / 100., MOON_ALPHA])
                    moon = patches.Ellipse((moon_az, moon_alt), MOON_DIA / moon_alt, MOON_DIA,
                                           color='w', alpha=alpha)
                    ax1.add_patch(moon)

                if obs.sun_alt <= ASTRO_TWILIGHT:
                    tom_text = "Night"
                    background_color = (0, 0, 0)
                else:
                    tom_text = "Twilight"
                    blue_color = normalize_color((1 / 6) * obs.sun_alt + 3)
                    red_color = normalize_color((35 / 600) * obs.sun_alt + 105 / 100)
                    background_color = (red_color, 0, blue_color)
                axisSetup(ax1, background_color)
                fig_title = "Night {}, MJD {}".format(obs.night, obs.observation_start_mjd)
                plt.text(-0.3, 1.0, fig_title, transform=ax1.transAxes)
                moon_phase_text = "Moon Phase: {:.1f}%".format(obs.moon_phase)
                plt.text(0.9, 1.0, moon_phase_text, transform=ax1.transAxes)

                plt.text(0.9, 0.0, tom_text, transform=ax1.transAxes)
                plt.draw()
                if opts.save is not None:
                    filename = "mjd_{:15.0f}.png".format(obs.observation_start_mjd * 1e10)
                    filepath = os.path.join(opts.save, filename)
                    plt.savefig(filepath, facecolor=CANVAS_BACKGROUND_COLOR)
                plt.pause(0.0001)

                field_list[-1].set_alpha(ALPHA)
                field_list[-1].set_edgecolor('none')
                if len(field_list) > opts.trail:
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
    parser.add_argument("-t", "--trail", dest="trail", default=10, type=int,
                        help="Set the number of fields to keep.")
    parser.add_argument("-s", "--save", dest="save", default=None)
    parser.set_defaults()
    args = parser.parse_args()

    run(args)
