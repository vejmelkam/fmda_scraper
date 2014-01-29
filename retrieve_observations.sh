#!/usr/bin/env bash

STATIONS=`grep -v "^#" $1`

for S in $STATIONS ;
do
    echo "Processing $S ..."
    python scrape_station.py -c $S -i 24 -t $2 dl
done
