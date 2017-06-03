#! /usr/bin/zsh

names=('dfadd' 'dfdiv' 'dfmul' 'sha' 'motion' 'adpcm' 'dfsin' 'aes' 'blowfish' 'gsm' 'mips')
verilog_name="dummy.v"
duration=5400
parallel=1
workers=1
seed="seed.json"
async="seq"
iterations=10

for name in $names; do
    for i in $(seq 6 $iterations); do
        new_dir=$name\_$duration\_$i
        mkdir $new_dir
        python2 tuner.py \
            --stop-after=$duration \
            --results-log=log.txt \
            --results-log-details=log_details.txt \
            --parallelism=$parallel \
            --processes=$workers \
            --no-dups \
            --verilog-file=$verilog_name \
            --application=$name
#            --seed-configuration="$seed"

        mv config.tcl log.txt log_details.txt opentuner.log best_log.txt best_cycles_log.txt best_fmax_log.txt best_lu_log.txt best_pins_log.txt best_regs_log.txt best_block_log.txt best_ram_log.txt best_dps_log.txt best_log.json $new_dir
        ./clean.sh
    ; done
; done
