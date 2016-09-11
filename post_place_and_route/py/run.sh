#! /usr/bin/zsh

name="adpcm"
verilog_name="dfadd.v"
duration=7200
parallel=1
workers=1
seed="seed.json"
async="seq"
iterations=1

for i in $(seq 1 $iterations);
    do sudo python2 tuner.py \
        --stop-after=$duration \
        --results-log=log.txt \
        --results-log-details=log_details.txt \
        --parallelism=$parallel \
        --processes=$workers \
        --seed-configuration="$seed" \
        --no-dups \
        --verilog-file=$verilog_name \
        --application=$name

    new_dir=$name\_$duration\_$i
    mkdir $new_dir
    mv log.txt log_details.txt opentuner.log best_log.txt best_log.json $new_dir
    sudo ./clean.sh
; done
