#!/bin/sh

for i in `seq 0 999`
do
    echo $i
    python dl_imgs.py $i
done
