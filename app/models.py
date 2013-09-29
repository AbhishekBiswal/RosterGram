#from app import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
	__tablename__ = 'admin'
	uid = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(100))
	password = db.Column(db.String(100))

	def __init__(self, username, password):
		self.username = username
		self.password = password
