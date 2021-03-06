#! /bin/bash

cd $1 > /dev/null
2>/dev/null 1>/dev/null make -j4

CYCLES=$(2>/dev/null make -j4 v | grep Cycles: | awk 'BEGIN { FS = " " } ; { print $3 }')
if [[ -z $CYCLES ]]; then
    echo 'ERROR OCURRED'
    exit 0
else
    echo $CYCLES
fi
cd -> /dev/null
