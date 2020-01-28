# start from an official image
FROM python:3.6

# arbitrary Location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src


# install our dependencies
COPY requirements.txt /opt/services/djangoapp/src/
RUN pip install -r requirements.txt

# copy our project code
COPY . /opt/services/djangoapp/src

# expose the port 8000
EXPOSE 8000

RUN adduser --disabled-password --gecos '' myuser

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "transfer_system", "--bind", ":8000", "transfer_system.wsgi:application"]

#CMD ["--chdir", "crawler", "python", "manage.py", "collectstatic", "--no-input", "python", "manage.py", "migrate", "gunicorn", "--bind", ":8000", "crawler.wsgi:application"]

#CMD python manage.py collectstatic --no-input;python manage.py migrate; --chdir crawler; gunicorn crawler.wsgi -b 0.0.0.0:8000