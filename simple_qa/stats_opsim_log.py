import argparse
import matplotlib.pyplot as plt
import numpy
import os

if __name__ == '__main__':
    description = ["Python script to plot runtime per night and print statistics."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.set_defaults()
    args = parser.parse_args()

    file_head = os.path.basename(args.dbfile).split('.')[0]

    ifile = numpy.load(args.dbfile)
    deltas = ifile["deltas"]
    survey_time = ifile["survey_time"][0]
    print("Number of Nights: %d" % deltas.size)
    print("Mean: %.2f seconds" % numpy.mean(deltas))
    print("Median: %.2f seconds" % numpy.median(deltas))
    print("Standard Deviation: %.2f seconds" % numpy.std(deltas, ddof=1))
    print("Minimum: %.2f seconds" % numpy.amin(deltas))
    print("Maximum: %.2f seconds" % numpy.amax(deltas))
    print("Survey Time: %.2f hours" % survey_time)

    x = numpy.arange(deltas.size) + 1

    fig = plt.figure(figsize=(12, 5))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(x, deltas)
    ax1.set_title("Processing Time for Each Night")
    ax1.set_xlabel("Night of Survey")
    ax1.set_xlim(0, deltas.size)
    ax1.set_ylim(0, numpy.max(deltas) * 1.15)
    ax1.set_ylabel("$\Delta T_{N}$ (seconds)")

    ax2 = fig.add_subplot(1, 2, 2)
    font_size = 15
    ax2.text(0.2, 0.75, "Number of Nights: {}".format(deltas.size), fontsize=font_size)
    ax2.text(0.2, 0.65, "Survey Time: {:.2f} hours".format(survey_time), fontsize=font_size)
    ax2.text(0.2, 0.55, "Mean: {:.2f} seconds".format(numpy.mean(deltas)), fontsize=font_size)
    ax2.text(0.2, 0.45, "Median: {:.2f} seconds".format(numpy.median(deltas)), fontsize=font_size)
    ax2.text(0.2, 0.35, "Standard Deviation: {:.2f} seconds".format(numpy.std(deltas, ddof=1)),
             fontsize=font_size)
    ax2.text(0.2, 0.25, "Minimum: {:.2f} seconds".format(numpy.amin(deltas)), fontsize=font_size)
    ax2.text(0.2, 0.15, "Maximum: {:.2f} seconds".format(numpy.amax(deltas)), fontsize=font_size)
    ax2.set_title("Statistics")
    plt.setp(plt.gca(), frame_on=False, xticks=(), yticks=())

    plt.subplots_adjust(left=0.08, right=1.00, wspace=0.0)
    plt.savefig(file_head + "_runtime_per_night.png")

    try:
        suggest_targets_times = ifile["suggest_targets_times"]
        observe_target_times = ifile["observe_target_times"]

        try:
            print("")
            print("Suggest Targets Mean: {:.3f} seconds".format(numpy.mean(suggest_targets_times)))
            print("Suggest Targets Maximum: {:.2f} seconds".format(numpy.amax(suggest_targets_times)))
            print("Observe Target Mean: {:.3f} seconds".format(numpy.mean(observe_target_times)))
            print("Observe Target Maximum: {:.2f} seconds".format(numpy.amax(observe_target_times)))
        except ValueError:
            pass
    except KeyError:
        pass

    if args.interactive:
        plt.show()
