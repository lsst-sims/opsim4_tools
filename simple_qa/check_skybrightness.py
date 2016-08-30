import argparse
import sqlite3

import numpy

from lsst.sims.skybrightness import SkyModel
from lsst.sims.utils import Site
from ts_scheduler.observatoryModel import ObservatoryLocation
from ts_scheduler.sky_model import DateProfile

DB_FIELDS = ",".join(["requestTime", "ra", "dec", "skyBrightness", "filter"])

def main(opts):
    use_limit = opts.limit > 0

    sb = SkyModel(mags=True)
    lsst = Site(name="LSST")
    ol = ObservatoryLocation(lsst.latitude_rad, lsst.longitude_rad, lsst.height)
    dp = DateProfile(0, ol)

    with sqlite3.connect(opts.dbfile) as conn:
        cur = conn.cursor()
        query = "select {} from TargetHistory".format(DB_FIELDS)
        if use_limit:
            query += " limit {}".format(args.limit)
        query += ";"

        cur.execute(query)
        for row in cur:
            dp.update(row[0])
            sb.setRaDecMjd(numpy.radians(numpy.array([row[1]])), numpy.radians(numpy.array([row[2]])), dp.mjd)
            mags = sb.returnMags()
            print("MJD = {}".format(dp.mjd))
            print("(RA, Dec) = ({}, {})".format(row[1], row[2]))
            print("Sky Brightness for Band Filter {} = {}".format(row[4], row[3]))
            for k, v in mags.items():
                print("Sky Brightness for Band Filter {} = {}".format(k, v[0]))
            print()

if __name__ == "__main__":

    description = ["Python script to the sky brightness agains an OpSim run."]

    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-l", "--limit", default=0, help="Look at the first N fields.")
    parser.set_defaults()
    args = parser.parse_args()

    main(args)
