import xlrd
import sys
import string
import glob
import pytz
from datetime import datetime
import urllib

# skip and conversion tables
skip_vars = [ 'QFLG' ]
process_vars = { 'FM' : lambda x: 0.01 * x,  # fuel moisture comes in gm water /100 gm pine wood
                 'TMPF' : lambda x: 273.15 + x,  # we actually download TMPF in degrees C in the scraper
                 'RELH' : lambda x : 0.01 * x,  # relative humidity comes in percent
                 'SKNT' : lambda x : 273.15 + x # skin temperature is also in deg C
               }


def retrieve_web_page(addr):
    """
    Retrieve the web page and return it as a string.
    """
    f = urllib.urlopen(addr)
    content = f.read()
    f.close()
    return content


def decode_obs_xls(file_contents):
    """
    Load all available fuel moisture data from the station measurement file data.
    The data must be in xls format.
    """
    # open worksheet and retrieve first sheet
    x = xlrd.open_workbook(file_contents=file_contents)
    s = x.sheet_by_index(0)

    # find the order of the variables
    var_ord = []
    cell_ord = []
    obs = {}
    for i in range(1,s.ncols):
        cv = s.cell_value(0,i).strip().split(" ")[0]
        if len(cv) > 0 and cv not in skip_vars:
            var_ord.append(cv)
            cell_ord.append(i)
            if cv not in process_vars:
                process_vars[cv] = lambda x: x

    # now read 24 entries starting at 
    i = 1
    gmt_tz = pytz.timezone('GMT')
    while i < s.nrows:
        # parse the time stamp string
        try:
            tstamp = gmt_tz.localize(datetime.strptime(s.cell_value(i,0), '%m-%d-%Y %H:%M %Z'))
        except ValueError:
            break

        # parse the variables in order
        obs_i = []
        for j in range(len(cell_ord)):
            try:
                val = process_vars[var_ord[j]](float(s.cell_value(i,cell_ord[j])))
                obs_i.append((var_ord[j], val))
            except ValueError:
                pass

        obs[tstamp] = obs_i

        i += 1

    return obs



def write_plain_format(sid, obs, obs_var_tbl):
    for tm in sorted(obs.keys()):
        # sometimes stations need not supply a single measurement at a given time, then zip() fails
        if len(obs[tm]) > 0:
            # remove unavailable measurments
            var_list, obs_list = zip(*obs[tm])
            obs_var = [ obs_var_tbl[x] if x in obs_var_tbl else float("nan") for x in var_list ]
            print(tm.strftime('%Y-%m-%d_%H:%M:00 %Z'))
            for v,o,var in zip(var_list, obs_list, obs_var):
                print('%s,%g,%g' % (v,o,var))



