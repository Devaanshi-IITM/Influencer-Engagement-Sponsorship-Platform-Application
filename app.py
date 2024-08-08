from flask import Flask
from application.database import db # so app.py should be able to take db object from application database
import sqlite3
from sqlite3 import Error

app = None

def create_app():
    app = Flask(__name__) 
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///inspo.sqlite3" # insp -- > infuencer sponsor platform, its just name
    app.config['SQLALCHEMY_POOL_SIZE'] = 20
    db.init_app(app) # app shuld be configured with db object.
    app.app_context().push() # direct acessing app by other modules such as db

    return app

app = create_app()

from application.controllers import * # * --> everything. 

if __name__ == "__main__":
    app.run()
