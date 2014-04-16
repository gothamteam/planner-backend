from flask import Response
from flask import json

from qtimeapp import app
from qtimeapp import geohash, utils


DEFAULT_PRECISION = 6


@app.route("/restaurant/random")
def restaurants_from_random_block():
    key = app.redis.randomkey()
    data = app.redis.zrange(key, 0, -1)
    restaurants = [json.loads(item) for item in data]
    resp = Response(json.dumps(restaurants), status=200, mimetype='application/json')
    return resp


@app.route("/restaurant/<lat>/<lon>")
def restaurants_by_location(lat, lon):
    lat = float(lat)
    lon = float(lon)
    h = geohash.encode(lat, lon, DEFAULT_PRECISION)
    blocks = geohash.expand(h)
    candidates = reduce(lambda a, b: a+b,
                        [[json.loads(item) for item in app.redis.zrange('geobox:%s:restaurant' % block, 0, -1)] for block in blocks],
                        [])
    sorted_candidates = sorted(candidates,
                               key=lambda candidate: abs(utils.compute_geo_distance((lat, lon), candidate['location'])))


    resp = Response(json.dumps(sorted_candidates), status=200, mimetype='application/json')
    return resp
