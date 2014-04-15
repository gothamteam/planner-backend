import urllib

import simplejson

DISTANCE_BASE_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json'


def get_distance(origin="New+York,+NY", dest="Chicago,IL", sensor="false",
                 mode="driving", language="en-US", **geo_args):
    geo_args.update({
        'origins': origin,
        'destinations': dest,
        'sensor': sensor,
        'mode': mode,
        'language': language
    })
    url = DISTANCE_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = simplejson.load(urllib.urlopen(url))
    return result


if __name__ == '__main__':
    get_distance(origin="San+Francisco", sensor="false", mode="driving")

'''
Sample json response

{
destination_addresses: [
"Chicago, IL, USA"
],
origin_addresses: [
"New York, NY, USA"
],
rows: [
{
elements: [
{
distance: {
text: "1,270 km",
value: 1270272
},
duration: {
text: "11 hours 57 mins",
value: 42997
},
status: "OK"
}
]
}
],
status: "OK"
}

'''
