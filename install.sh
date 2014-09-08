#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root through sudo." 1>&2
   exit 1
fi

RUNASUSER="sudo -u $SUDO_USER"
RUNASPOSTGRES="sudo -u postgres"

yum -y install python-devel python-pip python-virtualenv postgresql \
               postgresql-devel postgresql-server postgresql-plpython

virtualenv env
source ./env/bin/activate
cat dev/requirements.txt | xargs -L1 pip install
deactivate

$RUNASUSER bash <<FIN
gunzip -dc $(ls dev/bom_*.sql.gz -1 | sort | tail -1) > dump.sql
FIN

mkdir -p /usr/local/pgsql/data
touch postgres.log
chown postgres /usr/local/pgsql
chown postgres /usr/local/pgsql/data
chown postgres postgres.log

OLDDIR=$PWD

cd /usr/local/pgsql

$RUNASPOSTGRES bash <<FIN
if [ "$(ls -A /usr/local/pgsql/data)" ]; then
    echo "Database data directory already initialised."
else
    initdb -D /usr/local/pgsql/data
fi
nohup postgres -D /usr/local/pgsql/data >$PWD/postgres.log 2>&1 &

createuser -P -s -e bom
createdb --encoding=UNICODE bom -O bom
FIN

cp $OLDDIR/dump.sql /usr/local/pgsql/dump.sql
rm $OLDDIR/dump.sql
chown postgres:postgres /usr/local/pgsql/dump.sql

$RUNASPOSTGRES bash <<FIN
psql -d bom -U bom -f /usr/local/pgsql/dump.sql
FIN

cd $OLDDIR
cp dev/sample_settings.py bom/settings.py
$RUNASUSER mkdir cache
