import argparse
import matplotlib.pyplot as plt
import numpy

scale_factors = [1.8, 1.5, 1.1, 1.1, 1.6]

def get_run_id(run_filename):
    return '_'.join(run_filename.split('_')[:2])

if __name__ == "__main__":
    description = ["Python script to plot observations over time for a given proposal."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("npzfile3", help="Opsim3 observation info file.")
    parser.add_argument("npzfile4", help="Opsim4 observation info file.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.set_defaults()
    args = parser.parse_args()

    ifile3 = numpy.load(args.npzfile3)
    ifile4 = numpy.load(args.npzfile4)

    tag3 = get_run_id(args.npzfile3)
    tag4 = get_run_id(args.npzfile4)

    props = ["WFD", "NES", "SCP", "GP", "DD"]

    fig = plt.figure(figsize=(10, 10))

    for i, prop in enumerate(props):
        night_key = "{}_nights".format(prop)
        obs_key = "{}_observations".format(prop)

        ax1 = fig.add_subplot(3, 2, i + 1)

        try:
            x4 = ifile4[night_key]
            y4 = ifile4[obs_key]
            max4 = numpy.max(y4)
            ax1.plot(x4, y4, 'o', label=tag4)
        except KeyError:
            max4 = 0

        x3 = ifile3[night_key]
        y3 = ifile3[obs_key]
        max3 = numpy.max(y3)
        ax1.plot(x3, y3, 'o', label=tag3)

        ax1.set_title("Observations for {}".format(prop))
        ax1.set_xlabel("Night")
        ax1.set_ylabel("Observations")
        ax1.set_xlim(1, 3650)
        ax1.set_ylim(0, max(max3, max4) * scale_factors[i])
        ax1.legend(numpoints=1)

    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, wspace=0.29, hspace=0.36)
    plt.show()
