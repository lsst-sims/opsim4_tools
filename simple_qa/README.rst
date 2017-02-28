Simple QA
=========

This directory contains scripts made for doing simple quality assurance on *OpSim4* information.

Requirements
------------

``check_runs.py``: numpy, pandas, sqlalchemy

``check_skybrightness.py``: SOCS (*sims_ocs*), Scheduler (*ts_scheduler*), SkyModel (*sky_brightness*), *sims_utils*, *numpy* and all of their dependencies

``find_bad_row.py``: *numpy*

``get_observations_over_time_comp.py``: *numpy*, *pandas*, *sqlalchemy*

``parse_opsim_log.py``: *numpy* 

``plot_bias.py``: *matplotlib*, *numpy*, *pandas*, *sqlalchemy* 

``plot_filter_change_info.py``: *matplotlib*, *multiprocessing*, *numpy*, *pandas*, *sqlalchemy* 

``plot_obs_alt_az.py``: *matplotlib*, *numpy*, *pandas*, *sqlalchemy* 

``plot_observations_over_time.py``: *matplotlib*, *numpy*

``plot_observations_over_time_single.py``: *matplotlib*, *numpy*, *pandas*, *sqlalchemy*

``stats_opsim_log.py``: *matplotlib*, *numpy*

Scripts
-------

``check_runs.py``: This script checks the ordering of the TargetHistory, ObsHistory, SlewHistory and SlewFinalState tables between two OpSim SQLite databases.

``check_skybrightness.py``: This script takes an *OpSim4* results database and compares the sky brightness found in the target history against the sky brightness calculated by the SkyModel class at the same MJD.

``find_bad_row.py``: When *OpSim4* fails on a database write, usually for a nan, a compressed NumPy file is generated for the information that failed the insertion. This script reads that file and returns the column(s) associated with the bad row. The column with the bad value is excluded.

``get_observations_over_time.py``: This script as a SQLite database from either OpSim3 (requires flag) or Opsim4 and gathers the information for all observations over all nights in the standard five proposals.

``get_observations_over_time.py``: This script as a SQLite database from either OpSim3 (requires flag) or Opsim4 and gathers the information for all observations over all nights in the standard five proposals.

``parse_opsim_log.py``: This script parses an *OpSim4* output log to create a NPZ file containing the processing time per night as well as the total simulation running time.

``plot_bias.py``: This script plots the observing bias for a simulation. Two plots are given: The Hour Angle distribution and Azimuth vs Altitude.

``plot_filter_change_info.py``: Plot various quatities associated with filter changes: Changes per Night, Frequency of Changes per Night, Minimum Time Between Filter Changes per Night, Frequency of Minimum Time Between Filter Changes per Night, Number of Filter Changes vs Minimum Time Between Filter Changes.

``plot_obs_alt_az.py``:  Plot Altitude vs Azimuth distributions for both the dome and telescope.

``plot_observations_over_time_comp.py``: This script plots the distributions of observations over nights for the standard five proposals for an OpSim3 and OpSim4 run.

``plot_observations_over_time_single.py``: This script plots the distributions of observations over nights for all proposals in an OpSim4 run.

``stats_opsim_log.py``: This script gathers statistics about the per night processing from the NPZ file create by ``parse_opsim_log.py`` and also plots the Processing Time per Night vs Night.