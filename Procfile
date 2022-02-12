web: ./manage.py collectstatic --no-input && uwsgi uwsgi.ini
kill: kill -9 $(cat /tmp/dcoleman-master.pid) && rm /tmp/dcoleman-master.pid
createdb: ./manage.py sqlcreate | DATABASE_URL=postgresql://postgres:$PG_PASSWORD@postgres:5432/postgres ./manage.py dbshell || true
migrate: ./manage.py showmigrations && ./manage.py migrate
makemigrations: ./manage.py makemigrations && ./manage.py makemigrations partner mtasks
createadmin: ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('$ADMIN_USERNAME', password='$ADMIN_PASSWORD')" && printf "User $ADMIN_USERNAME/$ADMIN_PASSWORD created.\n---> DON'T forget to CHANGE the password <---\n"
