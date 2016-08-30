import argparse
import os
import sqlite3

def run(opts):

    if opts.clouds:
        table_name = "Cloud"
        out_file_name = "cloud.db"
        column_names = ["cloudId", "c_date", "cloud"]
    if opts.seeing:
        table_name = "Seeing"
        out_file_name = "seeing.db"
        column_names = ["seeingId", "s_date", "seeing"]

    records = []
    with sqlite3.connect(os.path.expanduser(opts.dbfile)) as conn:
        cur = conn.cursor()
        query = "select * from {};".format(table_name)
        cur.execute(query)
        lines = 1
        for row in cur:
            records.append((lines, row[1], row[2]))
            lines += 1
        cur.close()

    with sqlite3.connect(out_file_name) as conn1:
        table = []
        table.append("{} INTEGER PRIMARY KEY".format(column_names[0]))
        table.append("{} INTEGER".format(column_names[1]))
        table.append("{} DOUBLE".format(column_names[2]))
        cur1 = conn1.cursor()
        cur1.execute("DROP TABLE IF EXISTS {}".format(table_name))
        cur1.execute("CREATE TABLE {}({})".format(table_name, ",".join(table)))
        cur1.executemany("INSERT INTO {} VALUES(?, ?, ?)".format(table_name), records)
        cur1.close()

if __name__ == '__main__':
    description = []
    parser = argparse.ArgumentParser(usage="convert_weather.py [options]",
                                     description=" ".join(description),
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("dbfile", help="The full path to the OpSim SQLite database file.")

    type_group = parser.add_mutually_exclusive_group(required=True)
    type_group.add_argument("-c", "--clouds", dest="clouds", action="store_true",
                            help="Convert the Cloud table in an OpSim SQLite file to a standalone file.")
    type_group.add_argument("-s", "--seeing", dest="seeing", action="store_true",
                            help="Convert the Seeing table in an OpSim SQLite file to a standalone file.")

    parser.set_defaults()
    args = parser.parse_args()

    run(args)
