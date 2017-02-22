import datetime
import os
import psycopg2
import psycopg2.extras
from lib.config import *
from lib import data_postgresql as pg
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')


username = ''
password = ''
firstname = ''
zipcode = ''

@app.route('/', methods=['GET','POST'])
def mainIndex():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['password'] = request.form['password']
		session['firstname'] = pg.getFirstName(session['username'],session['password'])
		session['zipcode'] = pg.getZip(session['username'],session['password'])
		
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	return render_template('index.html', user=user)
	
	
@app.route('/about')
def showAbout():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	return render_template('about.html', user=user)
	
	
@app.route('/contact')
def showContact():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	return render_template('contact.html', user=user)
	
	
@app.route('/form', methods=['GET','POST'])
def showForm():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	return render_template('form.html', user=user)
	
	
@app.route('/form2', methods=['GET','POST'])
def showForm2():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	fname=request.form['fname']
	firstname=fname
	lname=request.form['lname']
	email=request.form['email']
	zipcode=request.form['zipcode']
	pw1=request.form['pw1']
	pw2=request.form['pw2']
	dob=request.form['dob']
	if request.method == 'POST':
		
		if (fname != "" and lname != "" and email != "" and pw1 == pw2):
			try:
				results = pg.newMember(fname, lname, email, dob, zipcode, pw1)
				if results == None:
					return render_template('badform.html')
			except:
				print("ERROR INSERTING INTO login")
			try:
				results = pg.currentRoster()
			except:
				print("ERROR executing select")
			return render_template('form2.html', fname=fname, results=results, user=user)
		else:
			return render_template('badform.html', fname=fname, lname=lname, email=email, pw1=pw1, pw2=pw2, dob=dob, zipcode=zipcode)
	else:
		return render_template('form3.html', results=results, user=user)


@app.route('/form3', methods=['GET','POST'])
def showForm3():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	try:
		results = pg.currentRoster()
	except:
		print("Error executing select")
	return render_template('form3.html', results=results, user=user)


@app.route('/login', methods=['GET','POST'])
def showLogin():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	return render_template('login.html', user=user)
	
	
@app.route('/search', methods=['GET','POST'])
def showSearch():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	return render_template('search.html', user=user)
	
	
@app.route('/searchresults', methods=['GET','POST'])
def showSearchResults():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	try:
		search=request.form['search']
		cat=request.form['cat']
		zipcode=user[3]
		print("Search Term: " , search)
		print("Category   : " , cat)
	except:
		print("Error fetching search term")
		#//try:
	results = pg.superSearch(user[3], cat, search)
#	except:
	#	print("Error executing SuperSearch")
	print "SHOW: ", results
	
	return render_template('searchresults.html', user=user, results=results, search=search)
	
	
	
	
@app.route('/logout', methods=['GET','POST'])
def logout():
	session.pop('username')
	user = ['','','','']
	return render_template('login.html', user=user)
	

@app.route('/gallery')
def showGallery():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode']]
	else:
		user = ['','','','']
	p1 = '/static/faceboard/1.jpg'
	p2 = '/static/faceboard/2.jpg'
	p3 = '/static/faceboard/3.jpg'
	p4 = '/static/faceboard/4.jpg'
	p5 = '/static/faceboard/5.jpg'
	p6 = '/static/faceboard/6.jpg'
	p7 = '/static/faceboard/Thor.jpg'
	photos = {p7, p1, p2, p3, p4, p5, p6}
	return render_template('gallery.html', photos=photos, user=user)

	
# Start the server
if __name__ == '__main__':
	app.run(host=os.getenv('IP', "0.0.0.0"), port =int(os.getenv('PORT', 8080)), debug=True)