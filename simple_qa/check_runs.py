from __future__ import print_function
import os
import pandas as pd
from sqlalchemy import create_engine
import sys

def get_data_frame(dbpath):
    engine = create_engine("sqlite:///{}".format(dbpath))
    select_sql = "select targetId, Field_fieldId, filter from TargetHistory;"
    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage python check_runs.py <run db 1> <run db 2>")
        sys.exit(255)

    run1 = get_data_frame(sys.argv[1])
    run2 = get_data_frame(sys.argv[2])

    comp = run1 == run2

    fieldId = comp.all(0)[1]
    band_filter = comp.all(0)[2]
    if fieldId and band_filter:
        print("Databases are the same")
    else:
        if not fieldId:
            bad_fields = ~comp['Field_fieldId']
            print("Out-of-order fields:")
            print(os.path.basename(sys.argv[1]))
            print(run1[bad_fields])
            print(os.path.basename(sys.argv[2]))
            print(run2[bad_fields])
        if not band_filter:
            bad_filters = ~comp['filter']
            print("Out-of-order filters:")
            print(os.path.basename(sys.argv[1]))
            print(run1[bad_filters])
            print(os.path.basename(sys.argv[2]))
            print(run2[bad_filters])
