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
    print("Variance: %.2f seconds" % numpy.var(deltas, ddof=1))
    print("Minimum: %.2f seconds" % numpy.amin(deltas))
    print("Maximum: %.2f seconds" % numpy.amax(deltas))
    print("Survey Time: %.2f hours" % survey_time)

    x = numpy.arange(deltas.size) + 1
    plt.plot(x, deltas)
    plt.title("Processing Time for Each Night")
    plt.xlabel("Night of Survey")
    plt.xlim(0, deltas.size)
    plt.ylim(0, numpy.max(deltas) * 1.15)
    plt.ylabel("$\Delta T_{N}$ (seconds)")
    if args.interactive:
        plt.show()
    plt.savefig(file_head + ".png")
