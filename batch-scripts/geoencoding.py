import sys
import time
import requests
import argparse
import signal

from bs4 import BeautifulSoup
from collections import Counter

EXCEPT_MAXIMUM = 20

BING_MAPS_KEY = 'Ahy8gRlSXY-6ByIWtjmeL6wXWYO6m8WIYazn2J-n33r8lNgaQ-kABeQisHzAyFwm'
BING_MAPS_NY_URL = 'http://dev.virtualearth.net/REST/v1/Locations/US/NY/%d//%s?o=xml&key=' + BING_MAPS_KEY
GOOGLE_MAPS_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false'


def handler(signum, frame):
    raise Exception("Time out")


class OverLimitException(Exception):
    pass


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
    signal.alarm(6)
    r = requests.get(url, proxies = proxy, timeout = 10)
    signal.alarm(0)
    if r.ok:
        json_data = r.json()
        if json_data['status'] == 'OK':
            json_data = r.json()
            location = json_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        elif json_data['status'] == 'OVER_QUERY_LIMIT':
            raise OverLimitException(r.text)
        else:
            raise Exception(r.text)
    else:
        raise Exception(r.text)


def run_geo_encoding_job(args):
    input_file = args.input
    output_file = args.output
    except_file = input_file + ".more"
    proxy_file = args.proxy
    start = args.start

    proxies = []
    if proxy_file is not None:
        with open(proxy_file) as fin:
            proxies = [{'https': line.strip()} for line in fin.readlines()]

    count = 0
    except_counter = [0] * len(proxies)
    fexcept = open(except_file, 'w')
    fout = open(output_file, 'a')
    with open(input_file, 'r') as fin:
        for line in fin:
            line = line.strip()
            count += 1
            if count < start:
                continue
            address, zipcode = line.split(',')
            try:
                idx = count % len(proxies)
                proxy = proxies[idx]
                print proxy
                x, y = geo_encoding_google(address, int(zipcode), proxy)                
                fout.write("%s: (%f, %f)\n" % (line.strip(), x, y))
                if count % 10 == 0:
                    print "%d addresses have been processed" % count
            except OverLimitException as e:
                print '%s over limit' % proxy
                del proxies[idx]
                del except_counter[idx]
                if len(proxies) == 0:
                    break
            except Exception as e:
                except_counter[idx] += 1
                fexcept.write(line + '\n') 
                print "%s: %s" % (line, e.args[0])
                if except_counter[idx] > EXCEPT_MAXIMUM:
                    del proxies[idx]
                    del except_counter[idx]
    print count
    fexcept.close()
    fout.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--proxy', type=str, required=False)
    parser.add_argument('--start', type=int, default=-1)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, handler)
    run_geo_encoding_job(args)

if __name__ == '__main__':
    main()

