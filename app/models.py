#from app import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'usrs'
	uid = db.Column(db.Integer, primary_key = True)
	fullname = db.Column(db.String(100))
	provider = db.Column(db.String(100))
	fbid = db.Column(db.String(300))
	username = db.Column(db.String(100))
	gender = db.Column(db.String(20))
	email = db.Column(db.String(100))

	def __init__(self, fullname, provider, fbid, username, gender, email):
		self.fullname = fullname
		self.provider = provider
		self.fbid = fbid
		self.username = username
		self.gender = gender
		self.email = email
