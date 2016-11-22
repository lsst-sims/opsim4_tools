from __future__ import print_function
import datetime
import numpy
import os
import sys
import time

def get_timestamp(v):
    # First element is date
    v1 = v[0].split(":")[-1]
    # Second element is time
    v2 = v[1].split(",")
    timestr = v1 + " " + v2[0]
    timeobj = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    return time.mktime(timeobj.timetuple())

try:
    infile = sys.argv[1]
except IndexError:
    print("usage: %s <log filename>" % sys.argv[0])
    sys.exit(-1)

file_head = os.path.basename(infile).replace('.', '_')

with open(infile, "r") as ifile:
    timestamps = []
    for line in ifile:
        if "kernel.Simulator - Night" in line or "Simulator - Ending simulation" in line:
            values = line.split()
            timestamp = get_timestamp(values)
            timestamps.append(timestamp)

        if "opsim4 - Total running time" in line:
            parts = line.split()
            survey_time = float(parts[11])
            # Want it in hours
            survey_time /= 3600.0

try:
    svt = numpy.array([survey_time])
except NameError:
    print("Log missing survey runtime.")
    svt = numpy.array([0])

times = numpy.array(timestamps)
deltas = times[1:] - times[:-1]
with open(file_head + ".npz", 'w') as outfile:
    numpy.savez(outfile, deltas=deltas, survey_time=svt)
