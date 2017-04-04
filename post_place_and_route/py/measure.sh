#! /bin/bash

cd .. > /dev/null

rm config.tcl > /dev/null
cp tuner/config.tcl .

MAKEV_T=600
MAKEP_T=900
MAKEF_T=900

2>/dev/null 1>/dev/null make

CYCLES=$(timeout $MAKEV_T 2>/dev/null make -j4 v | grep Cycles: | awk 'BEGIN { FS = " " } ; { print $3 }' | tr -dc '[0-9]\+.?[0-9]\*\n')
if [[ -z $CYCLES ]]; then
    echo 'ERROR OCURRED'
    exit 0
else
    echo $CYCLES
    timeout $MAKEP_T 2>/dev/null 1>/dev/null make p
    timeout $MAKEF_T 2>/dev/null 1>/dev/null make f
    grep '^; [0-9]\+.[0-9]\+ MHz' top.sta.rpt | awk 'BEGIN { FS = ";" } ; { print $2 }'
    grep '^Logic utilization*' top.fit.summary | awk 'BEGIN { FS = "(" } ; { print $3 }' | tr -dc '[0-9]\+.?[0-9]\*\n'
    grep '^Total pins*' top.fit.summary | awk 'BEGIN { FS = "(" } ; { print $2 }' | tr -dc '[0-9]\+.?[0-9]\*\n'
    grep '^Total registers*' top.fit.summary | awk 'BEGIN { FS = ":" } ; { print $2 }' | tr -dc '[0-9]\+.?[0-9]\*\n'
    grep '^Total block memory*' top.fit.summary | awk 'BEGIN { FS = "(" } ; { print $2 }' | tr -dc '[0-9]\+.?[0-9]\*\n'
    grep '^Total RAM Blocks*' top.fit.summary | awk 'BEGIN { FS = "(" } ; { print $2 }' | tr -dc '[0-9]\+.?[0-9]\*\n'
    grep '^Total DSP Blocks*' top.fit.summary | awk 'BEGIN { FS = "(" } ; { print $2 }' | tr -dc '[0-9]\+.?[0-9]\*\n'
fi
