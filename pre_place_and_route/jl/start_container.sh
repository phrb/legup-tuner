#! /bin/bash

IMG="legup_ubuntu"
HOST_PATH="/home/phrb/code/legup-tuner/pre_place_and_route/jl"
WORK_PATH="/root/legup_src/legup-4.0/examples/chstone/tuner"
CMD="/bin/bash"

echo "docker run --rm -w $WORK_PATH -v $HOST_PATH:$WORK_PATH -it $IMG $CMD"
docker run --rm -w $WORK_PATH -v $HOST_PATH:$WORK_PATH -it $IMG $CMD
