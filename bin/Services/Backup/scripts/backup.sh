#!/bin/bash

# How to use:
# ./backup.sh <BACKUP_SOURCE_DIR> <BACKUP_DESTINATION_DIR> <PREFIX> -C optional for compression

source bin/Services/Backup/scripts/utility.sh

BACKUP_SOURCE_DIR=$1
BACKUP_DESTINATION_DIR=$2
PREFIX=$3

shift 3

DO_COMPRESS=false
DO_RENAME=false

if [ $# -ge 1 ]; then
    args="$@"
fi

for arg in $args; do
    # make arge Lowercase
    arg=$(echo "$arg" | tr '[:upper:]' '[:lower:]')

    if [ $arg = "--compress" ]; then
        DO_COMPRESS=true;
    elif [ $arg = "--rename" ]; then
        DO_RENAME=true;
    else 
        echo Invalid Arg : $arg; exit 1
    fi
done

check_path_valid    "$BACKUP_SOURCE_DIR"      "BACKUP_SOURCE_DIR";
check_path_valid    "$BACKUP_DESTINATION_DIR" "BACKUP_DESTINATION_DIR";
check_string_valid  "$PREFIX"                 "PREFIX";

if [ $DO_RENAME = true ]; then
    NAME=$PREFIX-`date +"[%d-%m-%Y.%T].%s"`
else
    NAME=${BACKUP_SOURCE_DIR##*/};
fi

if [ $DO_COMPRESS = true ]; then
    cd "$BACKUP_SOURCE_DIR" && zip -rq "$BACKUP_DESTINATION_DIR/$NAME.zip" *;
    echo -n "$BACKUP_DESTINATION_DIR/$NAME.zip";
else
    rsync --recursive "$BACKUP_SOURCE_DIR" "$BACKUP_DESTINATION_DIR/$NAME";
    echo -n "$BACKUP_DESTINATION_DIR/$NAME";
 fi

