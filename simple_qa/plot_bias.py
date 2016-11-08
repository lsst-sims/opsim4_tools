import argparse
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from sqlalchemy import create_engine
import os
import sys

def get_data_frame(dbpath):
    engine = create_engine("sqlite:///{}".format(dbpath))
    select_sql = "select observationStartMJD, (observationStartLST - ra) as hourAngle, altitude, azimuth "\
                 "from ObsHistory;"
    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

if __name__ == "__main__":
    description = ["Python script to plot runtime per night and print statistics."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.set_defaults()
    args = parser.parse_args()

    run = get_data_frame(args.dbfile)

    hour_angle = run['hourAngle'].values
    hour_angle = numpy.where(hour_angle < -180.0, hour_angle + 360.0, hour_angle)
    hour_angle = numpy.where(hour_angle > 180.0, hour_angle - 360.0, hour_angle)
    hour_angle /= 15.0

    azimuth = run['azimuth'].values
    altitude = run['altitude'].values

    fig = plt.figure(figsize=(12, 5))
    fig.suptitle("Observing Bias")

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.hist(hour_angle, bins=100, log=True)
    ax1.set_xlabel("Hour Angle (hours)")
    ax1.axvline(color='red', linewidth=2, linestyle='--')

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.hist2d(azimuth, altitude, bins=40)
    ax2.set_xlabel("Azimuth (degrees)")
    ax2.set_ylabel("Altitude (degrees)")

    file_head = os.path.basename(args.dbfile).split('.')[0]
    plt.savefig(file_head + "_observing_bias.png")

    if args.interactive:
        plt.show()
