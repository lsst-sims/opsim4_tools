Simple QA
=========

This directory contains scripts made for doing simple quality assurance on *OpSim4* information.

Requirements
------------

``check_skybrightness.py``: SOCS (*sims_ocs*), Scheduler (*ts_scheduler*), SkyModel (*sky_brightness*), *sims_utils*, *numpy* and all of their dependencies

``find_bad_row.py``: *numpy*

Scripts
-------

``check_skybrightness.py``: This script takes an *OpSim4* results database and compares the sky brightness found in the target history against the sky brightness calculated by the SkyModel class at the same MJD.

``find_bad_row.py``: When *OpSim4* fails on a database write, usually for a nan, a compressed NumPy file is generated for the information that failed the insertion. This script reads that file and returns the column(s) associated with the bad row. The column with the bad value is excluded.