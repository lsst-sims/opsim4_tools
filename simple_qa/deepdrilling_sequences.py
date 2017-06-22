import argparse
import collections
import numpy
import pandas as pd
from sqlalchemy import create_engine

SECONDS_IN_DAY = 3600.0 * 24.0

def get_config_info(c, si, cc, pn, p):
    r = c.execute("select paramName, paramValue from Config where paramName "
                  "like \"%{}%sequence%{}%\"".format(pn, p))
    rows = r.fetchall()
    for row in rows:
        index = int(row[0].split('/')[-2])
        seq_name = si[index]
        if p == "filters":
            cc[seq_name][p] = [x.strip().strip('\'')for x in row[1].strip('[]').split(',')]
        else:
            cc[seq_name][p] = float(row[1])

def get_information(k, n, c, v=False):
    print("Observations: {}".format(n.size))
    diff = nights[1:] - nights[:-1]

    info = c[k]
    num_events = int(info["num_events"])
    start_window = info["window_start"] * info["time_interval"] / SECONDS_IN_DAY
    end_window = info["window_end"] * info["time_interval"] / SECONDS_IN_DAY
    diff = n[1:] - n[:-1]

    print("Mean days between obs: {}".format(numpy.mean(diff)))
    print("Median days between obs: {}".format(numpy.median(diff)))

    complete_sequences = 0
    attempts = 0
    count = 0
    for d in diff:
        if start_window <= d <= end_window:
            if count:
                count += 1
            else:
                count = 2
        else:
            count = 0
            attempts += 1

        if count == num_events:
            count = 0
            complete_sequences += 1
            attempts += 1

    print("Number of completed sequences: {}".format(complete_sequences))
    print("Number of attempts: {}".format(attempts))
    if v:
        print("Inter-observation time (days)")
        print(diff)

if __name__ == "__main__":
    description = ["Python script to plot runtime per night and print statistics."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim4 SQLite database file.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.add_argument("-p", dest="proposal_id", default=5,
                        help="Specify the proposal Id for the SQL query.")
    parser.add_argument("-v", dest="verbose", action="store_true", default=False,
                        help="Print out inter-observation time differences. WARNING: Could be large!.")

    parser.set_defaults()
    args = parser.parse_args()

    engine = create_engine("sqlite:///{}".format(args.dbfile))

    select_sql = "select night, observationStartMJD, "\
                 "groupId, Field_fieldId as fieldId, altitude, azimuth, filter from "\
                 "ObsHistory, ObsProposalHistory where "\
                 "ObsProposalHistory.ObsHistory_observationId = ObsHistory.observationId and "\
                 "ObsProposalHistory.Proposal_propId={}".format(args.proposal_id)
    #print(select_sql)

    data = None
    config = collections.defaultdict(dict)
    with engine.connect() as conn, conn.begin():
        r = conn.execute("select propName from Proposal where propId={}".format(args.proposal_id))
        row = r.fetchone()
        prop_name = row[0]
        r = conn.execute("select paramName, paramValue from Config where paramName "
                         "like \"%{}%sequence%name%\"".format(prop_name))
        rows = r.fetchall()
        sequence_index = {}
        for row in rows:
            index = int(row[0].split('/')[-2])
            sequence_index[index] = row[1]
            config[row[1]] = {}
        params = ["filters", "num_events", "time_interval", "window_start", "window_end"]
        for param in params:
            get_config_info(conn, sequence_index, config, prop_name, param)

        data = pd.read_sql_query(select_sql, conn)

    #print(config)
    data["filter"] = data["filter"].str.strip()
    fieldIds = data["fieldId"].values
    unique_fields = numpy.unique(fieldIds)

    sequences = collections.OrderedDict()

    #print(unique_fields)
    for fieldId in unique_fields:
        sequences[fieldId] = collections.defaultdict(dict)
        for name in sequence_index.values():
            filter_list = config[name]["filters"]
            subdata = data[(data.fieldId == fieldId) & (data["filter"].isin(filter_list))]
            nights = subdata["night"].values
            unique_nights, unique_night_indexes = numpy.unique(nights, return_index=True)
            unique_mjds = subdata["observationStartMJD"].values[unique_night_indexes]
            sequences[fieldId][name] = unique_mjds

    #print(sequences)

    for fieldId, value in sequences.items():
        print("Field {}".format(fieldId))
        for name, nights in value.items():
            print(name)
            get_information(name, nights, config, args.verbose)
