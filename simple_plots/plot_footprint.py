import argparse
import collections
import numpy as np

from utilities import plot_fields

from lsst.sims.survey.fields import FieldsDatabase, FieldSelection

def get_scp(fd, fs):
    query1 = fs.select_region("fieldDec", -90.0, -62.5)
    query2 = fs.galactic_region(10.0, 0.0, 90.0)
    query = fs.combine_queries(('and',), query1, query2)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("SouthCelestialPole", ra, dec)

def get_gp(fd, fs):
    query = fs.galactic_region(10.0, 0.0, 90.0, exclusion=False)
    query = fs.combine_queries((), query)
    print(query)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("GalacticPlane", ra, dec)

def get_wfd(fd, fs):
    query1 = fs.select_region("fieldDec", -62.5, 2.8)
    query2 = fs.galactic_region(10.0, 0.0, 90.0)
    query = fs.combine_queries(('and', ), query1, query2)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("WideFastDeep", ra, dec)

def get_nes(fd, fs):
    query1 = fs.select_region("fieldEB", -30.0, 10.0)
    query2 = fs.select_region("fieldDec", 2.8, 90.0)
    query = fs.combine_queries(('and',), query1, query2)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("NorthEclipticSpur", ra, dec)

def get_dd(fd, fs):
    user_regions = ((0.01, -45.5), (34.39, -5.1), (53.0, -27.34), (150.0, 2.84), (349.4, -63.3))
    ra = [x[0] for x in user_regions]
    dec = [x[1] for x in user_regions]
    return ("DDCosmology", np.array(ra), np.array(dec))

def get_eb15(fd, fs):
    # Full band
    query1 = fs.select_region("fieldEB", -15.0, 15.0)
    # Adding NES bump
    query2 = fs.select_region("fieldEB", -30.0, -15.0)
    query3 = fs.select_region("fieldDec", 2.8, 90.0)
    query = fs.combine_queries(('or', 'and'), query1, query2, query3)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("EclipticBand-15", ra, dec)

def get_eb12(fd, fs):
    # Full band
    query1 = fs.select_region("fieldEB", -12.0, 12.0)
    # Adding NES bump
    query2 = fs.select_region("fieldEB", -30.0, -12.0)
    query3 = fs.select_region("fieldDec", 2.5, 90.0)
    query = fs.combine_queries(('or', 'and'), query1, query2, query3)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("EclipticBand-12", ra, dec)

def get_eb10(fd, fs):
    # Full band
    query1 = fs.select_region("fieldEB", -10.0, 10.0)
    # Adding NES bump
    query2 = fs.select_region("fieldEB", -30.0, -10.0)
    query3 = fs.select_region("fieldDec", 2.0, 90.0)
    query = fs.combine_queries(('or', 'and'), query1, query2, query3)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("EclipticBand-10", ra, dec)

if __name__ == "__main__":

    description = ["Python script to plot the expected footprint of a configuration."]

    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("--ra-center", dest="ra_center", type=float, default=0.0,
                        help="Set the RA (degrees) center of the plot.")

    parser.set_defaults()
    args = parser.parse_args()

    field_ra = collections.OrderedDict()
    field_dec = collections.OrderedDict()

    field_select = FieldSelection()
    field_db = FieldsDatabase()

    proposal_funcs = []
    proposal_funcs.append(get_gp)
    proposal_funcs.append(get_wfd)
    proposal_funcs.append(get_scp)
    proposal_funcs.append(get_nes)
    proposal_funcs.append(get_dd)
    # proposal_funcs.append(get_eb15)
    # proposal_funcs.append(get_eb12)
    # proposal_funcs.append(get_eb10)

    for func in proposal_funcs:
        name, ra, dec = func(field_db, field_select)
        print("{}: ({}, {})".format(name, len(ra), len(dec)))
        field_ra[name] = ra
        field_dec[name] = dec

    # Check their locations on a plot.
    plot_fields(field_ra, field_dec, np.radians(args.ra_center))
