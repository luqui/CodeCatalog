
set -x
set -e

sudo apt-get -y install python-pip
sudo apt-get -y install postgresql

sudo apt-get -y install s3cmd
cp server-scripts/s3cfg ~/.s3cfg

rm -f *.sql.gz
s3cmd get `s3cmd ls s3://codecatalog-backup | sort -r | head -n 1 | awk '{print $4}'`

sudo -u postgres dropdb codecatalog || echo "No Database to Drop"
sudo -u postgres dropuser codecatalog || echo "No User to Drop"

sudo -u postgres createuser --no-superuser --no-createdb --no-createrole --login codecatalog
sudo -u postgres createdb -O codecatalog codecatalog
zcat *.sql.gz | sudo -u postgres psql -f - codecatalog > /dev/null

sudo pip install setuptools
sudo pip install django

sudo pip install psycopg2

cd catalogserver
cp settings/dev_settings.py.livedb dev_settings.py
./manage.py syncdb
./manage.py migrate
