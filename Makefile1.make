file2.csv: script1.py file1.csv
	python3 $^ $@

osm_downloaded.osm.bz2: script2.py file3.csv
	python3 $^ $@

recreated.touch: recreate-db.sql
	psql mydb -v ON_ERROR_STOP -f $^ && touch $@

imported.touch: file2.csv recreated.touch
	psql mydb -v ON_ERROR_STOP -c "copy '$<' to my_table csv header;" && touch $@

processed.touch: process.sql imported.touch
	psql mydb -v ON_ERROR_STOP -f $< && touch $@

file3.csv: processed.touch
	psql mydb -v ON_ERROR_STOP  -c "copy my_table2 to '$@' csv header;"

osm_downloaded.osm.bz2: script2.py file3.csv
	python3 $^ $@

osm-import.touch: osm_downloaded.osm.bz2 importing.style
	osm2pgsql $< -d mydb -c -s -S importing.style && touch $@

osm-processed.touch: process-osm.sql osm-import.touch
	psql mydb -v ON_ERROR_STOP $< && touch $@

diagram.png: Makefile
	python makefile2dot.py < Makefile | dot -Tpng > diagram.png
