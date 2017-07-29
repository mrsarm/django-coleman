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

    $ python3 manage.py makemigrations
    $ python3 manage.py makemigrations mtasks
    $ python3 manage.py migrate

To create an admin user::

    $ python3 manage.py createsuperuser

Then run with::

    $ python3 manage.py runserver

Or use the script to startup::

    $ ./run.sh dev

To run for production environment::

    $ ./run.sh prod

Some settings can be overwritten with enviroment variables with the same name.
For example to overwrite the language of the application::

    $ LANGUAGE_CODE=es-ar ./run.sh prod

Available settings to override are:

* ``TIME_ZONE``: default ``UTC``. Other example: ``America/Buenos_Aires``
* ``LANGUAGE_CODE``: default ``en-us``. Other example: ``es-ar``.


Access the application
----------------------

Like any Django app developed with Django Admin, enter with: http://localhost:8000/admin


Development
-----------

Some tips if you are improving this application.

Translations
^^^^^^^^^^^^

After add to the code new texts to be translated, execute
from the root folder::

    $ django-admin makemessages -l LANG

The go to the *.po* file and add the translation. Finally
execute to compile::

    $ django-admin compilemessages


About
-----

**Project**: https://github.com/mrsarm/django-coleman

**Authors**: (2017) Mariano Ruiz <mrsarm@gmail.com>

**License**: AGPL-v3
