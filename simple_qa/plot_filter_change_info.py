from __future__ import division, print_function
import argparse
import matplotlib.pylab as plt
import multiprocessing
import numpy
import pandas as pd
from sqlalchemy import create_engine
import os

MINUTES_IN_DAY = 24 * 60

def find_filter_changes(dbname, col, nr, fc, mtfc):
    engine = create_engine("sqlite:///{}".format(dbname))
    with engine.connect() as conn, conn.begin():
        for night in range(nr[0], nr[1]):
            select_sql = "select {}, filter from ObsHistory where night={};".format(col, night)
            run = pd.read_sql_query(select_sql, conn)
            filters = run['filter'].values
            idx = numpy.where(filters[:-1] != filters[1:])
            mjd = run[col].values[idx]
            fc[night] = (len(mjd))
            diff_mjd = mjd[1:] - mjd[:-1]
            try:
                mtfc[night] = numpy.min(diff_mjd) * MINUTES_IN_DAY
            except ValueError:
                # No filter changes
                mjd = run[col].values
                try:
                    mtfc[night] = (mjd[-1] - mjd[0]) * MINUTES_IN_DAY
                except IndexError:
                    # Downtime night
                    mtfc[night] = 0.0
            #print("Night {}: Number of filter changes: {}".format(night, len(mjd)))

if __name__ == "__main__":
    description = ["Python script to plot various filter change related quantities."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-3", dest="v3", action="store_true", default=False, help="Query an OpSim v3 DB.")
    parser.add_argument("-p", dest="num_procs", default=2, type=int,
                        help="Specify the number of processors to use.")
    parser.add_argument("-n", dest="nights", default=3650, type=int,
                        help="Specify the number of nights to process.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.add_argument("-l", dest="log", action="store_true", default=False,
                        help="Set log scale on y axis for histogram plots.")
    parser.set_defaults()
    args = parser.parse_args()

    mgr = multiprocessing.Manager()
    filter_changes_dict = mgr.dict()
    min_time_btw_filter_changes_dict = mgr.dict()

    if args.v3:
        mjd_name = "expMJD"
    else:
        mjd_name = "observationStartMJD"

    # Create a list of jobs and then iterate through the number of processes appending each process to
    # the job list
    frac = args.nights // args.num_procs
    jobs = [multiprocessing.Process(target=find_filter_changes,
                                    args=(args.dbfile, mjd_name, (i * frac, (i + 1) * frac),
                                          filter_changes_dict,
                                          min_time_btw_filter_changes_dict))
            for i in range(0, args.num_procs)]

    # Start the processes
    for j in jobs:
        j.start()

    # Ensure all of the processes have finished
    for j in jobs:
        j.join()

    print("Processing complete.")

    filter_changes = numpy.array(filter_changes_dict.values())
    min_time_btw_filter_changes = numpy.array(min_time_btw_filter_changes_dict.values())
    night_array = numpy.array(filter_changes_dict.keys())

    fig = plt.figure(figsize=(12, 8))
    fig.suptitle("Filter Change Quantities")

    ax1 = fig.add_subplot(2, 3, 1)
    ax1.plot(night_array, filter_changes)
    ax1.set_xlabel("Night")
    ax1.set_xlim(night_array[0], night_array[-1])
    ax1.set_xticks(numpy.arange(0, night_array[-1], 1000))
    ax1.set_ylabel("Number of Filter Changes")

    ax2 = fig.add_subplot(2, 3, 2)
    ax2.hist(filter_changes, bins=numpy.max(filter_changes))
    ax2.set_xlabel("Number of Filter Changes")

    ax3 = fig.add_subplot(2, 3, 3)
    ax3.plot(night_array, min_time_btw_filter_changes)
    ax3.set_xlabel("Night")
    ax3.set_xlim(night_array[0], night_array[-1])
    ax3.set_xticks(numpy.arange(0, night_array[-1], 1000))
    ax3.set_ylabel("Min Time Btw Filter Changes (min)")

    ax4 = fig.add_subplot(2, 3, 4)
    ax4.hist(min_time_btw_filter_changes, bins=100, log=args.log)
    ax4.set_xlabel("Min Time Btw Filter Changes (min)")

    ax5 = fig.add_subplot(2, 3, 5)
    ax5.scatter(filter_changes, min_time_btw_filter_changes)
    ax5.set_xlabel("Number of Filter Changes")
    ax5.set_ylabel("Min Time Btw Filter Changes (min)")

    file_head = os.path.basename(args.dbfile).split('.')[0]
    fig_name = "{}_filter_changes.png".format(file_head)

    plt.subplots_adjust(left=0.07, right=0.95, top=0.93, bottom=0.1, hspace=0.2, wspace=0.45)
    plt.savefig(fig_name)
    if args.interactive:
        plt.show()
