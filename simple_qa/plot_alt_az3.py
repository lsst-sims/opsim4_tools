import matplotlib.pyplot as plt
import numpy
import pandas as pd
from sqlalchemy import create_engine
import sys

def get_data_frame(dbpath):
    engine = create_engine("sqlite:///{}".format(dbpath))
    select_sql = "select altitude, azimuth from ObsHistory;"
    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_query(select_sql, conn)
    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage python plot_az.py <run db>")
        sys.exit(255)

    run = get_data_frame(sys.argv[1])

    azimuth = numpy.degrees(run['azimuth'].values)
    altitude = numpy.degrees(run['altitude'].values)

    plt.hist2d(azimuth, altitude, bins=40)
    plt.xlabel("Azimuth (degrees))")
    plt.ylabel("Altitude (degrees)")
    plt.show()
