#!/bin/bash

function check_path_valid(){
    DIR_PATH=$1;
    DIR_PATH_NAME=$2

    if [ -z "$DIR_PATH" ]; then
        echo "$DIR_PATH_NAME can't be empty"; exit 1
    elif [ ! -d "$DIR_PATH" ]; then
        echo "$DIR_PATH is not a valid directory path!"; exit 1
        # echo "./backup.sh <DATABASE_NAME> <BACKUP_DESTINATION_DIR>"; exit
    fi 
}

function check_string_valid(){
    STR=$1;
    STR_VAR_NAME=$2

    if [ -z "$STR" ]; then
        echo "$STR_VAR_NAME name can't be empty"; exit 1     
    fi 
}
