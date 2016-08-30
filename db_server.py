import argparse
import SALPY_scheduler
import sqlite3
import sys

DB_FIELDS = ",".join(["night", "observationStartMJD", "observationStartLST", "filter", "ra", "dec",
                      "numExposures"])

if __name__ == "__main__":

    description = ["Python script to serve an OpSim4 SQLite database like a DDS event stream."]

    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-l", "--limit", default=0, help="Look at the first N fields.")
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
            query = "select {} from ObsHistory".format(DB_FIELDS)
            if use_limit:
                query += " limit {}".format(args.limit)
            query += ";"

            cur.execute(query)
            for row in cur:
                obs.night = row[0]
                obs.observation_start_mjd = row[1]
                obs.observation_start_lst = row[2]
                obs.filter = str(row[3])
                obs.ra = row[4]
                obs.dec = row[5]
                obs.num_exposures = row[6]
                manager.putSample_observation(obs)
                num_obs += 1
            cur.close()

        manager.salShutdown()
        print("Number of observations sent: {}".format(num_obs))

    except KeyboardInterrupt:
        manager.salShutdown()
        sys.exit(0)
