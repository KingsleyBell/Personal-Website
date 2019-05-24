FROM tiangolo/uwsgi-nginx-flask:python3.7

# copy over our required files and dirs
COPY requirements.txt /tmp/
COPY data/letsencrypt /etc/letsencrypt

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# copy over our app code
COPY ./app /app


