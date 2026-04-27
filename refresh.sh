#!/usr/bin/env bash

set -e  # exit on error

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
MYSQL_SOCKET="/tmp/mysql.sock"
MYSQL_PORT=3306

echo "==> Updating repo (hard reset)"
cd "$REPO_DIR"
git fetch origin
git reset --hard origin/main

echo "==> Checking if MySQL is running"

if ! mysqladmin --socket="$MYSQL_SOCKET" ping >/dev/null 2>&1; then
echo "MySQL not running, starting it..."

mysqld 
--basedir="$HOME/bin/mysql_install" 
--datadir="$HOME/mysql-data" 
--socket="$MYSQL_SOCKET" 
--port=$MYSQL_PORT &

echo "Waiting for MySQL to be ready..."
for i in {1..30}; do
if mysqladmin --socket="$MYSQL_SOCKET" ping >/dev/null 2>&1; then
break
fi
sleep 1
done
fi

echo "==> Resetting 'jokes' database"

mysql --socket="$MYSQL_SOCKET" 
--user=root 
--password="$MYSQLPASS" 
-e "DROP DATABASE IF EXISTS jokes; CREATE DATABASE jokes;"

echo "==> Importing jkdb.sql"

mysql --socket="$MYSQL_SOCKET" 
--user=root 
--password="$MYSQLPASS" 
jokes < "$REPO_DIR/jkdb.sql"

echo "==> Done. Database refreshed."
