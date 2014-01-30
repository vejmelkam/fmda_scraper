#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys
import urllib
import time
from datetime import datetime
import string
import os
from mwest_utils import decode_obs_xls,write_plain_format,retrieve_web_page

# mesowest list of stations
mesowest_dl_url = 'http://mesowest.utah.edu/cgi-bin/droman/meso_download_mesowest_ndb.cgi'

# format of timestamp
tstamp_fmt = '%Y-%m-%d_%H:%M'

# renaming dictionary handling differences between variable names in xls files from Mesowest
# and in the variable listing
renames = { 'TMPF' : 'TMP', 'DWPF' : 'DWP' }
inv_renames = { 'TMP' : 'TMPF', 'DWP' : 'DWPF'}


def download_station_data(code, vlist, out_fmt, tstmp, length_hrs):
    """
    Downloads station observations for the given station and parameters.
    """
    output_map = { 'xls' : 'Excel', 'csv' : 'csv', 'xml' : 'xml' }

    params = [ ['product', ''],                 # empty in the form on the website
               ['stn', code],                   # the station code
               ['unit', '1'],                   # metric units
               ['time', 'GMT'],                 # tstamp will be in GMT
               ['day1', tstmp.day],             # the end timestamp of the measurements
               ['month1', '%02d' % tstmp.month],
               ['year1', tstmp.year],
               ['hour1', tstmp.hour],
               ['hours', length_hrs],
               ['daycalendar', 1],
               ['output', output_map[out_fmt]], # output format (excel/csv/xml)
               ['order', '0']                   # order is always ascending
               ]

    for v in vlist:
        params.append([v, v])

    # join al internal parameters
    get_rq = mesowest_dl_url + '?' + string.join(map(lambda x: x[0] + '=' + str(x[1]), params), '&')

    # download the observed variables
    content = retrieve_web_page(get_rq)
    return content


def parse_dt(dt):
    tstmp = datetime.strptime(dt, tstamp_fmt)
    return tstmp


if __name__ == '__main__':

    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print("usage: %s <station-code> <timestamp> <interval> <variables> <obs-var-table-path>" % sys.argv[0])
        print("          <timestamp> format is yyyy-mm-dd_HH:MM")
        print("          <variables> colon-separated list of variable codes (no spaces)")
        sys.exit(-1)

    code = sys.argv[1]
    ts = parse_dt(sys.argv[2])
    hours = int(sys.argv[3])
    vlist = map(lambda x: x if x not in inv_renames else inv_renames[x], sys.argv[4].split(':'))
    ovt_path = sys.argv[5]

    with open(ovt_path, "r") as f:
        obs_var_tbl = dict(map(lambda x: x.split(","), map(string.strip, f.readlines())))
        for k,v in obs_var_tbl.iteritems():
            obs_var_tbl[k] = float(v)

    # download the XLS version of the document
    doc = download_station_data(code, vlist, 'xls', ts, hours)

    # read in standard observation variances
    obs = decode_obs_xls(doc)
    write_plain_format(code,obs,obs_var_tbl)

