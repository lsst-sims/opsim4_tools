import argparse
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from sqlalchemy import create_engine
import os

def get_data_frame(engine, prop_id, band_filter=None):
    if band_filter is None:
        select_sql = "select fieldId, night from SummaryAllProps where proposalId={};".format(prop_id)
    else:
        select_sql = "select fieldId, night from SummaryAllProps where (proposalId={} "\
                     "and filter=\'{}\');".format(prop_id, band_filter)
    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

if __name__ == "__main__":
    description = ["Python script to get observations over time for all standard."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-f", "--band-filter", dest="band_filter", help="Plot only from a given filter.")
    parser.add_argument("-i", dest="interactive", action="store_true", default=False,
                        help="Show the finished plot.")
    parser.set_defaults()
    args = parser.parse_args()

    engine = create_engine("sqlite:///{}".format(args.dbfile))

    file_head = os.path.basename(args.dbfile).split('.')[0]

    sql = "select propId, propName from Proposal"
    #print(sql)
    with engine.connect() as conn:
        result = conn.execute(sql)
        values = result.fetchall()
    #print(values)
    num_props = len(values)
    rows = 3
    cols = 2
    fig = plt.figure(figsize=(10, 10))

    for (prop_id, prop_name) in values:
        run = get_data_frame(engine, prop_id, args.band_filter)
        field_ids = run['fieldId'].values
        nights = run['night'].values

        unique_nights, observations = numpy.unique(nights, return_counts=True)

        ax1 = fig.add_subplot(rows, cols, prop_id)
        ax1.plot(unique_nights, observations, 'o')
        if args.band_filter is None:
            ax1.set_title(prop_name)
        else:
            ax1.set_title("{}, Filter {}".format(prop_name, args.band_filter))
        ax1.set_xlabel("Night")
        ax1.set_ylabel("Observations")
        ax1.set_xlim(1, 3650)

    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, wspace=0.29, hspace=0.36)

    file_head = os.path.basename(args.dbfile).split('.')[0]
    middle_tag = "_observations_over_time"
    if args.band_filter is not None:
        middle_tag += "_filter_{}".format(args.band_filter)
    plt.savefig(file_head + middle_tag + ".png")

    if args.interactive:
        plt.show()
