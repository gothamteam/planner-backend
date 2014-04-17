#test
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('name','shusen wang')

r.get('name')
print r.get('name')
print r.smembers('news:1000:tags')