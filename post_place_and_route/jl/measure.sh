#! /bin/bash

cd .. > /dev/null

#diff config.tcl tuner/config.tcl > tuner/config_diff_$1.txt
#
#2>/dev/null 1>/dev/null make -j4
#mv $2 old.v

rm config.tcl
cp tuner/config.tcl .

#2>/dev/null 1>/dev/null make -j4
#mv $2 new.v
#
#diff old.v new.v > tuner/verilog_diff_$1.txt
#
#2>/dev/null 1>/dev/null make clean
2>/dev/null 1>/dev/null make -j4

CYCLES=$(2>/dev/null make -j4 v | grep Cycles: | awk 'BEGIN { FS = " " } ; { print $3 }')
if [[ -z $CYCLES ]]; then
    echo 'ERROR OCURRED'
    exit 0
else
    echo $CYCLES
    2>/dev/null 1>/dev/null make -j4 p
    2>/dev/null 1>/dev/null make -j4 f
    grep '^; [0-9]\+.[0-9]\+ MHz' top.sta.rpt | awk 'BEGIN { FS = ";" } ; { print $2 }'
fi
