import datetime
import os
import psycopg2
import psycopg2.extras
from lib.config import *
from lib import data_postgresql as pg
from flask import Flask, render_template, request, redirect
app = Flask(__name__)



@app.route('/')
def mainIndex():
	d = datetime.datetime.now().strftime('%A, %B %e, %Y')
	t = datetime.datetime.now().strftime('%R')
	dt = {'date': d, 'time': t}
	day = datetime.datetime.now().strftime('%A')
	return render_template('index.html', dt=dt, day=day)
	
	
@app.route('/about')
def showAbout():
	return render_template('about.html')
	
	
@app.route('/contact')
def showContact():
	return render_template('contact.html')
	
	
@app.route('/form', methods=['GET','POST'])
def showForm():
	return render_template('form.html')
	
	
@app.route('/form2', methods=['GET','POST'])
def showForm2():
	fname=request.form['fname']
	lname=request.form['lname']
	email=request.form['email']
	pw1=request.form['pw1']
	pw2=request.form['pw2']
	dob=request.form['dob']
	if request.method == 'POST':
		
		if (fname != "" and lname != "" and email != "" and pw1 == pw2):
			try:
				results = pg.newMember(fname, lname, email, dob, pw1)
				if results == None:
					return render_template('badform.html')
			except:
				print("ERROR INSERTING INTO login")
			try:
				results = pg.currentRoster()
			except:
				print("ERROR executing select")
			return render_template('form2.html', fname=fname, results=results)
		else:
			return render_template('badform.html', fname=fname, lname=lname, email=email, pw1=pw1, pw2=pw2, dob=dob)
	else:
		return render_template('form3.html', results=results)


@app.route('/form3', methods=['GET','POST'])
def showForm3():
	try:
		results = pg.currentRoster()
	except:
		print("Error executing select")
	return render_template('form3.html', results=results)


@app.route('/gallery')
def showGallery():
	p1 = '/static/faceboard/1.jpg'
	p2 = '/static/faceboard/2.jpg'
	p3 = '/static/faceboard/3.jpg'
	p4 = '/static/faceboard/4.jpg'
	p5 = '/static/faceboard/5.jpg'
	p6 = '/static/faceboard/6.jpg'
	p7 = '/static/faceboard/Thor.jpg'
	photos = {p7, p1, p2, p3, p4, p5, p6}
	return render_template('gallery.html', photos=photos)

	
# Start the server
if __name__ == '__main__':
	app.run(host=os.getenv('IP', "0.0.0.0"), port =int(os.getenv('PORT', 8080)), debug=True)