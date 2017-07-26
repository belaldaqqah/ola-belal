from flask import Flask, render_template, request, redirect, url_for, session, escape 
import dataset
from time import localtime, strftime
app = Flask(__name__)
db =  dataset.connect('postgres://aotvgbebjecnxl:8592d2ec4231cbe4641ec6c452a51dc41e0beef794b2fa4c42515fc4b4e93f1a@ec2-184-73-199-72.compute-1.amazonaws.com:5432/d46l183jamtfom')
app.secret_key = 'A0Zr98k/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/register' , methods=["GET","POST"])
def register():
	UsersTable = db["users"]
	if request.method == "GET":
		return render_template("register.html")
	else:  
		first_name = request.form["first_name"]
		last_name = request.form["last_name"]
		email = request.form["email"]
		username = request.form["username"]
		hometown = request.form["hometown"]
		personal_website = request.form['personal_website']
		password= request.form["password"]
		entry = {"first_name":first_name ,"last_name":last_name, "email":email, "username":username, "hometown":hometown, "personal_website":personal_website, "password": password}
		nameTocheck = username
		results = list(UsersTable.find(username = nameTocheck))
		if len(results) == 0:
			session["username"]= username
			taken=0
			UsersTable.insert(entry)
			return redirect ("/list")
		else:
			taken=1
			
			return render_template('home.html', first_name=first_name , last_name=last_name , 
			email=email, username=username, hometown=hometown, personal_website=personal_website, password=password, taken=taken)

@app.route('/home')
def homepage():
	
	if "username" in session:
		username=session["username"]
		return render_template ("home.html", username=username)
	else:
		return render_template('home.html')  
	
	


@app.route('/list')
def listt():
	
	if "username" in session:
		UsersTable = db["users"]
		allUsers = list(UsersTable.all())
		print allUsers
		return render_template('list.html' , users= allUsers)
	else:
		return redirect("/error")


@app.route('/feed', methods=["GET","POST"])
def newsfeed():
	feedTable=db["feed"]
	allposts = list(feedTable.all())[::-1]
	if request.method == "GET":
		return render_template("feed.html" ,allposts=allposts)
	else:
		UsersTable = db["users"]
		username = session["username"]
		post= request.form["post"]
		time = strftime("%Y-%m-%d %H:%M:%S", localtime())
		entry = {"post":post,"username": username, "time":time}
		nameTocheck = username
		results = list(UsersTable.find(username = nameTocheck))		

	if len(results) == 1:
		taken=1
		feedTable.insert(entry)
		allposts = list(feedTable.all())[::-1]
		return render_template('feed.html',post= post, username=username , allposts=allposts)
	else: 
		taken=0
		return render_template("error.html")
@app.route("/login", methods=["GET","POST"])
def login():
	
    if request.method == "GET":
        return render_template ("login.html")
    else:

        UsersTable = db["users"]
        form = request.form
        username= form["username"]
        password= form["password"]
        nameToCheck = username
        passwordToCheck=password
        results = len(list(UsersTable.find(username = nameToCheck, password=passwordToCheck)))
        if results > 0:
        	login=1
        	session["username"]=username
        	return redirect ("/home")
        else:
            login=0
            return render_template("register.html" , login=login,username= username,password=password)

@app.route("/logout")
def logout():
	if "username" in session:
		session.pop("username", None)
		return render_template("logout.html")
	else:
		return redirect("/home")


@app.route("/error")# TODO: route to /register
def error():
	return render_template("error.html")


if __name__ == "__main__":
    app.run(port=2000)











