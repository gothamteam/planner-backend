'''
Created on Mar 22, 2014

@author: chhe
'''
import os
import redis

from app import app
from flask import Response
from flask import json

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/json')
def readRedis():
    