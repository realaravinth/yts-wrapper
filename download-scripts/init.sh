#!/bin/bash

root="/home/aravinth/moviesBatsense/download-scripts"
mkdir -p $root
source $root/env-vars.sh

mkdir -p $log $tmp $movies $sub_bin

cd $root 

for exe in *
do 
    chmod +x $exe
done
   