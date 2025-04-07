#!/bin/bash

sed -i "s/__GMAPS_API_KEY__/$GMAPS_API_KEY/g" ./src/index.html
cat ./src/index.html