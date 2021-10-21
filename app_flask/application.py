from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import datetime
from pytz import timezone
import mysql.connector
import flask
import json

mydb = mysql.connector.connect(
  host="in8.fcomet.com",
  user="dtcorpsc_user",
  password="dtcorpsc_password",
  database="dtcorpsc_mp"
)


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM customers")
customers = mycursor.fetchall()


dt = datetime.datetime.now()
format = "%Y-%m-%d %H:%M:%S %Z%z"
now_utc = datetime.datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
AM_PM = 'PM'
if now_asia.time() < datetime.time(12):
    AM_PM = 'AM'

application = Flask(__name__) 
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)

@application.route("/") 
def home():
	if not session.get("name"):
		print('Session name')
		return redirect("/login")
	return render_template('trans/line.html',err_message = '')

@application.route("/login") 
def login():
	if not session.get("name"):
		return render_template('trans/login.html',err_message = '')

@application.route("/line", methods=["POST"])
def line():
    #global distance
    username = request.form["uname"]
    password = request.form["pword"]
    #username = request.form.get("typeUserX")
    print("User & Passowrd", username)
    print("User & Passowrd", password)
    if username == 'giri' and password == 'giri@2021':
    	session["name"] = username
    	return render_template('trans/line.html',linetime=AM_PM,customers=customers)
    else:
    	return render_template('trans/login.html',err_message = 'Incorrect UserName or Password')

@application.route("/logout")
def logout():
	print('Insection logout')
	session["name"] = None
	return redirect("/")

#background process happening without any refreshing
@application.route('/background_process_test/<js_data>')
def background_process_test(js_data):
    print ("Hello")
    js_data = json.loads(js_data)
    print(js_data)
    print(js_data['cust_id'])
    sql = "INSERT INTO line (cust_id, qty, unit_price, line, user_id) VALUES (%s, %s, %s, %s, %s)"
    val = (js_data["cust_id"], js_data["qty"], js_data["price"], AM_PM, js_data["userid"])
    print(val)
    mycursor.execute(sql, val)
    mydb.commit()
    # json_data = flask.request.json
    # print(json_data)
    return ("nothing")
application.run(debug = True)