import os
import argparse
import collections
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
# To plot the output
import lsst.sims.maf.slicers as slicers
import lsst.sims.maf.plots as plots
import lsst.sims.utils as simsUtils

from ts_scheduler.fields import FieldsDatabase, FieldSelection

def get_arrays(results):
    ra = []
    dec = []

    for row in results:
        ra.append(row[2])
        dec.append(row[3])

    return (np.array(ra), np.array(dec))

def get_scp(fd, fs, reach):
    query1 = fs.select_region("fieldDec", -90.0, -62.5)
    query2 = fs.galactic_region(10.0, 0.0, 90.0)
    query = fs.combine_queries(('and',), query1, query2)
    ra, dec = get_arrays(fd.query(query))
    return ("SouthCelestialPole", ra, dec)

def get_gp(fd, fs, reach):
    query0 = fs.select_region("fieldDec", *reach)
    query1 = fs.galactic_region(10.0, 0.0, 90.0, exclusion=False)
    query = fs.combine_queries(('and',), query0, query1)
    ra, dec = get_arrays(fd.query(query))
    return ("GalacticPlane", ra, dec)

def get_wfd(fd, fs, reach):
    query0 = fs.select_region("fieldDec", *reach)
    query1 = fs.select_region("fieldDec", -62.5, 2.8)
    query2 = fs.galactic_region(10.0, 0.0, 90.0)
    query = fs.combine_queries(('and', 'and'), query0, query1, query2)
    ra, dec = get_arrays(fd.query(query))
    return ("WideFastDeep", ra, dec)

def get_nes(fd, fs, reach):
    query1 = fs.select_region("fieldEB", -30.0, 10.0)
    query2 = fs.select_region("fieldDec", 2.8, 90.0)
    query = fs.combine_queries(('and',), query1, query2)
    ra, dec = get_arrays(fd.query(query))
    return ("NorthEclipticSpur", ra, dec)

def get_dd(fd, fs, reach):
    user_regions = ((0.01, -45.5), (34.39, -5.1), (53.0, -27.34), (150.0, 2.84), (349.4, -63.3))
    ra = [x[0] for x in user_regions]
    dec = [x[1] for x in user_regions]
    return ("DDCosmology", np.array(ra), np.array(dec))

def get_eb15(fd, fs, reach):
    # Full band
    query1 = fs.select_region("fieldEB", -15.0, 15.0)
    # Adding NES bump
    query2 = fs.select_region("fieldEB", -30.0, -15.0)
    query3 = fs.select_region("fieldDec", 2.8, 90.0)
    query = fs.combine_queries(('or', 'and'), query1, query2, query3)
    ra, dec = get_arrays(fd.query(query))
    return ("EclipticBand-15", ra, dec)

def get_eb12(fd, fs, reach):
    # Full band
    query1 = fs.select_region("fieldEB", -12.0, 12.0)
    # Adding NES bump
    query2 = fs.select_region("fieldEB", -30.0, -12.0)
    query3 = fs.select_region("fieldDec", 2.5, 90.0)
    query = fs.combine_queries(('or', 'and'), query1, query2, query3)
    ra, dec = get_arrays(fd.query(query))
    return ("EclipticBand-12", ra, dec)

def get_eb10(fd, fs, reach):
    # Full band
    query1 = fs.select_region("fieldEB", -10.0, 10.0)
    # Adding NES bump
    query2 = fs.select_region("fieldEB", -30.0, -10.0)
    query3 = fs.select_region("fieldDec", 2.0, 90.0)
    query = fs.combine_queries(('or', 'and'), query1, query2, query3)
    ra, dec = get_arrays(fd.query(query))
    return ("EclipticBand-10", ra, dec)

def plot_fields(fieldRA, fieldDec, raCenter):
    slicer = slicers.OpsimFieldSlicer()
    fignum = None
    colorlist = [[1, 0, 0], [1, 1, 0], [0, 1, 0], [0, .25, .5],
                 [.5, 0, .5], [0, 0, 0], [.5, .5, 1]]
    ci = 0
    colors = {}
    for prop in fieldRA:
        # Modify slicer so we can use it for plotting.
        slicer.slicePoints['ra'] = np.radians(fieldRA[prop])
        #print(slicer.slicePoints['ra'][0])
        slicer.slicePoints['dec'] = np.radians(fieldDec[prop])
        #print(slicer.slicePoints['dec'][0])
        fieldLocs = ma.MaskedArray(data=np.empty(len(fieldRA[prop]), object),
                                   mask=np.zeros(len(fieldRA[prop]), bool),
                                   fill_value=-99)
        colors[prop] = [colorlist[ci][0], colorlist[ci][1], colorlist[ci][2], 0.4]
        ci += 1
        if ci == len(colorlist):
            ci = 0
        for i in xrange(len(fieldRA[prop])):
            fieldLocs.data[i] = colors[prop]
        skymap = plots.BaseSkyMap()
        fignum = skymap(fieldLocs, slicer,
                        {'metricIsColor': True, 'bgcolor': 'lightgray', 'raCen': raCenter},
                        fignum=fignum)
    plt.figure(fignum)
    labelcolors = []
    labeltext = []
    for prop in fieldRA:
        el = Ellipse((0, 0), 0.03, 0.03,
                     fc=(colors[prop][0], colors[prop][1], colors[prop][2]),
                     alpha=colors[prop][3])
        labelcolors.append(el)
        labeltext.append(prop.rstrip('.conf'))
    plt.legend(labelcolors, labeltext, loc=(0.85, 0.9), fontsize='smaller')
    plt.show()

if __name__ == "__main__":

    description = ["Python script to plot the expected footprint of a configuration."]

    parser = argparse.ArgumentParser(description=" ".join(description))
    parser.add_argument("--ra-center", dest="ra_center", type=float, default=0.0,
                        help="Set the RA (degrees) center of the plot.")

    parser.set_defaults()
    args = parser.parse_args()

    fieldRA = collections.OrderedDict()
    fieldDec = collections.OrderedDict()

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

    lsst_site = simsUtils.Site(name='LSST')
    min_dec = lsst_site.latitude - 90.0
    max_dec = lsst_site.latitude + 90.0
    print("Reach:", min_dec, max_dec)

    for func in proposal_funcs:
        name, ra, dec = func(field_db, field_select, (min_dec, max_dec))
        print("{}: ({}, {})".format(name, len(ra), len(dec)))
        #un, un_cnts = np.unique(ra, return_counts=True)
        #print(un, un_cnts)
        #print(np.where(un_cnts > 1))
        fieldRA[name] = ra
        fieldDec[name] = dec

    # Check their locations on a plot.
    plot_fields(fieldRA, fieldDec, np.radians(args.ra_center))
