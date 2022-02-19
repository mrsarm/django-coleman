web: ./manage.py collectstatic --no-input && uwsgi uwsgi.ini
kill: kill -9 $(cat /tmp/dcoleman-master.pid) && rm /tmp/dcoleman-master.pid
createdb: ./manage.py sqlcreate | DATABASE_URL=postgresql://postgres:$POSTGRES_PASSWORD@postgres:5432/postgres ./manage.py dbshell || true
collectstatic: ./manage.py collectstatic --no-input
compilemessages: ./manage.py compilemessages --ignore 'venv*' --ignore '.venv*'
migrate: ./manage.py showmigrations && ./manage.py migrate
makemigrations: ./manage.py makemigrations && ./manage.py makemigrations partner mtasks
createadmin: ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$ADMIN_USERNAME', password='$ADMIN_PASSWORD')" && printf "User \"$ADMIN_USERNAME\" created.\n---> DON'T forget to CHANGE the password <---\n"
provision: honcho start createdb && honcho start migrate && honcho start createadmin
test: pytest --cov --cov-report=html --cov-report=term-missing --no-cov-on-fail --color=yes
