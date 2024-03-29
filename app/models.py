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

class Team(db.Model):
	__tablename__ = 'teams'
	tid = db.Column(db.Integer, primary_key = True)
	teamname = db.Column(db.String(100))
	colorone = db.Column(db.String(100))
	colortwo = db.Column(db.String(100))
	cat = db.Column(db.String(300))

	def __init__(self, teamname, colorone, colortwo, cat):
		self.teamname = teamname
		self.colorone = colorone
		self.colortwo = colortwo
		self.cat = cat

	def disp(self):
		Team.query.all()

class Players(db.Model):
	__tablename__ = 'players'
	pid = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	ig = db.Column(db.String(100))
	twitter = db.Column(db.String(300))
	team = db.Column(db.Integer)
	userid = db.Column(db.Integer)
	picture = db.Column(db.String(300))
	picturetwo = db.Column(db.String(300))
	picturethree = db.Column(db.String(300))
	picturetime = db.Column(db.String(300))
	picturetwotime = db.Column(db.String(300))
	picturethreetime = db.Column(db.String(300))
	picturecaption = db.Column(db.String(300))
	picturetwocaption = db.Column(db.String(300))
	picturethreecaption = db.Column(db.String(300))
	pictureid = db.Column(db.String(300))
	picturetwoid = db.Column(db.String(300))
	picturethreeid = db.Column(db.String(300))

	def __init__(self, name, ig, team, userid, picture):
		self.name = name
		self.ig = ig
		self.team = team
		self.userid = userid
		self.picture = picture