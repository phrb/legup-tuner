#! /usr/bin/zsh
sudo python2 tuner.py --stop-after=$1 --results-log=log.txt --parallelism=1 --seed-configuration="seed.json"
