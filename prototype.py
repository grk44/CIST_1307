from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask_bootstrap import Bootstrap
import sqlite3 as sql

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home_page():
	return render_template('home.html')

@app.route('/customer/')
def customer():
	return render_template('customer.html')


@app.route('/removeuser', methods=['POST'])
def removeuser():
	if request.method == "POST":
		userID=request.form["uID"]		

	with sql.connect("videodb.db") as con:
		try:
			cur=con.cursor()
			cur.execute("DELETE FROM customer WHERE custID=?",(userID))
		except:
			return "An Error has Occured"
	return render_template('admin.html')

@app.route('/setpass/', methods=['POST'])
def setpass():
	if request.method == "POST":
		userID=request.form["uID"]
		npw=request.form["npass"]

	with sql.connect("videodb.db") as con:
		try:
			cur=con.cursor()
			cur.execute("UPDATE customer SET password=? WHERE custID=?",(npw,userID))
		except:
			return "An Error has Occured"
	return "Change Successful"

@app.route('/removemovie', methods=['POST'])
def removemovie():
	if request.method == "POST":
		movieID=request.form["mID"]
		
	with sql.connect("videodb.db") as con:
		try:
			cur=con.cursor()
			cur.execute("DELETE FROM movies WHERE movieID=?",(movieID))
		except:
			return "An Error has Occured"
	return "Change Successful"
	

@app.route('/staff/')
def staffpage():
	con=sql.connect('videodb.db')
	con.row_factory=sql.Row
	cur=con.cursor()
	cur.execute("SELECT * FROM movies ORDER BY title ASC")
	_rows=cur.fetchall()
	return render_template('staff_portal.html', rows=_rows)

@app.route('/admin/')
def adminpage():
	
	con=sql.connect("videodb.db")
	con.row_factory = sql.Row
	cur=con.cursor()

	cur.execute("SELECT * FROM customer")
	_rows=cur.fetchall()
	return render_template('admin.html',rows=_rows)

@app.route('/rentmovie/', methods=['POST']) 
def rentmovie(): #THIS NEEDS WORK!!!!
	if request.method == "POST":
		movID=request.form["mID"]
		username=request.form["uname"]

	with sql.connect("videodb.db") as con:
		try:
			cur=con.cursor()
			cur.execute("UPDATE movies SET rentedby=? WHERE movieID=?",(username,movID))
		except:
			pass
	return render_template('home.html')

@app.route('/returnmovie/', methods=['POST'])
def returnmovie():
	if request.method == "POST":
		movID=request.form["mID"]

		with sql.connect("videodb.db") as con:
			try:
				cur=con.cursor()
				cur.execute("UPDATE movies SET rentedby= NULL WHERE movieID=?",(movID))
			except:
				pass
	return render_template('home.html')


@app.route('/addmovie/', methods=['POST'])
def addmovie():
	if request.method == "POST":
		mname = request.form["mtitle"]
		myear = request.form["myear"]
		mprice = request.form["mprice"]
		mstock = request.form["mstock"]

		with sql.connect("videodb.db") as con:
			try:
				cur = con.cursor()				
				cur.execute("INSERT INTO movies (title, year, price, stock) VALUES (?,?,?,?)",[mname,myear,mprice,mstock])
			except:
				
				return "An Error Has Occured:"
		con.commit()
		return "Movie Added:{0} year:{1} price:{2} stock:{3}".format(mname,myear,mprice,mstock)
	return 


@app.route('/customer_home/', methods=['GET','POST'])
def custhome():   # Pass Username in url with /<username> ???
	if request.method == "POST":
		uname=request.form["userl"]
		pword=request.form["passl"]

	con=sql.connect("videodb.db")
	con.row_factory = sql.Row
	cur=con.cursor()
	
	
	cur.execute("SELECT * FROM movies WHERE rentedby='%s'" % uname)
	rows=cur.fetchall()
	return render_template('customer_home.html',rows=rows)



@app.route('/customer_reg/', methods=['POST'])
def custreg():
	if request.method == "POST":
		username = request.form["usera"]
		password = request.form["passa"]

		with sql.connect("videodb.db") as con:
			try:
				cur = con.cursor()
				cur.execute("INSERT INTO customer (username, password) VALUES (?,?)",[username,password])
			except:
				#The most likely error is existing user name
				return "An Error Has Occured: Username already Exists"
		con.commit()
		return "User Added: {0}".format(username)
	return 


# def create_db():
# 	conn=sql.connect('videodb.db')
# 	conn.execute("CREATE TABLE staff (staffID INTEGER PRIMARY KEY ASC, username TEXT UNIQUE, password TEXT)")
# 	conn.execute("CREATE TABLE customer (custID INTEGER PRIMARY KEY ASC, username TEXT UNIQUE, password TEXT)")
# 	conn.execute("CREATE TABLE movies (movieID INTEGER PRIMARY KEY ASC, title TEXT, year INT, price INT, stock INT, rentedby TEXT)")
# 	conn.execute("CREATE TABLE rents (bill INT, custID INTEGER, movieID INTEGER, FOREIGN KEY(custID) REFERENCES customer(custID), FOREIGN KEY(movieID) REFERENCES movies(movieID))")
# 	conn.close()
# create_db()

if __name__ == '__main__':
	app.run(debug=True)