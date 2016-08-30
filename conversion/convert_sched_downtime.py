import collections
try:
    from itertools import zip_longest as izip_longest
except ImportError:
    from itertools import izip_longest
import os
import sqlite3
import sys

if __name__ == "__main__":
    infile = sys.argv[1]

    data = collections.defaultdict(list)

    with open(infile, 'r') as ifile:
        for iline in ifile:
            line = iline.strip()
            if line.startswith("#") or line.startswith(os.linesep):
                continue
            values = line.split()
            try:
                name = values[0]
                try:
                    val = int(values[2])
                except ValueError:
                    val = " ".join(values[2:])

                data[name].append(val)
            except IndexError:
                pass

    records = []
    for night, duration, activity in izip_longest(data["startNight"], data["duration"], data["activity"]):
        records.append((night, duration, activity))

    downtime_dbfile = "unscheduled_downtime_alt.db"

    downtime_table = []
    downtime_table.append("night INTEGER PRIMARY KEY")
    downtime_table.append("duration INTEGER")
    downtime_table.append("activity TEXT")

    conn = sqlite3.connect(downtime_dbfile)
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Downtime")
        cur.execute("CREATE TABLE Downtime({})".format(",".join(downtime_table)))
        cur.executemany("INSERT INTO Downtime VALUES(?, ?, ?)", records)
        cur.close()
