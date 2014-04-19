import redis
from user import *

conn = redis.StrictRedis(host='localhost', port=6379, db=0)
create=create_user(conn,"wangsuse2012","password1","chen","he","08281987", "yhfygmail.com","60","M",'cc')
print "create:"+str(create)

id=conn.hget("user:", "wangsuse2012")
print "user id is :"+id

delete=delete_user(conn,"wangsuse2012","password1")
print"delete:"+str(delete)