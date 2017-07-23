from flask import Flask, render_template, request, redirect, url_for
import dataset

app = Flask(__name__)
# TODO: connect your database here


@app.route('/')
@app.route('/home')
def homepage():
	return render_template('home.html')

# TODO: route to /list

# TODO: route to /feed

# TODO: route to /register

# TODO: route to /error

if __name__ == "__main__":
    app.run(port=3000)











