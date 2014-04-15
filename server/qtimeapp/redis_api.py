from flask import Response

from flask import json

from qtimeapp import app


@app.route("/restaurant/random")
def random_block():
    key = app.redis.randomkey()
    data = app.redis.zrange(key, 0, -1, withscores=True)
    restaurants = [json.loads(item) for item, _ in data]
    resp = Response(json.dumps(restaurants), status=200, mimetype='application/json')
    return resp
