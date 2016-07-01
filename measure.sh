#! /bin/bash

cd ..
rm config.tcl
cp tuner/config.tcl .
make &> /dev/null
CYCLES=$(make v | grep Cycles: | awk 'BEGIN { FS = " " } ; { print $3 }')
if [[ -z $CYCLES ]]; then
    echo 'ERROR OCURRED'
    exit 0
else
    echo $CYCLES
    make p &> /dev/null
    make f &> /dev/null
    grep '^; [0-9]\+.[0-9]\+ MHz' top.sta.rpt | awk 'BEGIN { FS = ";" } ; { print $2 }'
fi
