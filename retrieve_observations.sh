#!/usr/bin/env bash

if [ $# -ne 2 ]; then
  echo "usage: retrieve_observations.sh <station-list> <timestamp>"
  echo "       <timestamp> must be formatted as YYYY-MM-DD_HH:mmm"
  exit 2
fi


STATIONS=`grep -v "^#" $1`

for S in $STATIONS ;
do
    echo "Processing $S ..."
    python scrape_station.py -c $S -i 24 -t $2 dl
done
