from flask import Flask

from flask_peewee.db import Database
from view import app

#app = Flask(__name__)
app.config.from_object('config.Configuration')

