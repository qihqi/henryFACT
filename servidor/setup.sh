apt-get install mysql-server mysql-client
apt-get install nginx
apt-get install python-virtualenv python-pip fabric
#create virtual env
cd $DEPLOYMENT_ROOT
virtualenv env
source env/bin/activate
pip install django-1.4.0
pip install uwgsi

