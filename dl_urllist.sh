#!/bin/sh

while :
do
    for i in `seq 0 999`
    do
        echo $i
        python dllist.py $i
    done
done
