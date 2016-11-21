import argparse
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from sqlalchemy import create_engine
import os

def get_data_frame(dbpath, use_opsim3):
    engine = create_engine("sqlite:///{}".format(dbpath))
    if not use_opsim3:
        select_sql = "select observationStartMJD, (observationStartLST - ra) as hourAngle, altitude, "\
                     "azimuth from ObsHistory;"
    else:
        select_sql = "select expMJD, lst, fieldRA, altitude, azimuth from Field, ObsHistory "\
                     "where ObsHistory.Field_fieldId = Field.fieldId;"

    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

if __name__ == "__main__":
    description = ["Python script to plot runtime per night and print statistics."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.add_argument("-3", dest="v3", action="store_true", default=False,
                        help="Query an OpSim v3 DB.")
    parser.add_argument("-l", dest="log", action="store_true", default=False,
                        help="Set log scale on hour angle distribution plot.")
    parser.set_defaults()
    args = parser.parse_args()

    run = get_data_frame(args.dbfile, args.v3)

    if not args.v3:
        hour_angle = run['hourAngle'].values
        azimuth = run['azimuth'].values
        altitude = run['altitude'].values
    else:
        hour_angle = numpy.degrees(run['lst'].values) - run['fieldRA'].values
        azimuth = numpy.degrees(run['azimuth'].values)
        altitude = numpy.degrees(run['altitude'].values)

    hour_angle = numpy.where(hour_angle < -180.0, hour_angle + 360.0, hour_angle)
    hour_angle = numpy.where(hour_angle > 180.0, hour_angle - 360.0, hour_angle)
    hour_angle /= 15.0

    fig = plt.figure(figsize=(12, 5))
    fig.suptitle("Observing Bias")

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.hist(hour_angle, bins=100, log=args.log)
    ax1.set_xlabel("Hour Angle (hours)")
    ax1.axvline(color='red', linewidth=2, linestyle='--')

    ax2 = fig.add_subplot(1, 2, 2)
    h2 = ax2.hist2d(azimuth, altitude, bins=40)
    ax2.set_xlabel("Azimuth (degrees)")
    ax2.set_ylabel("Altitude (degrees)")
    plt.colorbar(h2[3], ax=ax2)

    file_head = os.path.basename(args.dbfile).split('.')[0]
    middle_tag = "_observing_bias"
    if args.log:
        middle_tag += "_logscale"
    plt.savefig(file_head + middle_tag + ".png")

    if args.interactive:
        plt.show()
