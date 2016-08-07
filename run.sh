#! /usr/bin/zsh
sudo python2 tuner.py --stop-after=$1 --results-log=log.txt --parallelism=$2 --seed-configuration="$3" --no-dups
