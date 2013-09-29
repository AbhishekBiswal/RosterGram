from app import app
from flask import Flask, Response, redirect, render_template, session, request
from models import db, Admin, Team, Players

@app.route("/")
def home():
	return "Works! Yeah!"

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
	newPlayer = Players(name, ig, tid)
	db.session.add(newPlayer)
	db.session.commit()
	return "added"