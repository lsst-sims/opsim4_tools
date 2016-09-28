import numpy
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python find_bad_row.py <NPZ file> <Column name>")
        sys.exit(255)

    nfile = sys.argv[1]
    col = sys.argv[2]

    npz = numpy.load(nfile)

    idxs = numpy.where(numpy.isnan(npz[col]))
    for idx in idxs:
        print("Index: {}".format(idx))
        for key in npz.keys():
            if col == key:
                continue
            print("{}: {}".format(key, npz[key][idx]))
