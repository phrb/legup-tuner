#! /usr/bin/zsh

name="dfadd"
duration=5400
parallel=2
workers=2
seed="seed.json"
async="map"

sudo python2 tuner.py --stop-after=$duration --results-log=log.txt --parallelism=$parallel --processes=$workers --seed-configuration="$seed" --no-dups --quiet

new_dir=$name\_$duration\_p$parallel\_w$workers\_$async

mkdir $new_dir

mv log.txt opentuner.log best_log.txt best_log.json $new_dir

sudo ./clean.sh

name="dfadd"
duration=5400
parallel=6
workers=6
seed="seed.json"
async="map"

sudo python2 tuner.py --stop-after=$duration --results-log=log.txt --parallelism=$parallel --processes=$workers --seed-configuration="$seed" --no-dups --quiet

new_dir=$name\_$duration\_p$parallel\_w$workers\_$async

mkdir $new_dir

mv log.txt opentuner.log best_log.txt best_log.json $new_dir

sudo ./clean.sh
