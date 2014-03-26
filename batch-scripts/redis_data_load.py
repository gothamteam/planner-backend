import redis
import re
import json
import uuid
import argparse


def cleanup_str(s):
     return " ".join(s.split())


def parse_restaurant_info(line):
     parts = [cleanup_str(p)[:-1].strip() for p in line[1:-1].strip().split(',\"')]
     entity = {}
     entity['name'] = parts[1]
     entity['addr'] = ' '.join(parts[3:5])
     entity['strt'] = parts[4]
     entity['zipcode'] = parts[5]
     entity['phone'] = parts[6]
     try:
          entity['type'] = int(parts[7])
     except:
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

     pipe = redis.StrictRedis().pipeline()
     uniq_set = set()
     with open(datafile, 'r') as f:
         count = 0
         for line in f:
             count += 1
             if count == 1:
                 continue
             info =  parse_restaurant_info(line)
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


def print_unique_addresses(args):
     datafile = args.data
     uniq_set = set()
     with open(datafile, 'r') as f:
         count = 0
         for line in f:
             count += 1
             if count == 1:
                 continue
             info =  parse_restaurant_info(line)
             json_obj = json.dumps(info, ensure_ascii=False)
             key = 'rest:%s:%s' % (info['strt'], info['zipcode'])
             signature = '%s:%s:%s' % (info['name'], info['addr'], info['zipcode'])
             # print count
             # print json_obj
             if signature not in uniq_set:
                  uniq_set.add(signature)
                  print info['addr'] + ', ' + info['zipcode']
             

def main():
     parser = argparse.ArgumentParser()
     parser.add_argument('--data', type=str, required=True)
     parser.add_argument('--host', type=str, required=True)
     parser.add_argument('--port', type=int, default=6379)
     parser.add_argument('--run', type=str, choices=['import', 'print'], required=True)

     args = parser.parse_args()
     if args.run == 'import':
          import_restaurant_data(args)
     elif args.run == 'print':
          print_unique_addresses(args)

if __name__ == '__main__':
     main()

    
