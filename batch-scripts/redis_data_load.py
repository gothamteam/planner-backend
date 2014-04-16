from ast import literal_eval as make_tuple
import argparse
import geohash
import json
import redis
import math


DEFAULT_PRECISION = 6


def cleanup_str(s):
    return ' '.join(s.split())


def parse_restaurant_info(line):
    parts = [cleanup_str(p)[:-1].strip() for p in line[1:-1].strip().split(',\"')]
    entity = dict()
    entity['name'] = parts[1]
    entity['addr'] = ' '.join(parts[3:5])
    entity['strt'] = parts[4]
    entity['zipcode'] = parts[5]
    entity['phone'] = parts[6]
    try:
        entity['type'] = int(parts[7])
    except ValueError:
        entity['type'] = 0
    try:
        entity['insp_scr'] = int(parts[11])
    except ValueError:
        entity['insp_scr'] = 0
    return entity


def import_restaurant_data(args):
    datafile = args.data
    host = args.host
    port = args.port

    pipe = redis.StrictRedis(host=host, port=port).pipeline()
    uniq_set = set()
    with open(datafile, 'r') as f:
        count = 0
        for line in f:
            count += 1
            if count == 1:
                continue
            info = parse_restaurant_info(line)
            json_obj = json.dumps(info, ensure_ascii=False)
            key = 'rest:%s:%s' % (info['strt'], info['zipcode'])
            signature = '%s:%s:%s' % (info['name'], info['addr'], info['zipcode'])
            # print count
            # print json_obj
            if signature not in uniq_set:
                uniq_set.add(signature)
                pipe.hset(key, info['name'], json_obj)
            if count % 1000 == 0:
                pipe.execute()
                print '%d items has been inserted' % count


def index_restaurant_data(args):
    datafile = args.data
    host = args.host
    port = args.port

    pipe = redis.StrictRedis(host=host, port=port).pipeline()
    with open(datafile, 'r') as f:
        count = 0
        for linum, line in enumerate(f):
            try:
                count += 1
                rest = json.loads(line, 'ISO-8859-1')
                lat, lon = rest['location']
                h = hash_location(lat, lon)
                key = 'geobox:%s:restaurant' % h
                pipe.zadd(key, geohash.encode_uint64(lat, lon), line.strip())
                if count % 1000 == 0:
                    pipe.execute()
                    print '%d items has been inserted' % count
            except Exception as e:
                print str(linum) + ' ' + line
                raise e


def generate_data_set(args):
    data_file = args.data
    location_file = args.locations

    locations = dict()
    with open(location_file, 'r') as f:
        for line in f:
            addr, loc = line.strip().split(':')
            locations[addr.strip()] = make_tuple(loc.strip())

    uniq_set = set()
    with open(data_file, 'r') as f:
        lines = (line.strip() for line in f)
        count = 0
        for line in lines:
            count += 1
            if count == 1:
                continue
            info = parse_restaurant_info(line)
            key = '%s, %s' % (info['addr'], info['zipcode'])
            signature = '%s:%s:%s' % (info['name'], info['addr'], info['zipcode'])
            if key in locations and signature not in uniq_set:
                info['location'] = locations[key]
                json_obj = json.dumps(info, ensure_ascii=False)
                uniq_set.add(signature)
                print json_obj


def print_unique_addresses(args):
    data_file = args.data
    uniq_set = set()
    with open(data_file, 'r') as f:
        lines = (line.strip() for line in f)
        count = 0
        for line in lines:
            count += 1
            if count == 1:
                continue
            info = parse_restaurant_info(line)
            signature = '%s:%s:%s' % (info['name'], info['addr'], info['zipcode'])
            if signature not in uniq_set:
                uniq_set.add(signature)
                print info['addr'] + ', ' + info['zipcode']


def hash_location(lat, lon, precision=DEFAULT_PRECISION):
    return geohash.encode(lat, lon, precision)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', type=str, choices=['import', 'print', 'generate', 'index'], required=True)
    parser.add_argument('--data', type=str, required=True)
    parser.add_argument('--locations', type=str, default='locations')
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=6379)

    args = parser.parse_args()
    if args.run == 'import':
        import_restaurant_data(args)
    elif args.run == 'print':
        print_unique_addresses(args)
    elif args.run == 'generate':
        generate_data_set(args)
    elif args.run == 'index':
        index_restaurant_data(args)


if __name__ == '__main__':
    main()
