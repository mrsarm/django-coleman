.. image:: https://media.giphy.com/media/vQ2YjH4KCDRSM/giphy-downsized.gif


Django Coleman
==============

Django Coleman: A very simple Task Management web app written
with **Django Admin**.


Features
--------

* Simple task manager that allows to define a tasks with title,
  partner (customer, provider...), description, responsible of the task, priority...
* Each task may have items: sub-tasks to be done.
* The built-in Django *Authentication and Authorization* system
  to manage users and groups, login, etc.
* Module `django-adminfilters <https://github.com/mrsarm/django-adminfilters>`_
  that allows multiselection searches.
* Module `django-advanced-filters <https://github.com/modlinltd/django-advanced-filters>`_
  that allows to make more complex searches.
* Send emails when a task is created.
* Spanish translations.
* Basic Rest API configuration (disabled by default, check the
  ``INSTALLED_APPS`` setting)
* Optionally, you can use Django Coleman along with
  `Django Coleman Viewer <https://github.com/mrsarm/tornado-dcoleman-mtasks-viewer>`_
  to allows users to follow the orders

.. image:: docs/source/_static/img/django-coleman.png
   :alt: Django Coleman


Requirements
------------

* Python 3.6+ (tested with Python 3.6 and 3.10).
* Django 3.2 and other dependencies declared
  in the ``requirements.txt`` file (use virtual environments!).
* A Django compatible database like PostgreSQL (by default uses
  the Python's built-in SQLite database for development purpose).


Install and Run
---------------

*(Optional)* Create a virtual environment and activate it with::

    $ python3 -m venv .venv && source .venv/bin/activate

Install dependencies with::

    $ pip install --upgrade pip wheel
    $ pip install -r requirements.txt
    $ pip install -r requirements-dev.txt       # For DEV environments

Create the database with::

    $ python3 manage.py makemigrations
    $ python3 manage.py makemigrations mtasks
    $ python3 manage.py makemigrations partner
    $ python3 manage.py migrate

To create an admin user::

    $ python3 manage.py createsuperuser

Then run in development mode with::

    $ python3 manage.py runserver

Or use the script to startup in the same mode::

    $ ./run.sh dev

Some settings can be overwritten with environment variables.
For example to overwrite the language translations of the application and
set *debug* options to false::

    $ DEBUG=False LANGUAGE_CODE=es-ar python3 manage.py runserver

Also in development environments an `.env` file can be used to setup
the environment variables easily, checkout the `<.env.example>`_ as example.
You can copy the example file and edit the variables you want to change::

   $ cp .env.example .env
   $ vi .env

Available settings to override are:

* ``DEBUG``: set the Django ``DEBUG`` option. Default ``True``.
* ``TIME_ZONE``: default ``UTC``. Other example: ``America/Buenos_Aires``.
* ``LANGUAGE_CODE``: default ``en-us``. Other example: ``es-ar``.
* ``SITE_HEADER``: Header title of the app. Default to *"Django Coleman - A Simple Task Manager"*.
* ``DATABASE_URL``: Database string connection. Default uses SQLite database. Other
  example: ``postgresql://dcoleman:postgres@localhost/dcoleman_dev``.
* More settings like email notifications, check the ``settings.py`` file
  for more details, any variable that is set with ``env('...`` is able
  to be configured using environment variables.

To run in a production environment, check the `<README-production.rst>`_ notes, or
see the official Django documentation.


Access the application
----------------------

Like any Django app developed with Django Admin, enter with: http://localhost:8000/admin


Django Coleman Viewer
---------------------

`Django Coleman Viewer <https://github.com/mrsarm/tornado-dcoleman-mtasks-viewer>`_ is a
small webapp that can be used along with Django Coleman to allow "partners" (customers, employees,
providers...) to see their orders anonymously, without access to the Django Admin.

You need to enable the email notifications and set ``TASKS_VIEWER_ENABLED`` and ``REST_ENABLED``
settings to ``True`` to send the emails with the viewer order URL. See more configurations in the
``coleman/settings_emails.py`` file, and checkout the viewer project.

.. image:: https://raw.githubusercontent.com/mrsarm/tornado-dcoleman-mtasks-viewer/master/docs/source/_static/img/dcoleman-viewer.png


Development
-----------

Some tips if you are improving this application.

Translations
^^^^^^^^^^^^

After add to the source code new texts to be translated, execute
from the root folder (replace ``LANG`` by a valid language
code like ``es``)::

    $ django-admin makemessages -l LANG

Then go to the *.po* file and add the translations. Finally
execute to compile the locales::

    $ django-admin compilemessages


Oldest Django versions
^^^^^^^^^^^^^^^^^^^^^^

The ``master`` branch works with Django 3.2. The are a few more branches (though unmaintained):

* ``django/2.2``
* ``django/2.0``
* ``django/1.11``

With the source code that works for each version of Django,
and maybe tweaking some configurations can works with oldest versions too.


Some screenshots
----------------

.. image:: docs/source/_static/img/django-coleman-task-change.png
   :alt: Django Coleman - Task Chance View


.. image:: docs/source/_static/img/django-coleman-task-change-mobile.png
   :alt: Django Coleman - Task Chance View, mobile version


About
-----

**Project**: https://github.com/mrsarm/django-coleman

**Authors**: (2017-2022) Mariano Ruiz <mrsarm@gmail.com>

**License**: AGPL-v3
