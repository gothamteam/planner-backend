'''
Created on Mar 22, 2014

@author: chhe
'''
import os
import redis

from flask import Flask
from flask import Response
from flask import json
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("resturants/random.json")
def clouds():
    aKey = app.redis.randomkey();
    data = app.redis.hgetall(aKey);
    newdata = [json.loads(val) for key,val in data.iteritems()];    
    resp = Response(json.dumps(newdata) , status=200, mimetype='application/json')
    return resp;