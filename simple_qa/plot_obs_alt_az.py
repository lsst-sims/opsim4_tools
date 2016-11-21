import argparse
import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from sqlalchemy import create_engine
import os

def get_data_frame(dbpath, use_opsim3):
    engine = create_engine("sqlite:///{}".format(dbpath))
    if not use_opsim3:
        select_sql = "select domeAz, domeAlt, telAz, telAlt from SlewFinalState;"
    else:
        select_sql = "select domAz, domAlt, telAz, telAlt from SlewState where state=1;"

    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

if __name__ == "__main__":
    description = ["Python script to plot Observatory Alt-Az distributions."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.add_argument("-3", dest="v3", action="store_true", default=False,
                        help="Query an OpSim v3 DB.")
    parser.add_argument("-l", dest="log", action="store_true", default=False,
                        help="Set log scale on Alt-Az plots.")
    parser.set_defaults()
    args = parser.parse_args()

    run = get_data_frame(args.dbfile, args.v3)

    if not args.v3:
        dome_az = run['domeAz'].values
        dome_alt = run['domeAlt'].values
        tel_az = run['telAz'].values
        tel_alt = run['telAlt'].values
    else:
        dome_az = numpy.degrees(run['domAz'].values)
        dome_alt = numpy.degrees(run['domAlt'].values)
        tel_az = numpy.degrees(run['telAz'].values)
        tel_alt = numpy.degrees(run['telAlt'].values)

    if args.log:
        norm = mc.LogNorm()
    else:
        norm = None

    fig = plt.figure(figsize=(12, 5))
    fig.suptitle("Observatory Altitude-Azimuth Distributions")

    ax1 = fig.add_subplot(1, 2, 1)
    h1 = ax1.hist2d(dome_az, dome_alt, bins=40, norm=norm)
    ax1.set_title("Dome")
    ax1.set_xlabel("Azimuth (degrees)")
    ax1.set_ylabel("Altitude (degrees)")
    plt.colorbar(h1[3], ax=ax1)

    ax2 = fig.add_subplot(1, 2, 2)
    h2 = ax2.hist2d(tel_az, tel_alt, bins=40, norm=norm)
    ax2.set_title("Telescope")
    ax2.set_xlabel("Azimuth (degrees)")
    ax2.set_ylabel("Altitude (degrees)")
    plt.colorbar(h2[3], ax=ax2)

    file_head = os.path.basename(args.dbfile).split('.')[0]
    middle_tag = "_observatory_altaz"
    if args.log:
        middle_tag += "_logscale"
    plt.savefig(file_head + middle_tag + ".png")

    if args.interactive:
        plt.show()
