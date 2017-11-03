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
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
	return render_template('login.html', user=user)
	

@app.route('/addwarehouse')
def showAddWarehouse():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		if (user[5] == 'Administrator'):
			return render_template('addwarehouse.html', user=user)
		else:
			return render_template('forbidden.html', user=user)
	else:
		user = ['','','','','','','']
		return render_template('search.html', user=user)	




	
@app.route('/manager', methods=['GET','POST'])
def showManager():
	
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		if (user[5] == 'Administrator') or (user[5] == 'Manager'):
			return render_template('manager.html', user=user)
		else:
			return render_template('forbidden.html', user=user)
	else:
		user = ['','','','','','','']
		return render_template('search.html', user=user)	

	
@app.route('/sales')
def showSales():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		if (user[5] == 'Administrator') or (user[5] == 'Manager') or (user[5] == 'Sales Associate'):
			return render_template('sales.html', user=user)
		else:
			return render_template('forbidden.html', user=user)
	else:
		user = ['','','','','','','']
		return render_template('search.html', user=user)	

	
@app.route('/profile', methods=['GET','POST'])
def showProfile():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
	return render_template('profile.html', user=user)
	

@app.route('/remove', methods=['GET','POST'])
def remove():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		if(user[5] == 'Administrator') or (user[5] == 'Manager'):
			return render_template('remove.html', user = user)
		else:
			return render_template('forbidden.html', user = user)
	else:
		user = ['','','','','','','']
		return render_template('search.html', user = user)
		
	return render_template('remove.html', user=user)
	
@app.route('/removeresults', methods=['GET','POST'])
def showRemoveResults():

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
	try:
		fname=request.form['fname']
		lname=request.form['lname']
		email=request.form['email']
		userlevel=request.form['userlevel']
		print("***FName: , LNAME: , EMAIL , LEVEL: " , fname, lname, email, userlevel)
	except:
		print("Error fetching removal characteristics")
	
	print("***FName: , LNAME: , EMAIL , LEVEL: " , fname, lname, email, userlevel)
	results = pg.removeUser(fname, lname, email, userlevel)
	print("SHOW: ", results)
	
	return render_template('removeresults.html', user=user, results=results, fname=fname, lname=lname, userlevel = userlevel)
# @app.route('/chat', methods=['GET','POST'])
# def showChat():
#	if 'username' in session:
#		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
#	else:
#		user = ['','','','','','','']
# 	return render_template('chat.html', user=user)
	


@app.route('/form', methods=['GET','POST'])
def showForm():
	print("-- in showForm()")
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
		
	
	if request.method == 'POST':
		fname=request.form['fname']
		firstname=fname
		lname=request.form['lname']
		email=request.form['email']
		zipcode=request.form['zipcode']
		pw1=request.form['pw1']
		pw2=request.form['pw2']
		dob=request.form['dob']
		level=request.form['level']
		print(fname)
		print(lname)
		print(email)
		print(zipcode)
		print(pw1)
		print(pw2)
		print(dob)
		print(level)
	print("end of function")
	
	return render_template('form.html', user=user)
	

@app.route('/form2', methods=['GET','POST'])
def showForm2():
	print("-- in showForm2")
	
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
		

	if request.method == 'POST':
		print("-- METHOD IS POST")
		try:
			fname=request.form['fname']
			lname=request.form['lname']
			email=request.form['email']
			zipcode=request.form['zipcode']
			pw1=request.form['pw1']
			pw2=request.form['pw2']
			userlevel=request.form.get('userlevel')
			print(">>>> *** This worked!" , userlevel)
		except:
			print(">>>> *** Error fetching search term")

		if (fname != "" and lname != "" and email != "" and userlevel != "" and pw1 == pw2):
			try:
				print("Trying 1")
				results = pg.newMember(email, fname, lname, pw1, zipcode, userlevel)
				print("pg.newMember worked!")
				if results == None:
					print("ERROR 2")
					return render_template('badform.html', user=user)
			except:
				print("ERROR INSERTING INTO login")
			return render_template('form2.html', fname=fname, user=user, userlevel=userlevel)
		else:
			print("ERROR 4")
			return render_template('badform.html', user=user, fname=fname, lname=lname, email=email, pw1=pw1, pw2=pw2, zipcode=zipcode, userlevel=userlevel)
	else:
		print("ERROR 5")
		return render_template('form3.html', user=user)


@app.route('/form3', methods=['GET','POST'])
def showRoster():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
	try:
		results = pg.currentRoster()
	except:
		print("Error executing select")
	return render_template('form3.html', results=results, user=user)


@app.route('/login', methods=['GET','POST'])
def showLogin():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']

	if request.method == 'POST':
		email=request.form['username']
		pw=request.form['password']
		if (email != "" and pw == pw2):
			try:
				if results == None:
					return render_template('login.html')
			except:
				print("ERROR logging in")
				
		
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
		except:
			return render_template('badlogin.html')

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
	return render_template('search.html', user=user)
	
	
	
@app.route('/searchresults', methods=['GET','POST'])
def showSearchResults():

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
	try:
		search=request.form['search']
		print("***Search Term: " , search)
	except:
		print("Error fetching search term")
	print("***Search Term: " , search)
	results = pg.superSearch(search)
	print("SHOW: ", results)
	
	return render_template('searchresults.html', user=user, results=results, search=search)
	
	
	
	
@app.route('/logout', methods=['GET','POST'])
def logout():
	try:
		session.pop('username', None)
		session.pop('firstname')
		session.pop('zipcode')
		session.pop('password')
		session.pop('level')
		session.pop('lastname')
		user = ['','','','','','','']
		flash('You were logged out')
		return render_template('login.html', user=user)
	except:
		user = ['','','','','','','']
		return render_template('login.html', user=user)
	

# Start the server
if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=8080, debug=True)
