# Transfer system
###Commands for launching:

docker-compose run --rm djangoapp /bin/bash -c "cd transfer_system; python manage.py migrate"

docker-compose run --rm djangoapp /bin/bash -c "cd transfer_system; python manage.py createsuperuser"

docker-compose run --rm djangoapp /bin/bash -c "cd transfer_system; python manage.py collectstatic"

docker-compose up

docker-compose down


#For testing:

cd transfer_system

pytest -v
