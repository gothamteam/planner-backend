import urllib

import simplejson

DIRECTIONS_BASE_URL = 'https://maps.googleapis.com/maps/api/directions/json'


def get_directions(origin="New+York,+NY", dest="Chicago,IL", sensor="false", waypoints=[], **geo_args):
    geo_args.update({
        'origin': origin,
        'destination': dest,
        'waypoints': covert_way_points(waypoints),
        'sensor': sensor
    })
    url = DIRECTIONS_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = simplejson.load(urllib.urlopen(url))
    return result
    # print simplejson.dumps([s['formatted_address'] for s in result['results']], indent=2)


def covert_way_points(waypoints):
    way_point_str = ""
    if len(waypoints) > 0:
        way_point_str = "optimize:true|"
        for wayPoint in waypoints:
            way_point_str += wayPoint + "|"
    way_point_str = way_point_str[:-1]
    return way_point_str


if __name__ == '__main__':
    points = ["West Lafayette,Indiana", "Annabel,MI"]
    get_directions(origin="San+Francisco", waypoints=points, sensor="false")
