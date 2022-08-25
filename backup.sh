#! /bin/bash

BACKUP_FILE=`date +"%Y-%m-%d-%T"`".sql"
BACKUP_PATH="mainnet_dump/$BACKUP_FILE"

echo "Snapshotting database"
echo "Backup file path: $BACKUP_PATH"

pg_dump -d postgresql://dipdup:dipdup@localhost:5432/dipdup > $BACKUP_PATH
if [ $? -eq 0 ]; then
  echo "Snapshot succesfull."
  find ./mainnet_dump -type f -not -name $BACKUP_FILE -delete
else
  echo "Snapshot failed."
fi