import redis
from flask import Flask


app = Flask(__name__)
app.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

from qtimeapp import views
from qtimeapp import redis_api
from qtimeapp import diag_utils

if __name__ == "__main__":
    app.run()
