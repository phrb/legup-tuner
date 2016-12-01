#! /usr/bin/zsh

names=('dfadd' 'dfdiv' 'dfmul' 'sha' 'motion' 'adpcm' 'dfsin' 'aes' 'blowfish' 'gsm' 'mips' 'jpeg')
verilog_name="dummy.v"
duration=5400
parallel=1
workers=1
seed="seed.json"
async="seq"
iterations=1

for name in $names; do
    for i in $(seq 1 $iterations); do
        new_dir=$name\_$duration\_$i
        mkdir $new_dir
        python2 tuner.py \
            --stop-after=$duration \
            --results-log=log.txt \
            --results-log-details=log_details.txt \
            --parallelism=$parallel \
            --processes=$workers \
            --seed-configuration="$seed" \
            --no-dups \
            --verilog-file=$verilog_name \
            --application=$name

        mv log.txt log_details.txt opentuner.log best_log.txt best_log.json $new_dir
        ./clean.sh
    ; done
; done
