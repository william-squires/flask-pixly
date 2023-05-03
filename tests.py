import os

os.environ["DATABASE_URL"] = 'postgresql:///pixly_test'

from unittest import TestCase

from app import app
from models import db, Image, connect_db

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# connect_db(app)

db.drop_all()
db.create_all()