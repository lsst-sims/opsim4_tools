import argparse
import math
import SALPY_scheduler
import sqlite3
import sys
import time

SQL_4 = "select night, observationStartMJD, observationStartLST, filter, ra, dec, altitude, azimuth, "\
        "numExposures, moonAlt, moonAz, moonPhase, sunAlt from ObsHistory"

SQL_3 = "select night, expMJD, lst, filter, Field.fieldRA, Field.fieldDec, altitude, azimuth, "\
        "moonAlt, moonAZ, moonPhase, sunAlt from ObsHistory, Field"

SQL_3_WHERE = " where ObsHistory.Field_fieldID = Field.fieldID"

if __name__ == "__main__":

    description = ["Python script to serve an OpSim4 SQLite database like a DDS event stream."]

    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-l", "--limit", default=0, help="Look at the first N fields.")
    parser.add_argument("-3", dest="v3", action="store_true", default=False, help="Query an OpSim v3 DB.")
    parser.add_argument("-n", "--night", nargs="*", default=[], type=int,
                        help="Set the night or night range (min, max) to view.")
    parser.set_defaults()
    args = parser.parse_args()

    use_limit = args.limit > 0

    try:
        manager = SALPY_scheduler.SAL_scheduler()
        manager.setDebugLevel(0)
        manager.salTelemetryPub("scheduler_observation")
        obs = SALPY_scheduler.scheduler_observationC()
        num_obs = 0

        with sqlite3.connect(args.dbfile) as conn:
            cur = conn.cursor()
            if args.v3:
                query = SQL_3
            else:
                query = SQL_4

            night_query = None
            if len(args.night):
                try:
                    min_night = args.night[0]
                    max_night = args.night[1]
                    night_query = " (night>={} and night<={})".format(min_night, max_night)
                except IndexError:
                    night = args.night[0]
                    night_query = " night={}".format(night)
            if night_query is not None:
                if args.v3:
                    query += SQL_3_WHERE + " and" + night_query
                else:
                    query += " where" + night_query
            else:
                if args.v3:
                    query += SQL_3_WHERE

            if use_limit:
                query += " limit {}".format(args.limit)
            query += ";"

            cur.execute(query)
            for row in cur:
                obs.night = row[0]
                obs.observation_start_mjd = row[1]
                obs.filter = str(row[3])
                obs.ra = row[4]
                obs.dec = row[5]
                if not args.v3:
                    obs.observation_start_lst = row[2]
                    obs.altitude = row[6]
                    obs.azimuth = row[7]
                    obs.num_exposures = row[8]
                    obs.moon_alt = row[9]
                    obs.moon_az = row[10]
                    obs.moon_phase = row[11]
                    obs.sun_alt = row[12]
                else:
                    obs.observation_start_lst = math.degrees(row[2])
                    obs.altitude = math.degrees(row[6])
                    obs.azimuth = math.degrees(row[7])
                    obs.num_exposures = 2
                    obs.moon_alt = math.degrees(row[8])
                    obs.moon_az = math.degrees(row[9])
                    obs.moon_phase = row[10]
                    obs.sun_alt = math.degrees(row[11])

                manager.putSample_observation(obs)
                num_obs += 1
                time.sleep(0.1)
            cur.close()

        manager.salShutdown()
        print("Number of observations sent: {}".format(num_obs))

    except KeyboardInterrupt:
        manager.salShutdown()
        sys.exit(0)
