from app import app
from flask import Flask, Response, redirect, render_template, session, request
from models import db, Admin, Team, Players
import urllib2
import json

from instagram.client import InstagramAPI
access_token = '398127879.d2c650e.be22d091d3b944bcaf9e2942dd0047fc'
api = InstagramAPI(client_id='d2c650e6e9ea41e4a77d3d7cf56f9919', client_secret='323783a9221f456fa454736f53a61d57', access_token='398127879.d2c650e.be22d091d3b944bcaf9e2942dd0047fc')

@app.route("/")
def home():
	loadPlayers = Players.query.limit(10)
	recent_media, next = api.user_recent_media(user_id=398127879, count=2)
	return render_template("home.html", pageTitle="RosterGram Home", recent_media= recent_media, Players=Players, db=db, api=api)

@app.route("/admin")
def adminHome():
	if session.get('loggedin'):
		return redirect("/dash")
	return render_template("admin-home.html", pageTitle="Admin Login")

@app.route("/admin/login", methods=['GET', 'POST'])
def adminLogin():
	if session.get('loggedin'):
		return redirect("/dash")
	userName = request.form['username']
	passWord = request.form['password']
	if (userName is None) or (passWord is None):
		return redirect("/admin?error=1")
	check = Admin.query.filter_by(username=userName, password=passWord).first()
	if check is None:
		return redirect("/admin?error=1")
	else:
		session['loggedin'] = True
		session['username'] = userName
		return redirect("/dash")

@app.route("/dash")
def dash():
	if not session.get('loggedin'):
		return redirect("/admin")
	return render_template("dash.html", pageTitle="Dash", db=db, Team=Team)

@app.route("/dash/add-team")
def addTeam():
	if not session.get('loggedin'):
		return redirect("/admin")
	return render_template("add-team.html", pageTitle="Add Team")

@app.route("/dash/add-team/sub", methods=['POST'])
def addTeamSub():
	if not session.get('loggedin'):
		return redirect("/admin")
	teamName = request.form['tname']
	colorOne = request.form['tcolorone']
	colorTwo = request.form['tcolortwo']
	if (teamName is None) or (colorOne is None) or (colorTwo is None):
		return redirect("/dash/add-team?error=1")
	newTeam = Team(teamName, colorOne, colorTwo)
	db.session.add(newTeam)
	db.session.commit()
	return redirect("/dash")

@app.route("/dash/players", methods=['GET'])
def teamPlayers():
	if not session.get('loggedin'):
		return redirect("/admin")
	if request.args.get('team') is None:
		return redirect("/dash")
	teamID = request.args.get('team')
	return render_template("players.html", pageTitle="Team Members", db=db, teamID = teamID, Players=Players)

@app.route("/dash/delplayer/<uid>")
def delPlayer(uid):
	player = Players.query.filter_by(pid=uid)
	for x in player:
		db.session.delete(x)
	return redirect("/dash")

@app.route("/dash/add-player", methods=['GET'])
def addPlayer():
	if not session.get('loggedin'):
		return redirect("/admin")
	if request.args.get('team') is None:
		return redirect("/dash")
	teamID = request.args.get('team')
	return render_template("add-player.html", pageTitle="Players", teamID=teamID)

@app.route("/dash/add-player/sub", methods=['POST'])
def addPlayerSub():
	if not session.get('loggedin'):
		return redirect("/admin")
	tid = request.form['teamID']
	name = request.form['name']
	ig = request.form['ig']
	if (tid is None) or (ig is None) or (name is None):
		return redirect("/dash/add-player?error=1")

	url = "https://api.instagram.com/v1/users/search?q="+ig+"&access_token="+access_token
	url = "https://api.instagram.com/v1/users/search?q="+ig+"&access_token="+access_token
	response = urllib2.urlopen(url)
	html = response.read()
	nhtml = json.loads(html)
	userid = nhtml["data"][0]['id']

	newPlayer = Players(name, ig, tid, userid)
	db.session.add(newPlayer)
	db.session.commit()
	return "added"

@app.route("/team/<teamid>", methods=['GET'])
def teamPage(teamid):
	loadTeam = Team.query.filter_by(tid = teamid).first()
	teamName = loadTeam.teamname
	i = 0
	list = []
	for item in db.session.query(Players).filter_by(team=teamid):
		list.append([])
		list[i].append(item.name)
		list[i].append(item.ig)
		list[i].append(item.userid)
		list[i].append(item.team)
		recent_media, next = api.user_recent_media(user_id=item.userid, count=1)
		for media in recent_media:
			image = media.images['thumbnail'].url
			list[i].append(image)
		i = i + 1

	return render_template("teampage.html", pageTitle = "Team Page", Players=Players, teamid=teamid, db=db, teamName=teamName, list=list, media=media)

@app.route("/p/<pid>")
def picPage(pid):
	if pid == "":
		return redirect("/")
	pData = Players.query.filter_by(pid=pid).first()
	if pData is None:
		return "404"
	recent_media, next = api.user_recent_media(user_id=pData.userid, count=1)
	for media in recent_media:
		picture = media.images['standard_resolution'].url
		comments = media.comments
	no_of_comments = len(comments)
	return render_template("pic.html", pageTitle="Picture.", player=pData, picture=picture, comments=comments, no_of_comments=no_of_comments)


@app.route("/test")
def testpage():
	media = api.user_recent_media(userid = 398127879, count=1)
	return str(media)