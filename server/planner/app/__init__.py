'''
Created on Mar 22, 2014

@author: chhe
'''
import os
import redis

from flask import Flask
app = Flask(__name__)
app.redis = redis.StrictRedis(host=os.getenv('WERCKER_REDIS_HOST', 'localhost'),
      port= 6379, db=0)

from app import views