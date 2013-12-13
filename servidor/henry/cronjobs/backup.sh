#!/bin/sh
mysqldump -uroot -p'no jodas'  --opt henry  > ~/backup/my_db.sql
cd ~/backup/
filename="db_weekly_"`eval date +%Y%m%d`".tgz"
tar -zcvf $filename *.sql

#run the data collector script
python /var/servidor/henry/cronjobs/jobs.py
