import argparse
import collections
import numpy as np

from utilities import plot_fields

from lsst.sims.survey.fields import FieldsDatabase, FieldSelection

def get_scp(fd, fs):
    query1 = fs.select_region("Dec", -90.0, -62.5)
    query2 = fs.galactic_region(10.0, 0.0, 90.0, exclusion=True)
    query = fs.combine_queries(query1, query2, combiners=('and',))
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("SouthCelestialPole", ra, dec)

def get_gp(fd, fs):
    query = fs.galactic_region(10.0, 0.0, 90.0)
    query = fs.combine_queries(query)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("GalacticPlane", ra, dec)

def get_wfd(fd, fs):
    query1 = fs.select_region("Dec", -62.5, 2.8)
    query2 = fs.galactic_region(10.0, 0.0, 90.0, exclusion=True)
    query = fs.combine_queries(query1, query2, combiners=('and', ))
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("WideFastDeep", ra, dec)

def get_nes(fd, fs):
    query1 = fs.select_region("EB", -30.0, 10.0)
    query2 = fs.select_region("Dec", 2.8, 90.0)
    query = fs.combine_queries(query1, query2, combiners=('and',))
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("NorthEclipticSpur", ra, dec)

def get_ddc1(fd, fs):
    user_regions = (290, 744, 1427, 2412, 2786)
    query1 = fs.select_user_regions(user_regions)
    query = fs.combine_queries(query1)
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("DDCosmology1", ra, dec)

def get_eb15(fd, fs):
    # Full band
    query1 = fs.select_region("EB", -15.0, 15.0)
    # Adding NES bump
    query2 = fs.select_region("EB", -30.0, -15.0)
    query3 = fs.select_region("Dec", 2.8, 90.0)
    query = fs.combine_queries(query1, query2, query3,
                               combiners=('or', 'and'))
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("EclipticBand-15", ra, dec)

def get_eb12(fd, fs):
    # Full band
    query1 = fs.select_region("EB", -12.0, 12.0)
    # Adding NES bump
    query2 = fs.select_region("EB", -30.0, -12.0)
    query3 = fs.select_region("Dec", 2.5, 90.0)
    query = fs.combine_queries(query1, query2, query3,
                               combiners=('or', 'and'))
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("EclipticBand-12", ra, dec)

def get_eb10(fd, fs):
    # Full band
    query1 = fs.select_region("EB", -10.0, 10.0)
    # Adding NES bump
    query2 = fs.select_region("EB", -30.0, -10.0)
    query3 = fs.select_region("Dec", 2.0, 90.0)
    query = fs.combine_queries(query1, query2, query3,
                               combiners=('or', 'and'))
    ra, dec = fd.get_ra_dec_arrays(query)
    return ("EclipticBand-10", ra, dec)

if __name__ == "__main__":

    description = ["Python script to plot the expected footprint of a "]
    description.append("configuration.")

    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("--ra-center", dest="ra_center", type=float,
                        default=0.0,
                        help="Set the RA (degrees) center of the plot.")
    parser.add_argument("--save-fig", dest="save_fig", action="store_true",
                        default=False,
                        help="Save the figure instead of showing it.")

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
    proposal_funcs.append(get_ddc1)
    # proposal_funcs.append(get_eb15)
    # proposal_funcs.append(get_eb12)
    # proposal_funcs.append(get_eb10)

    for func in proposal_funcs:
        name, ra, dec = func(field_db, field_select)
        print("{}: ({}, {})".format(name, len(ra), len(dec)))
        field_ra[name] = ra
        field_dec[name] = dec

    # Check their locations on a plot.
    plot_fields(field_ra, field_dec, args)
