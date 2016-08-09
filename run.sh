#! /usr/bin/zsh
sudo python2 tuner.py --stop-after=$1 --results-log=log.txt --parallelism=$2 --processes=$3 --seed-configuration="$4" --no-dups --quiet
