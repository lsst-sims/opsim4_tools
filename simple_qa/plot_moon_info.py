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
        select_sql = "select skyBrightness, moonDistance, moonPhase, filter from ObsHistory;"
    else:
        select_sql = "select expMJD, lst, fieldRA, altitude, azimuth from Field, ObsHistory "\
                     "where ObsHistory.Field_fieldId = Field.fieldId;"

    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

if __name__ == "__main__":
    description = ["Python script to plot moon information."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.add_argument("-3", dest="v3", action="store_true", default=False,
                        help="Query an OpSim v3 DB.")
    parser.add_argument("-l", dest="log", action="store_true", default=False,
                        help="Set log scale on distribution plots.")
    parser.set_defaults()
    args = parser.parse_args()

    run = get_data_frame(args.dbfile, args.v3)

    if args.log:
        norm = mc.LogNorm()
    else:
        norm = None

    sky_brightness = run['skyBrightness'].values
    idxs = numpy.where(numpy.isfinite(sky_brightness))
    sky_brightness = sky_brightness[idxs]

    moon_distance = run['moonDistance'].values[idxs]
    moon_phase = run['moonPhase'].values[idxs]
    band_filter = run['filter'].values[idxs]

    fig1 = plt.figure(figsize=(11, 8))
    fig1.suptitle("Moon Information")

    ax1 = fig1.add_subplot(2, 2, 1)
    ax1.hist(moon_distance, bins=100, log=args.log)
    ax1.set_xlabel("Moon Distance (degrees)")

    ax2 = fig1.add_subplot(2, 2, 2)
    h2 = ax2.hist2d(sky_brightness, moon_distance, bins=(100, 100), norm=norm)
    ax2.set_xlabel("Sky Brightness ($mags/arcsec^2$)")
    ax2.set_ylabel("Moon Distance (degrees")
    plt.colorbar(h2[3], ax=ax2)

    ax3 = fig1.add_subplot(2, 2, 3)
    h3 = ax3.hist2d(moon_distance, moon_phase, bins=(100, 200), norm=norm)
    ax3.set_xlabel("Moon Distance (degrees)")
    ax3.set_ylabel("Moon Phase")
    plt.colorbar(h3[3], ax=ax3)

    ax4 = fig1.add_subplot(2, 2, 4)
    h4 = ax4.hist2d(moon_phase, sky_brightness, bins=(200, 100), norm=norm)
    ax4.set_xlabel("Moon Phase")
    ax4.set_ylabel("Sky Brightness ($mags/arcsec^2$)")
    plt.colorbar(h4[3], ax=ax4)

    u_idxs = numpy.where(band_filter == 'u')
    g_idxs = numpy.where(band_filter == 'g')
    r_idxs = numpy.where(band_filter == 'r')
    i_idxs = numpy.where(band_filter == 'i')
    z_idxs = numpy.where(band_filter == 'z')
    y_idxs = numpy.where(band_filter == 'y')

    fig2 = plt.figure(figsize=(11, 8))
    fig2.suptitle("Moon Distance Per Filter Information")

    ax10 = fig2.add_subplot(2, 3, 1)
    ax10.hist(moon_distance[u_idxs], bins=100, log=args.log)
    ax10.set_xlabel("Moon Distance (degrees)")
    ax10.set_title("u Filter")

    ax11 = fig2.add_subplot(2, 3, 2)
    ax11.hist(moon_distance[g_idxs], bins=100, log=args.log)
    ax11.set_xlabel("Moon Distance (degrees)")
    ax11.set_title("g Filter")

    ax12 = fig2.add_subplot(2, 3, 3)
    ax12.hist(moon_distance[r_idxs], bins=100, log=args.log)
    ax12.set_xlabel("Moon Distance (degrees)")
    ax12.set_title("r Filter")

    ax13 = fig2.add_subplot(2, 3, 4)
    ax13.hist(moon_distance[i_idxs], bins=100, log=args.log)
    ax13.set_xlabel("Moon Distance (degrees)")
    ax13.set_title("i Filter")

    ax14 = fig2.add_subplot(2, 3, 5)
    ax14.hist(moon_distance[z_idxs], bins=100, log=args.log)
    ax14.set_xlabel("Moon Distance (degrees)")
    ax14.set_title("z Filter")

    ax15 = fig2.add_subplot(2, 3, 6)
    ax15.hist(moon_distance[y_idxs], bins=100, log=args.log)
    ax15.set_xlabel("Moon Distance (degrees)")
    ax15.set_title("y Filter")

    fig2.subplots_adjust(left=0.07, right=0.95, top=0.93, bottom=0.1, hspace=0.3, wspace=0.2)

    fig3 = plt.figure(figsize=(12, 8))
    fig3.suptitle("Sky Brightness vs Moon Distance Per Filter Information")

    ax20 = fig3.add_subplot(2, 3, 1)
    h20 = ax20.hist2d(sky_brightness[u_idxs], moon_distance[u_idxs], bins=(100, 100), norm=norm)
    ax20.set_xlabel("Sky Brightness ($mags/arcsec^2$)")
    ax20.set_ylabel("Moon Distance (degrees)")
    ax20.set_title("u Filter")
    plt.colorbar(h20[3], ax=ax20)

    ax21 = fig3.add_subplot(2, 3, 2)
    h21 = ax21.hist2d(sky_brightness[g_idxs], moon_distance[g_idxs], bins=(100, 100), norm=norm)
    ax21.set_xlabel("Sky Brightness ($mags/arcsec^2$)")
    ax21.set_ylabel("Moon Distance (degrees)")
    ax21.set_title("g Filter")
    plt.colorbar(h21[3], ax=ax21)

    ax22 = fig3.add_subplot(2, 3, 3)
    h22 = ax22.hist2d(sky_brightness[r_idxs], moon_distance[r_idxs], bins=(100, 100), norm=norm)
    ax22.set_xlabel("Sky Brightness ($mags/arcsec^2$)")
    ax22.set_ylabel("Moon Distance (degrees)")
    ax22.set_title("r Filter")
    plt.colorbar(h22[3], ax=ax22)

    ax23 = fig3.add_subplot(2, 3, 4)
    h23 = ax23.hist2d(sky_brightness[i_idxs], moon_distance[i_idxs], bins=(100, 100), norm=norm)
    ax23.set_xlabel("Sky Brightness ($mags/arcsec^2$)")
    ax23.set_ylabel("Moon Distance (degrees)")
    ax23.set_title("i Filter")
    plt.colorbar(h23[3], ax=ax23)

    ax24 = fig3.add_subplot(2, 3, 5)
    h24 = ax24.hist2d(sky_brightness[z_idxs], moon_distance[z_idxs], bins=(100, 100), norm=norm)
    ax24.set_xlabel("Sky Brightness ($mags/arcsec^2$)")
    ax24.set_ylabel("Moon Distance (degrees)")
    ax24.set_title("z Filter")
    plt.colorbar(h24[3], ax=ax24)

    ax25 = fig3.add_subplot(2, 3, 6)
    h25 = ax25.hist2d(sky_brightness[y_idxs], moon_distance[y_idxs], bins=(100, 100), norm=norm)
    ax25.set_xlabel("Sky Brightness ($mags/arcsec^2$)")
    ax25.set_ylabel("Moon Distance (degrees)")
    ax25.set_title("y Filter")
    plt.colorbar(h25[3], ax=ax25)

    fig3.subplots_adjust(left=0.07, right=0.95, top=0.93, bottom=0.1, hspace=0.3, wspace=0.3)

    file_head = os.path.basename(args.dbfile).split('.')[0]
    middle_tag1 = "_moon_info"
    middle_tag2 = "_moon_info_filter"
    middle_tag3 = "_moon_sb_info_filter"
    if args.log:
        middle_tag1 += "_logscale"
        middle_tag2 += "_logscale"
        middle_tag3 += "_logscale"

    fig1.savefig(file_head + middle_tag1 + ".png")
    fig2.savefig(file_head + middle_tag2 + ".png")
    fig3.savefig(file_head + middle_tag3 + ".png")

    if args.interactive:
        plt.show()
