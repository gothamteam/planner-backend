import redis
from qtimeuser.utils.user import *

conn = redis.StrictRedis(host='localhost', port=6379, db=0)
create=create_user(conn,"yhfy85","password1","chen","he","08281987", "yhfygmail.com","60","M",'cccc')
print "create:"+str(create)

qid=conn.hget("user:", "yhfy85")
print "user id is :"+qid

print "user details: "+ str(get_user_infor(conn,"yhfy85"))
update_user(conn,"yhfy85","password1","chen2","he2","082819872", "yhfygmail2.com","602","M2",'cc2')
print "user details: "+ str(get_user_infor(conn,"yhfy85"))

print "next line should have access"
print has_access(conn, "yhfy85","password1")
print "next should not have access"
print has_access(conn, "yhfy85","ajisdfnej")
print has_access(conn, "yhfy84","password1")

add_friend(conn,"yhfy85","password","14")
add_friend(conn,"yhfy85","password1","2")
add_friend(conn,"yhfy85","password1","10")
add_friend(conn,"yhfy85","password1", "15")
add_friend(conn,"yhfy85","password1","3")
add_friend(conn,"yhfy85","password1","4")
add_friend(conn,"yhfy85","password1", "5")
remove_friend(conn,"yhfy85","password1", "5")


print  get_friends(conn, "yhfy85")
print  get_friends(conn, "yhfy86")

delete=delete_user(conn,"yhfy85","password1")
print"delete:"+str(delete)
