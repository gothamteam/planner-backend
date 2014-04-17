from flask import Response
from flask import json
from flask import render_template

from qtimeapp import app
from qtimeapp import geohash, utils

DEFAULT_PRECISION = 6

@app.route("/diag/map/restaurant/<lat>/<lon>")
def restaurants_diag_by_location(lat, lon):
    lat = float(lat)
    lon = float(lon)
    h = geohash.encode(lat, lon, DEFAULT_PRECISION)
    blocks = geohash.expand(h)
    candidates = reduce(lambda a, b: a+b,
                        [[json.loads(item) for item in app.redis.zrange('geobox:%s:restaurant' % block, 0, -1)] for block in blocks],
                        [])
    sorted_candidates = sorted(candidates,
                               key=lambda candidate: abs(utils.compute_geo_distance((lat, lon), candidate['location'])))
    
    #restaurant = {'addr':sorted_candidates[0]['addr'],'location':sorted_candidates[0]['location']};
    restaurant = {'addr':"lalaldfjshialdf fjosl",'location':'abcde'};
    restaurantJson = json.dumps(restaurant);
    
    return render_template("map_diag.html",title="map_diag_restaurant",restaurant=restaurantJson,Lat=lat,Lng=lon);
