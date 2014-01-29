fmda_scraper
============

Prerequisites
-------------
  * python 2.6 or 2.7
  * [xlrd](https://pypi.python.org/pypi/xlrd "xlrd") python package
  * BeautifulSoup 4

Description
-----------

A data scraper that retrieves RAWS observations from the MesoWest website and stores them in a format suitable for the [fmda](http://github.com/vejmelkam/fmda "fmda") python code.  The MesoWest RAWS network observations are available hourly.

This code has two main functions:
  * retrieve information about a particular RAWS station, including location, elevation and observed quantities
  * download observations for a selected 1 day interval (24 observations for each requested quantity).

Example
-------

The ''describe_stations.sh'' script accepts a file containin a station id per line and retrieves the station
information for each file.  In the fmda_scraper directory, run the following (using the list of example stations
in Colorado):

    ./describe_stations.sh example/example_colorado_stations

This will create one ''.info'' file per station in the station LIST in the current directory, for example
''BAWC2.info''.  Each file contains data similar to the following:

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

Lines beginning with # are comments and skipped by the parser in the [fmda](http://github.com/vejmelkam/fmda "fmda") code.


To retrieve station observations for the above list of stations for the 24 hours up to 5th of June 2013 6:00 AM (all times are in **GMT**), run
the following script:

    ./retrieve_observations.sh example/example_colorado_stations 2013-06-06_09:00

This will produce `xls` files in the current directory for each station in the form `HRC2_2013-06-06_06:00.xls`, encoding the originating station and the requested date/time.

Note that station obsevations are not available exactly on the hour, in my `BAWC2_2013-06-06_06:00.xls` file, the last observation is at 5:22 AM (GMT).
    

Converting to obs format
------------------------

The second step before the observations can be used by the [fmda](http://github.com/vejmelkam/fmda "fmda") code is to convert the data into `obs` format.  The `obs` format aggregates possibly multi-day observations and also adds information on the variance of the observations to the observations themselves.

Currently information on the variance of the observations is not available from the network, thus a user-constructed table is used in its place.  An example table is in `examples/example_obs_var_table`.  The table format has the observed quantity name in the first column and the variance (in appropriate units) in the second colum separated by a comma:

    FM, 1e-4
    RELH, 2.5e-3
    TMP, 0.25

This information will be injected into the `obs` files which will aggregate all observations in all `xls` files available for each station.

Run the following to obtain an `obs` file for each station containing the currently downloaded observations:

    ./extract_observations.py example/example_colorado_stations example/example_obs_var_table

Now the working directory will contain one obs file per station.  The obs files contain records of four lines each in the form:

    2013-06-05_21:56 GMT
    TMP, RELH, SKNT, GUST, DRCT, SOLR, PREC, FT, FM, PEAK, PDIR, VOLT, DWP
    7.8, 0.97, 275.35, 4.0, 100.0, 431.0, 13.21, 11.7, 0.18, 4.0, 79.0, 14.1, 7.3
    0.25, 0.0025, nan, nan, nan, nan, nan, nan, 0.0001, nan, nan, nan, nan

The first line is the timestamp in ESMF format with the time zone.  The second line contains the quantity names, the third line the observed values and the fourth line the variances of each observation (retrieved from `example_obs_var_table`).

Note that unknown variances are marked with a `nan`.  Note also that the [fmda](http://github.com/vejmelkam/fmda "fmda") code requires the variance of FM to be a valid variance.

The `info` and `obs` files can then be directly used with the [fmda](http://github.com/vejmelkam/fmda "fmda" as detailed in its documentation.


TODO
----

When station variances are available from some source, this code needs to be updated to properly assign variances to observations depending on the source station.
