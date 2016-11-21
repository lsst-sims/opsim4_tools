Simple QA
=========

This directory contains scripts made for doing simple quality assurance on *OpSim4* information.

Requirements
------------

``check_runs.py``: pandas, sqlalchemy

``check_skybrightness.py``: SOCS (*sims_ocs*), Scheduler (*ts_scheduler*), SkyModel (*sky_brightness*), *sims_utils*, *numpy* and all of their dependencies

``find_bad_row.py``: *numpy*

``parse_opsim_log.py``: *numpy* 

``plot_bias.py``: *matplotlib*, *numpy*, *pandas*, *sqlalchemy* 

``plot_filter_change_info.py``: *matplotlib*, *multiprocessing*, *numpy*, *pandas*, *sqlalchemy* 

``plot_obs_alt_az.py``: *matplotlib*, *numpy*, *pandas*, *sqlalchemy* 

``stats_opsim_log.py``: *matplotlib*, *numpy*

Scripts
-------

``check_runs.py``: This script checks the ordering of the Field_fieldId and filter columns from the TargetHistory table between two OpSim SQLite databases.

``check_skybrightness.py``: This script takes an *OpSim4* results database and compares the sky brightness found in the target history against the sky brightness calculated by the SkyModel class at the same MJD.

``find_bad_row.py``: When *OpSim4* fails on a database write, usually for a nan, a compressed NumPy file is generated for the information that failed the insertion. This script reads that file and returns the column(s) associated with the bad row. The column with the bad value is excluded.

``parse_opsim_log.py``: This script parses an *OpSim4* output log to create a NPZ file containing the processing time per night as well as the total simulation running time.

``plot_bias.py``: This script plots the observing bias for a simulation. Two plots are given: The Hour Angle distribution and Azimuth vs Altitude.

``plot_filter_change_info.py``: Plot various quatities associated with filter changes: Changes per Night, Frequency of Changes per Night, Minimum Time Between Filter Changes per Night, Frequency of Minimum Time Between Filter Changes per Night, Number of Filter Changes vs Minimum Time Between Filter Changes.

``plot_obs_alt_az.py``:  Plot Altitude vs Azimuth distributions for both the dome and telescope.

``stats_opsim_log.py``: This script gathers statistics about the per night processing from the NPZ file create by ``parse_opsim_log.py`` and also plots the Processing Time per Night vs Night.