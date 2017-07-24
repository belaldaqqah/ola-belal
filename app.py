from flask import Flask, render_template, request, redirect, url_for, session 
import dataset
from time import localtime, strftime
app = Flask(__name__)
db =  dataset.connect('postgres://aotvgbebjecnxl:8592d2ec4231cbe4641ec6c452a51dc41e0beef794b2fa4c42515fc4b4e93f1a@ec2-184-73-199-72.compute-1.amazonaws.com:5432/d46l183jamtfom')

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
		entry = {"first_name":first_name ,"last_name":last_name, "email":email, "username":username, "hometown":hometown, "personal_website":personal_website}
		nameTocheck = username
		results = list(UsersTable.find(username = nameTocheck))
		if len(results) == 0:
			taken=0
			UsersTable.insert(entry)
			return redirect ("/list")
		else:
			taken=1
			
			return render_template('home.html', first_name=first_name , last_name=last_name , 
			email=email, username=username, hometown=hometown, personal_website=personal_website, taken = taken)

@app.route('/home')
def homepage():
	return render_template('home.html')

@app.route('/list')
def listt():
	UsersTable = db["users"]
	allUsers = list(UsersTable.all())
	print allUsers
	return render_template('list.html' , users= allUsers)


@app.route('/feed', methods=["GET","POST"])
def newsfeed():
	feedTable=db["feed"]
	if request.method == "GET":
		allposts = list(feedTable.all())
		return render_template("feed.html" ,allposts=allposts)
	else:
		username = request.form["username"]
		post= request.form["post"]
		time = strftime("%Y-%m-%d %H:%M:%S", localtime())
		entry = {"post":post,"username": username, "time":time}
		feedTable.insert(entry)
		allposts = list(feedTable.all())
		return render_template('feed.html',post= post, username=username , allposts=allposts)

# TODO: route to /register

# TODO: route to /error

if __name__ == "__main__":
    app.run(port=3000)











