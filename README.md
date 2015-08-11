[![Build Status](https://travis-ci.org/dandb/salinity.svg?branch=master)](https://travis-ci.org/dandb/salinity)
__Description__
----------------
This project is designed a django backed frontend which will parse redis information
returned from Salt-Stack config mangement highstated (Configuration applications). 

It will look at the last returns from each type of server in each environment and 
will display if they contain any failed states. Planned feature is also a Jenkins
like build health which would look at the past x state applications and determain
health based on how many failured states in the last y configuration applications.

Will display overall "salinity" percentage at the top of the page. Goal being 100%

__Install__
------------
I recommend creating a virtualenv envrionment, then simply run:
```
pip install -r requirements.txt
```

To setup django's database (sqlite for now):
```
salinity/manage.py syncdb
```
