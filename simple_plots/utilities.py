import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import lsst.sims.maf.slicers as slicers
import lsst.sims.maf.plots as plots

def plot_fields(field_ra, field_dec, options):
    ra_center = np.radians(options.ra_center)
    slicer = slicers.OpsimFieldSlicer()
    fignum = None
    colorlist = [[1, 0, 0], [1, 1, 0], [0, 1, 0], [0, .25, .5],
                 [.5, 0, .5], [0, 0, 0], [.5, .5, 1]]
    ci = 0
    colors = {}
    for prop in field_ra:
        # Modify slicer so we can use it for plotting.
        slicer.slicePoints['ra'] = np.radians(field_ra[prop])
        slicer.slicePoints['dec'] = np.radians(field_dec[prop])

        fieldLocs = ma.MaskedArray(data=np.empty(len(field_ra[prop]), object),
                                   mask=np.zeros(len(field_ra[prop]), bool),
                                   fill_value=-99)
        colors[prop] = [colorlist[ci][0], colorlist[ci][1], colorlist[ci][2], 0.4]
        ci += 1
        if ci == len(colorlist):
            ci = 0
        for i in range(len(field_ra[prop])):
            fieldLocs.data[i] = colors[prop]
        skymap = plots.BaseSkyMap()
        fignum = skymap(fieldLocs, slicer,
                        {'metricIsColor': True, 'bgcolor': 'lightgray', 'raCen': ra_center},
                        fignum=fignum)

    labelcolors = []
    labeltext = []
    for prop in field_ra:
        el = Ellipse((0, 0), 0.03, 0.03,
                     fc=(colors[prop][0], colors[prop][1], colors[prop][2]),
                     alpha=colors[prop][3])
        labelcolors.append(el)
        labeltext.append(prop.rstrip('.conf'))
    plt.legend(labelcolors, labeltext, loc=(0.85, 0.9), fontsize='smaller')
    if not options.save_fig:
        plt.show()
    else:
        print("Saving figure")
        plt.savefig('LSST_Proposal_Sky_Coverage.png', dpi=500)
