from __future__ import print_function
import numpy
import os
import pandas as pd
from sqlalchemy import create_engine
import sys

def get_data_frame(dbpath, select_sql):
    engine = create_engine("sqlite:///{}".format(dbpath))
    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

def check_order(db1, db2, table_name):
    print("Checking {}".format(table_name))

    sql = "select * from {};".format(table_name)

    run1 = get_data_frame(db1, sql)
    run2 = get_data_frame(db2, sql)

    try:
        comp = run1 == run2
    except ValueError:
        if len(run1) != len(run2):
            print("Databases are not the same length: {}, {}.".format(len(run1), len(run2)))
            if len(run1) > len(run2):
                comp = run1[:len(run2)] == run2
            else:
                comp = run1 == run2[:len(run1)]

    columns = list(comp.columns.values)
    column_comps = []
    for column in columns:
        if "Session_sessionId" in column:
            column_comps.append(True)
        else:
            column_comps.append(comp.all(0)[column])

    cc = numpy.array(column_comps)
    if numpy.all(cc):
        print("Databases are the same")
    else:
        for i, ccomp in enumerate(column_comps):
            if not ccomp:
                column_name = columns[i]
                bad_column = ~comp[column_name]
                print("Out-of-order {}:".format(column_name))
                print(os.path.basename(db1))
                if table_name == "Config":
                    r1 = run1
                    r2 = run2
                else:
                    r1 = run1[column_name]
                    r2 = run2[column_name]
                print(r1[bad_column])
                print(os.path.basename(db2))
                print(r2[bad_column])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage python check_runs.py <run db 1> <run db 2>")
        sys.exit(255)

    check_order(sys.argv[1], sys.argv[2], "Config")
    check_order(sys.argv[1], sys.argv[2], "TargetProposalHistory")
    check_order(sys.argv[1], sys.argv[2], "TargetExposures")
    check_order(sys.argv[1], sys.argv[2], "TargetHistory")
    check_order(sys.argv[1], sys.argv[2], "ObsProposalHistory")
    check_order(sys.argv[1], sys.argv[2], "ObsExposures")
    check_order(sys.argv[1], sys.argv[2], "ObsHistory")
    check_order(sys.argv[1], sys.argv[2], "SlewHistory")
    check_order(sys.argv[1], sys.argv[2], "SlewFinalState")
    check_order(sys.argv[1], sys.argv[2], "SlewInitialState")
    check_order(sys.argv[1], sys.argv[2], "SlewActivities")
    check_order(sys.argv[1], sys.argv[2], "SlewMaxSpeeds")
