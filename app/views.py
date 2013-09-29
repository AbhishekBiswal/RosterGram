from app import app
from flask import Flask, Response, redirect, render_template, session, request
from models import db, Admin

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
	return "works!"