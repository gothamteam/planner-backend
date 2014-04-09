'''
Created on Apr 8, 2014

@author: Changchen He
'''

import simplejson, urllib

DIRECTIONS_BASE_URL = 'https://maps.googleapis.com/maps/api/directions/json'

def getDirections(origin="New+York,+NY",dest="Chicago,IL",sensor="false", wayPoints=[],**geo_args):
    
    geo_args.update({
        'origin': origin,
        'destination': dest,
        'waypoints': covertWayPoints(wayPoints),
        'sensor':sensor
    })
    url = DIRECTIONS_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = simplejson.load(urllib.urlopen(url))
    return result
    #print simplejson.dumps([s['formatted_address'] for s in result['results']], indent=2)

def covertWayPoints(wayPoints):
    waypointString=""
    if len(wayPoints)>0:
        waypointString="optimize:true|"
        for wayPoint in wayPoints:
            waypointString+=wayPoint+"|"
    waypointString = waypointString[:-1] 
    return waypointString       

if __name__ == '__main__':
    waypoinst = ["West Lafayette,Indiana","Annabel,MI"]
    getDirections(origin="San+Francisco",wayPoints=waypoinst,sensor="false")