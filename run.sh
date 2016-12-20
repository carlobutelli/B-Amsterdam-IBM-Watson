#!/bin/bash

#Change this values for django superuser
if [ -z "$VCAP_APP_PORT" ];
  then SERVER_PORT=5000;
  else SERVER_PORT="$VCAP_APP_PORT";
fi

echo [$0] Migrating
python manage.py migrate

#echo [$0] Uploading data to DB
#python manage.py shell -c "`cat data/eat_drink_import.py `"

#echo [$0] Creating superuser
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('${USER}', '${MAIL}', '${PASS}')" | python manage.py shell

echo [$0] port is------------------- $SERVER_PORT
echo [$0] Starting Django Server...
exec gunicorn discovery_backend.wsgi --workers 2