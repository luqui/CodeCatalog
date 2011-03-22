rm database.sqlite
rm -r zoo/migrations/
./manage.py syncdb
./manage.py convert_to_south zoo
./manage.py migrate
