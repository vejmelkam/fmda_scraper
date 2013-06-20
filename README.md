fmda_scraper
============

Prerequisites
-------------
  * python 2.6 or 2.7
  * [xlrd](https://pypi.python.org/pypi/xlrd "xlrd") python package

Description
-----------
A data scraper that retrieves RAWS observations from the MesoWest website and stores them in a format suitable for the [fmda_julia](http://github.com/vejmelka/mfmda_julia "fmda_julia") code.  The MesoWest RAWS network observations are available hourly.

This code has two main functions:
  * retrieve information about a particular RAWS station, including location, elevation and observed quantities
  * download observations for a selected 1 day interval (24 observations for each requested quantity).

Example
-------

The ''describe_stations.sh'' script accepts a file containin a station id per line and retrieves the station
information for each file.  In the fmda_scraper directory, run the following (using the list of example stations
in Colorado):

    ./describe_stations.sh example/example_colorado_stations

This will produce many ''*.info'' files in the current directory, for example ''BAWC2.info'', which contain the following data

    # Info created by scrape_stations.py on 2013-06-19 18:19:07.746994
    BAWC2
    # Station name
    BAILEY
    # Station geo location
    39.3794, -105.338
    # Elevation (meters)
    2432.91
    # Station sensors
    TMP, RELH, SKNT, GUST, DRCT, QFLG, VOLT, FT, FM, TLKE, PEAK, PDIR, PREC, SOLR, ITIM, UTIM, DWP

Lines beginning with # are comments and skipped by the (simple) parser.


To retrieve station observations for the above list of stations for the 24 hours up to 5th of June 2013 6:00 AM (all times are in **GMT**), run
the following script:

    ./retrieve_observations.sh example/example_colorado_stations 2013-06-06_09:00

This will produce `xls` files in the current directory for each station in the form `HRC2_2013-06-06_06:00.xls`, encoding the originating station and the requested date/time.

Note that station obsevations are not available exactly on the hour, in the `BAWC2_2013-06-06_06:00.xls` file, the last observation is at 5:22 AM (GMT).
    

      