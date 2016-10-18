Simple Plotting
===============

This directory contains scripts that allow for simple plotting.

Requirements
------------

The scripts use the plotting harness from MAF (*sims_maf*), so therefore depend on that package. The *numpy* package is also required, but that is a dependency of *sims_maf*. The *sims_survey_fields* package is required as well. 

Scripts
-------

``plot_footprint.py``: This scripts plots various *OpSim* proposal sky regions by using the new style selection mechanism from the *sims_survey_fields* package and plots them via MAF.

``utilities.py``: This is not intended to be used as a script, but an importable module to get the plotting functionality. The ``plot_fields`` function requires two dictionaries, one containing right ascension and the other containing declination. The keys can be any name and will be displayed on the resulting plot. The typical convention is to use proposal names. The last required parameter is a center for the right ascension on the plot. 