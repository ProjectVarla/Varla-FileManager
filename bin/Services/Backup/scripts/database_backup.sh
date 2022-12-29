#!/bin/bash

# How to use:
# ./backup.sh <DATABASE_NAME> <BACKUP_DESTINATION_DIR>

source bin/Services/Backup/scripts/utility.sh

DATABASE_NAME=$1
BACKUP_DESTINATION_DIR=$2

check_string_valid  "$DATABASE_NAME" "DATABASE_NAME"
check_path_valid    "$BACKUP_DESTINATION_DIR" "BACKUP_DESTINATION_DIR"

    {
        mysqldump "$DATABASE_NAME" > "$BACKUP_DESTINATION_DIR/$DATABASE_NAME.sql" 
    } || {
        rm "$BACKUP_DESTINATION_DIR/$DATABASE_NAME.sql" 
        echo "Failed to backup database $DATABASE_NAME"
        exit 1
    } 

exit 0