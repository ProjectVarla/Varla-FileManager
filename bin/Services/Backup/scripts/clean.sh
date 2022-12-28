#!/bin/bash

# How to use:
# ./clean.sh <DIR_PATH> <SIZE_WINDOW Optional Default 5 days>

source bin/services/backup/scripts/utility.sh

DIR_PATH=$1
SIZE_WINDOW=$2 # Default 5 Days

if [ -z $SIZE_WINDOW ] & ! [[ "$SIZE_WINDOW" =~ ^[0-9]+$ ]]; then
    SIZE_WINDOW=5 
fi

if [ -z "$DIR_PATH" ]; then
    echo "DIR_PATH can't be empty"; exit;
elif [ ! -d "$DIR_PATH" ]; then
    echo "$DIR_PATH is not a valid directory path!"; exit;
fi 

for i in "$DIR_PATH/*"; do 
    if [ -f $i ]; then
                
        # Get timestamp directories in DIR_PATH 
        FILE_NAME=${i%.*};
        FILE_TIMESTAMP=${FILE_NAME##*.};

        # Get timestamp of allowed period 
        WINDOW_TIMESTAMP=`date +"%s " -d -"$SIZE_WINDOW day"`;

        # Remove all Dirctories not in allowed window.
        if [ $FILE_TIMESTAMP -le $WINDOW_TIMESTAMP ]; then
            rm $i;
        fi
        
    elif [ -d $i ]; then

        # Get timestamp directories in DIR_PATH 
        DIR_TIMESTAMP=${i##*.}

        # Get timestamp of allowed period 
        WINDOW_TIMESTAMP=`date +"%s " -d -"$SIZE_WINDOW day"`

        # Remove all Dirctories not in allowed window.
        if [ $DIR_TIMESTAMP -le $WINDOW_TIMESTAMP ]; then
            rm -r $i
        fi
    fi
done

