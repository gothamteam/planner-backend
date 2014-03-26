import sys
import time
import requests
from bs4 import BeautifulSoup

BING_MAPS_KEY = 'Ahy8gRlSXY-6ByIWtjmeL6wXWYO6m8WIYazn2J-n33r8lNgaQ-kABeQisHzAyFwm'
BING_MAPS_NY_URL = 'http://dev.virtualearth.net/REST/v1/Locations/US/NY/%d//%s?o=xml&key=' + BING_MAPS_KEY

GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false'

proxies = [
    'http://94.228.205.33:8080',
    'http://194.255.66.56:8080',
    'http://109.99.168.174:8080',
    'http://195.175.200.166:8080'
]

def geo_encoding_bing(address, zipcode):
    url = BING_MAPS_NY_URL % (zipcode, address)
    r = requests.get(url)
    if r.ok:
        xml = BeautifulSoup(r.text)
        try:
            x = float(xml.latitude.text)
            y = float(xml.longitude.text)
            return x, y
        except:
            raise Exception(r.text)
    else:
        raise Exception(r.text)


def geo_encoding_google(address, zipcode, proxy):
    url = GOOGLE_MAPS_URL % ('+'.join(address.split()) + 'NY,+' + str(zipcode))
    r = requests.get(url, proxies = proxy)
    if r.ok:
        try:
            json_data = r.json()
            location = json_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        except:
            raise Exception(r.text)
    else:
        raise Exception(r.text)


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    count = 0
    fout = open(output_file, 'w')
    with open(input_file, 'r') as fin:
        for line in fin:
            count += 1
            address, zipcode = line.split(',')
            try:
                proxy = { 'https': proxies[count % len(proxies)] }
                print proxy
                x, y = geo_encoding_google(address, int(zipcode), proxy)                
                fout.write("%s: (%f, %f)\n" % (line.strip(), x, y))
                if count % 10 == 0:
                    print "%d addresses have been processed" % count
            except Exception as e:
                print proxy
                print "%s: %s" % (line, e.args[0])
    fout.close()


if __name__ == '__main__':
    main()
