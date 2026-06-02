#!/bin/bash
set -e

mkdir -p backups

docker exec cloudops-db pg_dump -U postgres cloudops > backups/cloudops_backup.sql

echo "Backup saved: backups/cloudops_backup.sql"
