#!/bin/sh

# install nginx
# mac: brew install nginx, config file /usr/local/etc/nginx/nginx.conf
sudo apt-get install nginx
cp config/nginx.conf /etc/nginx/
sudo service nginx start
# sudo service nginx stop
# update-rc.d nginx defaults

cd server/
uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app

