import uuid
import math
import time
import redis


#create user 
def create_user(conn,username,password,firstName,lastName,DOB, email,age,sex,nickName):
    lower_username=username.lower()
    lock=acquire_lock_with_timeout(conn, 'lock:user:' +lower_username,10)
    if not lock:
        return False
    
    if conn.hget('user:',lower_username):
        release_lock(conn, 'lock:user:'+lower_username,lock)
        return False
    
    id=conn.incr('user:id')
    pipeline = conn.pipeline(True)
    pipeline.hset('user:',lower_username,id)
    pipeline.hmset('user:%s'%id , {
        'username':username,
        'id': id,
        'timeJoined':time.time(),
        'firstName':firstName,
        'lastName':lastName,
        'DOB':DOB,
        'email':email,
        'age':age,
        'sex':sex,
        'nickName':nickName,
    })
    pipeline.hset("user:password",lower_username,password)
    pipeline.execute()
    release_lock(conn, 'lock:user:'+lower_username,lock)
    return True

#delete a user
def delete_user(conn, username, password):
    lower_username=username.lower()
    lock=acquire_lock_with_timeout(conn, 'lock:user:' +lower_username,10)
    if not lock:
        return False
    
    if not conn.hget('user:',lower_username):
        return False
    
    id=conn.hget("user:",lower_username)
    passwordOnfile=conn.hget("user:password",lower_username)
    
    if(id!=0 and passwordOnfile==password):
        pipeline = conn.pipeline(True)
        pipeline.delete("user:"+id)
        pipeline.hdel("user:",lower_username)
        pipeline.hdel("user:password",lower_username)
        pipeline.execute()
        release_lock(conn, 'lock:user:'+lower_username,lock)
        return True
    else:
        release_lock(conn, 'lock:user:'+lower_username,lock)
        return False
    

#acquire lock
def acquire_lock_with_timeout(
    conn, lockname, acquire_timeout=10, lock_timeout=10):
    identifier=str(uuid.uuid4())
    lock_timeout = int(math.ceil(lock_timeout))
    time1=time.time()
    end=time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx(lockname, identifier):
            conn.expire(lockname,lock_timeout)
            return identifier
        elif not conn.ttl(lockname):
            conn.expire(lockname, lock_timeout)
        
        time.sleep(0.001)
    return False

#release lock
def release_lock(conn, lockname, identifier):
    pipe=conn.pipeline(True)
    
    
    while True:
        try:
            pipe.watch(lockname)
            if pipe.get(lockname) == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True
            
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            pass
        
    return False

