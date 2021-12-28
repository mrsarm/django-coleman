Run in production mode
======================

To run in production mode, you must install a WSGI compliant server
like *uWSGI* or *Gunicorn*. Also run a production-ready database like
PostgreSQL or MySQL.

To run the project with uWSGI server at port 8000, and connect
with a Postgres database named ``dcoleman_dev``
(or other specified in the environment variable ``DATABASE_URL``),
execute::

    $ ./run prod

Before run the first time, install the dependencies with::

    $ pip install -r requirements-prod.txt

The static resources must served with a HTTP server
like *Nginx* or *Apache HTTP*. To collect all static resources
in the folder ``static/``, execute once::

    $ python3 manage.py collectstatic


Nginx configuration
-------------------

This is an example of how should looks like a *Nginx* configuration
file for Django Coleman::

    server {
        listen      80;
        server_name coleman.localhost;
        access_log  /var/log/nginx/django.access.log;
        error_log   /var/log/nginx/django.error.log;

        root /path/to/project/django-coleman;

        location /static {
        }

        location / {
            proxy_pass   http://127.0.0.1:8000;
        }

        proxy_cache_valid       200  1d;
        proxy_cache_use_stale   error timeout invalid_header updating
                                http_500 http_502 http_503 http_504;

        proxy_redirect          off;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }

With the above configuration, the Admin interface should be accessible
at http://coleman.localhost/admin

If you can't see the Admin page correctly, and the browser console shows
you *403 Forbidden* errors, ensure the user that runs the Nginx server
has permissions to access to the Django Coleman resources.


PostgreSQL database
-------------------

If you want to use a PostgreSQL database (recommended), before run
the `migration scripts <https://github.com/mrsarm/django-coleman/#install-and-run>`_
be sure to create the user and the database used by Django Coleman.
In the ``run.sh`` script is used this string connection
as example: ``postgresql://dcoleman:postgres@localhost/dcoleman_dev``,
so to create a database ``dcoleman_dev`` with a user ``dcoleman`` and a
password ``postgres``, first create the user with::

    $ sudo -u postgres createuser --createdb --no-superuser --no-createrole --pwprompt dcoleman

If you are already logged-in as a superuser, you can execute instead the following, within the SQL session:
``CREATE USER dcoleman``.

Then create the database with::

    $ sudo -u postgres psql
    postgres=# CREATE DATABASE dcoleman_dev OWNER dcoleman;
