# application/database.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine('sqlite:///yourdatabase.db', pool_size=5, max_overflow=10)

db = SQLAlchemy()
