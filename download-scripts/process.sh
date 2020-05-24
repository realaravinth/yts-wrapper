#!/bin/bash
#---------------------------------------------------------------
#                              USAGE
#---------------------------------------------------------------
#Downloading:
#   ./process  "package-dir" "imdb-id"  "startime" 


root="/home/aravinth/moviesBatsense/download-scripts"
source $root/env-vars.sh

package=$1

convert_sub(){
    $sub_bin 
		rm *.srt
    mv *.vtt $1.vtt
		mv $1.vtt $package
}

convert_video(){
    mv $1 $2
    ffmpeg -i $2 -codec copy $2.mp4 
    mv $2.mp4 $package
}

cd $1/temp/*

# cleaning up junk
rm -r *.txt
rm -r *.jpg
rm -r *.png

# converting files 
for file in *
do
    if [ -d $file ]
    then 
        rm -rf $file
    fi
    extention="${file##*.}" 
    name="${file%.*}"
    
    if [ $extention == "srt" ]
    then
        convert_sub $2
		else
				status=$(/home/aravinth/venv/bin/python3.7 $root/download_subs.py $2)
				if [ $status -eq 1 ]
				then
						sleep 0.00000001
				else 
						curl $status --output $2.zip
						unzip $2.zip
						rm $2.zip
						convert_sub $2
				fi
    fi
    if [ $extention == "avi" ]
    then
        convert_video $file $2
    fi
    if [ $extention == "webm" ]
    then
        convert_video $file $2
    fi
    if [ $extention == "mkv" ]
    then
        convert_video $file $2
    fi
    if [ $extention == "mp4" ]
    then
        mv $file $2.mp4
        mv $2.mp4 $package
    fi

done 

# Cleaning up temp 
# cd ../$2

# mv * $1

# for file in *
# do
# mv $file $1
# done 

cd $1
rm -rf temp
cd ..

# moving files into production
mv $1 $movies 

rm -rf $tmp/$3
