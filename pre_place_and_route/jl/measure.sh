#! /bin/bash

RES_FILE="resources.legup.rpt"

cd $1 > /dev/null
2>/dev/null 1>/dev/null make clean && 2>/dev/null 1>/dev/null make -j4

FMAX=$(grep 'Fmax: ' $RES_FILE | awk 'BEGIN { FS = " " } ; { print $2 }')
COMB_EL=$(grep 'Combinational: ' $RES_FILE | awk 'BEGIN { FS = ": " } ; { print $2 }')
REGS_EL=$(grep 'Registers: ' $RES_FILE | awk 'BEGIN { FS = ": " } ; { print $2 }')
DSP_EL=$(grep 'DSP Elements: ' $RES_FILE | awk 'BEGIN { FS = ": " } ; { print $2 }')

if [[ -z $FMAX ]] || [[ -z $COMB_EL ]] || [[ -z $REGS_EL ]] || [[ -z $DSP_EL ]]; then
    echo 'ERROR OCURRED'
    exit 0
else
    echo "$FMAX $COMB_EL $REGS_EL $DSP_EL"
fi
cd -> /dev/null
