# set the base image 
FROM python:3.9

#add project files to the usr/src/app folder
ADD ./ /usr/src/app

#set directoty where CMD will execute 
WORKDIR /usr/src/app

COPY requirements.txt ./

# Install Postgres
RUN apt update
RUN apt install -y build-essential postgresql-server-dev-all

# Get pip to download and install requirements:
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 8000

# default command to execute    
RUN python manage.py migrate
RUN python manage.py create_local_admin
CMD exec gunicorn niftybits_api.wsgi:application --bind 0.0.0.0:8000 --workers 10 --reload