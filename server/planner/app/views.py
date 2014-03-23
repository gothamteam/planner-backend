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
