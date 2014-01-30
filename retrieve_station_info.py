#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys
import time
import argparse
from datetime import datetime
import string
import os
from mwest_utils import retrieve_web_page


# mesowest list of stations
mesowest_station_url = 'http://mesowest.utah.edu/cgi-bin/droman/download_ndb.cgi?stn=%s'
mesowest_station_pos = 'http://mesowest.utah.edu/cgi-bin/droman/side_mesowest.cgi?stn=%s'

# format of timestamp
tstamp_fmt = '%Y-%m-%d_%H:%M'

# renaming dictionary handling differences between variable names in xls files from Mesowest
# and in the variable listing
renames = { 'TMPF' : 'TMP', 'DWPF' : 'DWP' }


def get_station_info(station_info):
    """
    Return a list all the variables that are measured by a station with the station
    code given, store it in the station_info dictionary and also return it.
    """
    # retrieve web page, parse it and pause slightly
    p = retrieve_web_page(mesowest_station_url % station_info['code'])
    soup = BeautifulSoup(p)
    table = soup.find_all('table')[-2]
    varc = table.find_all('td')[2]
    vlist = [ inp.get('value') for inp in varc.find_all('input') ]
    station_info['vlist'] = vlist

    # retrieve web page with position info for station
    p = retrieve_web_page(mesowest_station_pos % station_info['code'])
    soup = BeautifulSoup(p)
    data = filter(lambda x: x.find(':') > 0, map(string.strip, soup.div.getText().split('\n')))
    d = dict([ s.split(':') for s in data ])
    station_info['elevation'] = int(d['ELEVATION'][:-3]) * 0.3048
    station_info['lat'] = float(d['LATITUDE'])
    station_info['lon'] = float(d['LONGITUDE'])
    station_info['wims'] = d['WIMS ID']
    station_info['mnet'] = d['MNET']
    station_info['name'] = d['NAME']


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: %s <station-code>" % sys.argv[0])
        sys.exit(-1)

    si = { 'code' : sys.argv[1] }
    get_station_info(si)
    nnv = [ renames[x] if x in renames else x for x in si['vlist'] ]
    print(",".join([si['code'], string.strip(si['name'].replace(',', ' ')), str(si['lat']), str(si['lon']), str(si['elevation']), ":".join(nnv)]))

