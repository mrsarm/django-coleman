Django Coleman
==============

Django Coleman: A very simple Task Management web app written
with **Django Admin**.


Requirements
------------

* Python 3.x (tested with Python 3.6)
* Django 1.11


Install and Run
---------------

Install dependencies with::

    $ pip install -r requirements.txt
    $ pip install -r requirements-dev.txt       # For DEV environments

Create the database with::

    $ ./manage.py makemigrations
    $ ./manage.py makemigrations mtasks
    $ ./manage.py migrate

To create an admin user::

    $ ./manage.py createsuperuser

Then run with::

    $ ./manage.py runserver


About
-----

**Project**: https://github.com/mrsarm/django-coleman

**Authors**: (2017) Mariano Ruiz <mrsarm@gmail.com>

**License**: AGPL-v3
