
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

echo "CREATE ROLE codecatalog ENCRYPTED PASSWORD 'md57440cf204de9772bdbf067bf97f8fb63' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;" | sudo -u postgres psql
sudo -u postgres createdb -O codecatalog codecatalog
zcat *.sql.gz | sudo -u postgres psql -f - codecatalog > /dev/null


sudo pip install setuptools
sudo pip install django
sudo pip install south
sudo pip install django-haystack
sudo pip install python-openid
sudo pip install django-openid-auth
sudo pip install pysolr
sudo pip install beautifulsoup

sudo apt-get -y install libpq-dev
sudo apt-get -y install python-psycopg2

sudo apt-get -y install libapache2-mod-wsgi
sudo cp server-scripts/httpd.conf /etc/apache2/httpd.conf
sudo cp server-scripts/pg_hba.conf /etc/postgresql/*/main/

sudo /etc/init.d/postgresql* restart

sudo apt-get -y install solr-tomcat
sudo cp server-scripts/server.xml /etc/tomcat6/server.xml
sudo cp server-scripts/schema.xml /etc/solr/conf/schema.xml

cd catalogserver
cp settings/dev_settings.py.postgres dev_settings.py
./manage.py syncdb
./manage.py migrate
sudo chown :www-data .
sudo chmod g+w .
sudo /etc/init.d/tomcat6 restart
./manage.py rebuild_index --noinput

cd ..
sudo cp server-scripts/codecatalog-backup /etc/cron.daily/

sudo /etc/init.d/apache2 restart

echo "CodeCatalog Configured"
