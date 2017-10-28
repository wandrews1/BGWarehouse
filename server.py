#import datetime
import os
import psycopg2
import psycopg2.extras
import uuid
import binascii
from lib.config import *
from lib import data_postgresql as pg
from flask import Flask, render_template, request, redirect, session, flash, url_for, g, abort
from flask_socketio import SocketIO, emit, send

app = Flask(__name__) # create the application instance
app.secret_key = binascii.hexlify(os.urandom(24))

username = ''
password = ''
firstname = ''
zipcode = ''
lastname = ''
level = ''
address = ''


socketio = SocketIO(app)

usernames = {}

@socketio.on('connect', namespace = '/chat')
def makeConnection():
	print('BEFORE CONNECTED')
	session['uuid'] = uuid.uuid1()
	print('*** Connected ***')
	usernames[session['uuid']] = {'username': 'New User'}

	for message in pg.printMessages():
		print(message)
		emit('message', {'text': message[2], 'name': message[0] + " " + message[1]})
		
		
@socketio.on('message', namespace = '/chat')
def new_message(message):
	person = session['firstname'] + " " + session['lastname']
	tmp = {'text': message, 'name': person}
	print(tmp)
	#messages.append(tmp)
	pg.newMessage(session['firstname'],session['lastname'],message)
	emit('message',tmp,broadcast=True)


@socketio.on('identify', namespace = '/chat')
def on_identify(value):
	print('Searching FaceChat for: ' + value)
	usernames[session['uuid']] = {'username': value}
	print(session['uuid'])

	for message in pg.searchMessages(value):
		print(message)
		emit('identify', {'text': message[2], 'name': message[0] + " " + message[1]})
	
	
	
@socketio.on('search', namespace = '/chat')
def search_Chat(value):
	print('Searching for: ' + value)
	usernames[session['uuid']] = {'username': value}
	session['uuid'] = uuid.uuid1()
	#print(' found ' + value)
	#pg.chatSearch(value)
	for message in pg.chatSearch(value):
		print(message)
		emit('message', {'text': message[2], 'name': message[0] + " " + message[1]})

 

@app.route('/', methods=['GET','POST'])
def mainIndex():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	return render_template('login.html', user=user)
	

@app.route('/admin')
def showAdmin():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	return render_template('admin.html', user=user)

	
@app.route('/manager', methods=['GET','POST'])
def showManager():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	return render_template('manager.html', user=user)
	
@app.route('/sales')
def showSales():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	return render_template('sales.html', user=user)
	
@app.route('/profile', methods=['GET','POST'])
def showProfile():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	return render_template('profile.html', user=user)
	
# @app.route('/chat', methods=['GET','POST'])
# def showChat():
#	if 'username' in session:
#		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
#	else:
#		user = ['','','','','','','','']
# 	return render_template('chat.html', user=user)
	


@app.route('/form', methods=['GET','POST'])
def showForm():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	return render_template('form.html', user=user)
	

@app.route('/form2', methods=['GET','POST'])
def showForm2():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	fname=request.form['fname']
	firstname=fname
	lname=request.form['lname']
	email=request.form['email']
	zipcode=request.form['zipcode']
	pw1=request.form['pw1']
	pw2=request.form['pw2']
	dob=request.form['dob']
	level=request.form['level']
	if request.method == 'POST':
		
		if (fname != "" and lname != "" and email != "" and pw1 == pw2):
			try:
				results = pg.newMember(fname, lname, email, dob, zipcode, pw1, level)
				if results == None:
					return render_template('badform.html')
			except:
				print("ERROR INSERTING INTO login")
			try:
				results = pg.currentRoster()
			except:
				print("ERROR executing select")
			return render_template('login.html', fname=fname, results=results, user=user, level=level)
		else:
			return render_template('badform.html', fname=fname, lname=lname, email=email, pw1=pw1, pw2=pw2, dob=dob, zipcode=zipcode, level=level)
	else:
		return render_template('form3.html', results=results, user=user, level=level)


@app.route('/form3', methods=['GET','POST'])
def showRoster():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	try:
		results = pg.currentRoster()
	except:
		print("Error executing select")
	return render_template('form3.html', results=results, user=user)


@app.route('/login', methods=['GET','POST'])
def showLogin():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']

	if request.method == 'POST':
		email=request.form['username']
		pw=request.form['password']
		if (email != "" and pw == pw2):
			try:
				if results == None:
					return render_template('login.html')
			except:
				print("ERROR INSERTING INTO login")
				
		
	return render_template('login.html', user=user)
	
	
@app.route('/search', methods=['GET','POST'])
def showSearch():
	
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['password'] = request.form['password']
		try:
			session['firstname'] = pg.getFirstName(session['username'],session['password'])
			session['lastname'] = pg.getLastName(session['username'],session['password'])
			session['zipcode'] = pg.getZip(session['username'],session['password'])
			session['level'] = pg.getLevel(session['username'],session['password'])
			session['address'] = pg.getAddress(session['username'],session['password'])
		except:
			return render_template('badlogin.html')
		

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	return render_template('search.html', user=user)
	
	
	
@app.route('/searchresults', methods=['GET','POST'])
def showSearchResults():

	# if request.method == 'POST':
	# 	session['username'] = request.form['username']
	# 	session['password'] = request.form['password']
	# 	session['firstname'] = pg.getFirstName(session['username'],session['password'])
	# 	session['lastname'] = pg.getLastName(session['username'],session['password'])
	# 	session['zipcode'] = pg.getZip(session['username'],session['password'])
		

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname'],session['address']]
	else:
		user = ['','','','','','','','']
	try:
		search=request.form['search']
		# cat=request.form['cat']
		# zipcode=user[3]
		print("***Search Term: " , search)
		# print("Category   : " , cat)
	except:
		print("Error fetching search term")
	# results = pg.superSearch(user[3], cat, search)
	print("***Search Term: " , search)
	results = pg.superSearch(search)
	print("SHOW: ", results)
	
	return render_template('searchresults.html', user=user, results=results, search=search)
	
	
	
	
@app.route('/logout', methods=['GET','POST'])
def logout():
	session.pop('username', None)
	session.pop('firstname')
	session.pop('zipcode')
	session.pop('password')
	session.pop('level')
	session.pop('address')
	session.pop('lastname')
	user = ['','','','','','','','']
	flash('You were logged out')
	return render_template('login.html', user=user)
	


	
# Start the server
if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=8080, debug=True)
	
	
# # start the server - Use this one without Socket IO
# if __name__ == '__main__':
# 	app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)
	
