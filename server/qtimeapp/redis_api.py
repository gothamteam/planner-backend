from flask import Response

from flask import json

from qtimeapp import app


@app.route("/restaurant/random")
def clouds():
    key = app.redis.randomkey()
    data = app.redis.hgetall(key)
    new_data = [json.loads(val) for key, val in data.iteritems()]
    resp = Response(json.dumps(new_data), status=200, mimetype='application/json')
    return resp
