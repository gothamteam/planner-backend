#!/bin/sh

# install nginx
# mac: brew install nginx, config file /usr/local/etc/nginx/nginx.conf
sudo apt-get install nginx
sudo service nginx start
# sudo service nginx stop
# update-rc.d nginx defaults

cp config/nginx.conf /etc/nginx/
uwsgi --socket 127.0.0.1:8080 --protocol=http -w wsgi:app

