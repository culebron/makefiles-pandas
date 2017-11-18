
# all.sh

script1.py file1.csv file2.csv
psql mydb -f recreate-db.sql
psql mydb -c "copy 'file2.csv' to my_table csv header;"
psql mydb -f process.sql
psql mydb -c "copy my_table2 to 'file3.csv' csv header;"
script2.py file3.csv osm_downloaded.osm.bz2
osm2pgsql osm_downloaded.osm.bz2 -d mydb -c -s -S importing.style
psql mydb -f process-osm.sql
