from app import app
from flask import Flask, Response, redirect, render_template, session, request
from models import db, Admin, Team, Players
import urllib2
import json

from instagram.client import InstagramAPI
import random
accesskeyNo = random.randint(1,2)
if accesskeyNo == 1:
	access_token = '398127879.d2c650e.be22d091d3b944bcaf9e2942dd0047fc'
else:
	access_token = '398127879.d2c650e.be22d091d3b944bcaf9e2942dd0047fc'
api = InstagramAPI(client_id='d2c650e6e9ea41e4a77d3d7cf56f9919', client_secret='323783a9221f456fa454736f53a61d57', access_token='398127879.d2c650e.be22d091d3b944bcaf9e2942dd0047fc')

@app.route("/", methods=['GET'])
def home():
	#loadPlayers = Players.query.limit(10)
	# recent_media, next = api.user_recent_media(user_id=398127879, count=10)
	page = request.args.get('page')
	query = Team.query
	"""if page is None:
		page = 1
	if page == 1:
		query = Team.query.limit(12)
	elif page == 2:
		query = Team.query.slice(13,25)
	elif page == 3:
		query = Team.query.slice(26,38)
	else:
		query = Players.query.slice(39,51)"""
	return render_template("home.html", pageTitle="RosterGram Home", Players=Players, db=db, Team=Team, query=query, page=page)

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

@app.route("/dash/del-team/<tid>")
def delTeam(tid):
	if not session.get('loggedin'):
		return redirect("/")
	if tid == "":
		return redirect("/")
	team = Team.query.filter_by(tid=tid)
	for x in team:
		db.session.delete(x)
	players = Players.query.filter_by(team=tid)
	for y in players:
		db.session.delete(y)
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

@app.route("/dash/delplayer/<uid>", methods=['GET'])
def delPlayer(uid):
	player = Players.query.filter_by(pid=uid)
	for x in player:
		db.session.delete(x)
	db.session.commit()
	next = "/dash/players?team="+str(request.args.get('next'))
	return redirect(next)

@app.route("/dash/add-player", methods=['GET'])
def addPlayer():
	if not session.get('loggedin'):
		return redirect("/admin")
	if request.args.get('team') is None:
		return redirect("/dash")
	teamID = request.args.get('team')
	return render_template("add-player.html", pageTitle="Players", teamID=teamID)

@app.route("/dash/add-player/sub", methods=['POST', 'GET'])
def addPlayerSub():
	if not session.get('loggedin'):
		return redirect("/admin")
	tid = request.form['teamID']
	name = request.form['name']
	ig = request.form['ig']
	twitter = request.form['twitter']
	if (tid is None) or (ig is None) or (name is None):
		return redirect("/dash/add-player?error=1")
	url = "https://api.instagram.com/v1/users/search?q="+ig+"&access_token="+access_token
	url = "https://api.instagram.com/v1/users/search?q="+ig+"&access_token="+access_token
	response = urllib2.urlopen(url)
	html = response.read()
	nhtml = json.loads(html)
	userid = nhtml["data"][0]['id']

	recent_media, next = api.user_recent_media(user_id=userid, count=1)
	for media in recent_media:
		picture = media.images["standard_resolution"].url

	newPlayer = Players(name, ig, tid, userid, picture)
	db.session.add(newPlayer)
	db.session.commit()
	return redirect("/dash")

@app.route("/dash/edit-player", methods=['GET'])
def editPlayer():
	if not session.get('loggedin'):
		return redirect("/admin")
	if request.args.get('pid') is None:
		return redirect("/dash")
	pid = request.args.get('pid')
	# loading the variables.
	data = Players.query.filter_by(pid=pid).first()
	if data is None:
		return "Player doesn't exist"
	return render_template("edit-player.html", data=data)

@app.route("/dash/edit-player/sub", methods=['POST'])
def editPlayerSub():
	if not session.get('loggedin'):
		return redirect("/admin")
	name = request.form['name']
	ig = request.form['ig']
	twitter = request.form['twitter']
	pid = request.form['pid']
	if name is None or ig is None or twitter is None:
		return redirect("/dash/edit-player?error=1")
	player = Players.query.filter_by(pid=pid).first()
	player.name = name
	player.ig = ig
	player.twitter = twitter
	db.session.commit()
	return redirect("/admin")


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

@app.route("/p/<pid>/<mid>")
def picPage(pid, mid):
	if pid == "":
		return redirect("/")
	if mid == "":
		return redirect("/")
	pData = Players.query.filter_by(pid=pid).first()
	if pData is None:
		return "404"
	# recent_media, next = api.user_recent_media(user_id=pData.userid, count=10)
	recent_media = api.media(mid)
	return render_template("pic.html", pageTitle="Picture.", player=pData, media=recent_media)


@app.route("/test")
def testpage():
	media = api.user_recent_media(userid = 398127879, count=1)
	return str(media)

@app.route("/dash/edit-colors/<tid>")
def editTeam(tid):
	if session.get("loggedin") is not True:
		return redirect("/")
	team = Team.query.filter_by(tid=tid).first()
	if team is None:
		return "Error"
	return render_template("edit-team.html", pageTitle="Edit Team", team=team)

@app.route("/dash/edit-colors/sub", methods=['POST'])
def editColorsSub():
	if session.get("loggedin") is not True:
		return redirect("/")
	colorOne = request.form['tcolorone']
	colorTwo = request.form['tcolortwo']
	tid = request.form['tid']
	team = Team.query.filter_by(tid=tid).first()
	if team is None:
		return "Error 1"
	team.colorone = colorOne
	team.colortwo = colorTwo
	db.session.commit()
	return redirect("/dash")

@app.route("/allteams", methods=['GET'])
def allTeams():
	page = request.args.get('page')
	return render_template("allteams.html", db=db, Players=Players, Team=Team)

@app.route("/fetchPics")
def fetchPics():
	players = db.session.query(Players)
	playersCount = Players.query.count()
	j = 0
	for p in players:
		j = j + 1
		try:
			recent_media, next = api.user_recent_media(user_id=p.userid, count=3)
		except Exception:
			errorMsg = "Oops! Seems like "+p.name + " is now a private user, which is interfering with the script. Please delete the user from the admin backend and try again!"
			return errorMsg
		i = 1
		#return str(recent_media)
		for pic in recent_media:
			picture = pic.images["standard_resolution"].url
			curPlayer = Players.query.filter_by(pid=p.pid).first()
			if i == 1:
				#name = curPlayer.name
				curPlayer.picture = picture
				#curPlayer.picturetime = pic.created_time
				if pic.caption is None:
					curPlayer.picturecaption = ""
				else:	
					curPlayer.picturecaption = pic.caption.text
				curPlayer.pictureid = pic.link
			elif i == 2:
				curPlayer.picturetwo = picture
				#curPlayer.picturetwotime = pic.created_time
				if pic.caption is None:
					curPlayer.picturetwocaption = ""
				else:	
					curPlayer.picturetwocaption = pic.caption.text
				curPlayer.picturetwoid = pic.link
			else:
				curPlayer.picturethree = picture
				#curPlayer.picturethreetime = pic.created_time
				if pic.caption is None:
					curPlayer.picturethreecaption = ""
				else:	
					curPlayer.picturethreecaption = pic.caption.text
				curPlayer.picturethreeid = pic.link
			db.session.commit()
			i = i + 1
	return "done."