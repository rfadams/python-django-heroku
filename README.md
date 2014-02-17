# Steps to get started with Django on Heroku
1. Create and start a python virtualenv http://pypi.python.org/pypi/virtualenv  
    a) easy_install virtualenv #first time only  
    b) mkdir ~/Documents/PythonEnv/ && cd ~/Documents/PythonEnv/  
    c) virtualenv project-name  
    d) source ~/Documents/PythonEnv/project-name/bin/activate  
2. git clone https://rfadams@github.com/rfadams/python-django-heroku.git ~/projects/project-name
3. cd ~/projects/project-name && pip install --upgrade setuptools && pip install -r requirements.txt
4. python web/manage.py syncdb --all #Gets user account profile configured properly
5. python web/manage.py migrate --fake #Gets South migration configured properly
4. python web/manage.py runserver
5. Create an account at http://heroku.com
6. Install the heroku CLI http://devcenter.heroku.com/articles/heroku-command
7. heroku create --stack cedar project-name
8. heroku config:add DJANGO_ENV=production
9. git push heroku master
10. heroku open
11. Yay! All done.

#### Assumes you're gonna use South for database management / migrations. 

http://south.aeracode.org/docs/tutorial/part1.html  
Database should already be sync'd using steps from above  

1. python web/manage.py startapp southtut  
2. add `'southtut',` just above `'south',` in the `INSTALLED_APPS` setting in web/settings.py  
3. python web/manage.py schemamigration southtut --initial #After making a new model  
4. python web/manage.py migrate southtut  
5. python web/manage.py schemamigration southtut --auto #After you make some changes to the model  
6. python web/manage.py migrate southtut  

### Optional - Create Database
##### Mysql 
1. mysqladmin -u DBUSER -p create <project-db>
2. modify web/settings.py to reflect your database settings

##### Postgres 
1. createdb <project-db>
2. modify web/settings.py to reflect your database settings
