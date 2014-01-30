#! /usr/bin/env python

import xlrd
import sys
import string
import glob
import pytz
from datetime import datetime
from mwest_utils import decode_obs_xls


if __name__ == "__main__":

    gmt_tz = pytz.timezone("GMT")

    if len(sys.argv) < 3:
        print("Usage: extract_observations.py station_list obs_var_table")
        sys.exit(1)

    # read in station codes
    with open(sys.argv[1], "r") as f:
        sids = filter(lambda x: len(x) > 0 and x[0] != '#', map(string.strip, f.readlines()))

    # read in standard observation variances
    with open(sys.argv[2], "r") as f:
        obs_var_tbl = dict(map(lambda x: x.split(","), map(string.strip, f.readlines())))
        for k,v in obs_var_tbl.iteritems():
            obs_var_tbl[k] = float(v)

    # for each station find all xls files
    for sid in sids:
        print("Processing station %s" % sid)
        fnames = glob.glob("%s*.xls" % sid)

        stored_obs = {}

        # read in each file and parse the contents
        obs = {}
        for fname in fnames:
            with open(fname, 'r') as f:
                obs_i = decode_obs_xls(f.read())
                obs.update(obs_i)

        # write out the data in a neat csv file
        with open("%s.obs" % sid, "w") as f:
            f.write("# Data file generated on %s by extract_observations.py\n" % str(datetime.now()))
            f.write("# Format is time, observed_vars, observations, variances\n")
            for tm in sorted(obs.keys()):
                # sometimes stations need not supply a single measurement at a given time, then zip() fails
                if len(obs[tm]) > 0:
                    # remove unavailable measurments
                    var_list, obs_list = zip(*obs[tm])
                    obs_var = [ obs_var_tbl[x] if x in obs_var_tbl else float("nan") for x in var_list ]
                    f.write(tm.strftime('%Y-%m-%d_%H:%M %Z'))
                    f.write('\n')
                    f.write(string.join(map(str, var_list), ", "))
                    f.write('\n')
                    f.write(string.join(map(str, obs_list), ", "))
                    f.write('\n')
                    f.write(string.join(map(str, obs_var), ", "))
                    f.write('\n')


