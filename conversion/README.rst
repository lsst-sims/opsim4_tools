Conversion
==========

This directory contains scripts that were used to convert *OpSim3* information into *OpSim4*  information.

Requirements
------------

The scripts need no special requirements as all dependencies are provided by the Python standard library.

Scripts
-------

``convert_sched_downtime.py``: This script takes an *OpSim3* downtime configuration file and converts it into a SQLite database.

``convert_weather.py``: This scripts takes the Cloud or Seeing tables from an *OpSim3* results database and converts it into a SQLite database for the given types. The script is designed to convert either cloud or seeing for a given execution.