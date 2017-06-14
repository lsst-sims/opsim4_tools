import argparse
import numpy
import pandas as pd
from sqlalchemy import create_engine
import os

PROP_NAMES = {
    "NES": "NorthEclipticSpur",
    "SCP": "SouthCelestialPole",
    "GP": "GalacticPlane"
}

ALT_PROPS = {
    "WFD_opsim3": "Universal",
    "WFD_opsim4": "WideFastDeep",
    "DD_opsim3": "DDcosmology1",
    "DD_opsim4": "DeepDrillingCosmology1"
}

def get_data_frame(engine, prop_id, use_opsim3):
    if not use_opsim3:
        select_sql = "select fieldId, night from SummaryAllProps where proposalId={};".format(prop_id)
    else:
        select_sql = "select fieldID, night from Summary where propID={};".format(prop_id)

    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

if __name__ == "__main__":
    description = ["Python script to get observations over time for all standard."]
    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")
    parser.add_argument("-3", dest="v3", action="store_true", default=False,
                        help="Query an OpSim v3 DB.")
    parser.set_defaults()
    args = parser.parse_args()

    props = ["GP", "SCP", "NES", "WFD", "DD"]
    output_arrays = {}
    engine = create_engine("sqlite:///{}".format(args.dbfile))

    if args.v3:
        file_head = os.path.basename(args.dbfile).split('_sqlite')[0]
    else:
        file_head = os.path.basename(args.dbfile).split('.')[0]

    for prop in props:
        try:
            prop_name = PROP_NAMES[prop]
        except KeyError:
            if args.v3:
                newkey = "{}_opsim3".format(prop)
            else:
                newkey = "{}_opsim4".format(prop)
            prop_name = ALT_PROPS[newkey]

        if args.v3:
            sql = "select propID from Proposal where propConf like \'%{}%\'".format(prop_name)
        else:
            sql = "select propId from Proposal where propName like \'%{}%\'".format(prop_name)
        #print(sql)
        with engine.connect() as conn:
            result = conn.execute(sql)
            prop_id = result.fetchone()[0]
            #print(prop_id)

        run = get_data_frame(engine, prop_id, args.v3)
        if args.v3:
            field_ids = run['fieldID'].values
        else:
            field_ids = run['fieldId'].values
        nights = run['night'].values

        unique_nights, observations = numpy.unique(nights, return_counts=True)

        if args.v3:
            unique_nights += 1

        output_arrays["{}_nights".format(prop)] = unique_nights
        output_arrays["{}_observations".format(prop)] = observations
        #print(unique_nights.size)
        #print(observations.size)

    with open(file_head + "_observations_over_time.npz", 'w') as outfile:
        numpy.savez(outfile, **output_arrays)
