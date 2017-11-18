D=mydb
p=python3
s=psql $D -v ON_ERROR_STOP=1
z=&& touch $@

file2.csv: script1.py file1.csv
	$p $^ $@

osm_downloaded.osm.bz2: script2.py file3.csv
	$p $^ $@

recreated.touch: recreate-db.sql
	$s -f $^ $z

imported.touch: file2.csv recreated.touch
	$s -c "copy '$<' to my_table csv header;" $z

processed.touch: process.sql imported.touch
	$s -f $< $z

file3.csv: processed.touch
	$s  -c "copy my_table2 to '$@' csv header;"

osm_downloaded.osm.bz2: script2.py file3.csv
	$p $^ $@

osm-import.touch: osm_downloaded.osm.bz2 importing.style
	osm2pgsql $< -d $D -c -s -S importing.style $z

osm-processed.touch: process-osm.sql osm-import.touch
	$s $< $z
