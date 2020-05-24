#!/bin/bash
#---------------------------------------------------------------
#                              USAGE
#---------------------------------------------------------------
#Downloading:
#   ./testing "magnet link or torrent link" "imdb id"



root="/home/aravinth/moviesBatsense/download-scripts"
source $root/env-vars.sh
start_time=$(date +"%F_%H-%M")
package="$tmp/$start_time/$2"
 

mkdir  -p $package/temp 

cd  $package/temp 

# downloading the torrent
transmission-cli   -w . $1 >> $movies/$2-status.txt 
$root/process.sh $package $2  $start_time
