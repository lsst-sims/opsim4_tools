Live Viewing
============

This directory contains the scripts for being able to perform live viewing on a running *OpSim4* simulation. It also provides a mechanism to serve a SQLite output database file that can be viewed by the same tools.

Requirements
------------

The scripts require the Scheduler SAL topic library. Setup instructions for this can be found in the `SOCS documentation`_. Currently, the viewer scripts require the topic library as well and also *numpy* and *matplotlib*. The server script only requires the topic library.

Scripts
-------

``opsims_live_polar.py``: This script shows the telescope view (altitude, azimuth) of the observations. Its inspiriation is drawn from the Telescope and Site simulator by Dave Mills. The background is black for night and fading/rising blue for twilight. The filter used for the observation is color coded. If the moon is up, it will show on the display. It has been enlarged 6x for visibility and the color code for the phase is white (full) to light gray (new). The new moon end of the color code is capped when the phase drops below 5%. The canvas displays the night and MJD information of the current observation. Also, the moon's phase and an indicator of twilight/night is displayed. The viewer keeps a 10 obeservation list showing the recent history of observations. 

``opsim_live.py``: This script is a sky view (right ascension, declination) of the observations. The rest of the functionality is the same as ``opsim_live_polar.py``. 

``db_server.py``: This script provides a mechanism to serve a SQLite results database as a stream of messages for the live viewers to look at. The script works with both *OpSim3* and *OpSim4* files. The script has a night option which allows a specific night or a range of nights to be served. There is also an option to serve a specifc number of observations.

.. _`SOCS documentation`: https://lsst-sims.github.io/sims_ocs/installation.html#sal-installation