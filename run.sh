#! /usr/bin/zsh

name="dfadd"
duration=5400
parallel=4
workers=4
seed="seed.json"
async="apply"

sudo python2 tuner.py --stop-after=$duration --results-log=log.txt --parallelism=$parallel --processes=$workers --seed-configuration="$seed" --no-dups --quiet --no-wait

new_dir=$name\_$duration\_p$parallel\_w$workers\_$async

mkdir $new_dir

mv log.txt opentuner.log best_log.txt best_log.json $new_dir

sudo ./clean.sh
