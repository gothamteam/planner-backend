# wget http://download.redis.io/redis-stable.tar.gz
# tar xvzf redis-stable.tar.gz
# cd redis-stable
# make

# sudo cp redis-server /usr/local/bin/
# sudo cp redis-cli /usr/local/bin/

# sudo mkdir /etc/redis
# sudo mkdir /var/redis

# sudo cp utils/redis_init_script /etc/init.d/redis_6379

# sudo cp redis.conf /etc/redis/6379.conf

# sudo mkdir /var/redis/6379

# Set daemonize to yes (by default it is set to no).
# Set the pidfile to /var/run/redis_6379.pid (modify the port if needed).
# Change the port accordingly. In our example it is not needed as the default port is already 6379.
# Set your preferred loglevel.
# Set the logfile to /var/log/redis_6379.log
# Set the dir to /var/redis/6379 (very important step!)

# sudo update-rc.d redis_6379 defaults

# /etc/init.d/redis_6379 start


# on ubuntu
sudo apt-get update
sudo apt-get install redis-server
/etc/init.d/redis-server start
