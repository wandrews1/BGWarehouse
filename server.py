from datetime import datetime
from datetime import timedelta
import os
import psycopg2
import psycopg2.extras
import uuid
import binascii
from lib.config import *
from lib import data_postgresql as pg
from flask import Flask, render_template, request, redirect, session, flash, url_for, g, abort, Session
from flask_socketio import SocketIO, emit, send
from flask_mail import Mail, Message

# create the application instance
app = Flask(__name__) 

# Flask_mail credentials. 
#Stored in separate file for obfuscational security.
app.config.update(dict(
    DEBUG = confDEBUG,
    MAIL_SERVER = confMAIL_SERVER,
    MAIL_PORT = confMAIL_PORT,
    MAIL_USE_TLS = confMAIL_USE_TLS,
    MAIL_USE_SSL = confMAIL_USE_SSL,
    MAIL_USERNAME = confMAIL_USERNAME,
    MAIL_PASSWORD = confMAIL_PASSWORD,
))

# initialize the Flask_Mail app
mail = Mail(app)

# no peaking
app.secret_key = binascii.hexlify(os.urandom(24))

# user variables, used for Flask_session
username = ''
password = ''
firstname = ''
zipcode = ''
lastname = ''
level = ''
cart = []
currentBasket = []

# Flask_socketIO initialization
socketio = SocketIO(app)

usernames = {}



# SHOPPING CART
# Each item will have all of these parameters in bg.sql
class Item(object): 
	def __init__(self, name, description, productID, price, quantity, cat):
		self._name = name
		self._description = description
		self._productID = productID
		self._price = price
		self._quantity = quantity
		self._cat = cat

	def __str__(self):
		return (self._name)
		
	def __repr__(self):
		return (str(self._productID))

	# Mutator methods for Item class
	def set_description(self, description):
		self._description = description
		
	def set_price(self, price):
		self._price = price
		
	def set_quantity(self, quantity):
		self._quantity = quantity
		
	def set_vat(self, cat):
		self._cat = cat
		
	# Accessor methods for Item class
	def get_name(self):
		return self._name
				
	def get_description(self):
		return self._description
				
	def get_productID(self):
		return self._productID
		
	def get_price(self):
		return self._price
		
	def get_quantity(self):
		return self._quantity 
				
	def get_cat(self):
		return self._cat
		
	def get_total_item_price(self): 
		return self._price * self._quantity
	
class Basket(object):
	def __init__(self):
		self._items = []
		self._price = 0 
		self._count = 0
		self._current = 0
		
	def __str__(self):
		output = ("Items currently in your basket: ")
		for x in self._items:
			output += x.get_name() + ", " # Add each item to the string, followed by a comma
		return output[0:-2] + "." # When the final item in the string is reached, remove the comma and add a full stop

			
	def __repr__(self):
		for x in self._items:
			return str(x)
			
	def __iter__(self):
		return self

	def next(self): # Python 3: def __next__(self)
		if self._current > self._count:
			raise StopIteration
		else:
			self._current += 1
			return self._current - 1
		
	def get_price(self):
		return self._price
		
	def get_items(self):
		return self._items
		
	def add_item(self, item): 
		if item in self._items:
			item.set_quantity(item.get_quantity()+1)
			self._price += item.get_price()
			self._count += 1
		else:
			self._items.append(item) # Add item to the current list of items 
			self._price += item.get_price() # Add price of current item to the price of items already added 
			self._count += 1 # Add to the total number of items held within the cart
		
	def remove_item(self, item):
		for i in self._items:
			if item == i.get_productID:
				self._items.remove(item)
				self._price -= item.get_price()
				self._count -= 1
		return(self)

with app.test_request_context():
	currentBasket = Basket()
	# session['currentBasket'] = currentBasket
	print("New Basket Created")
	
# session["cart"] = currentBasket.__dict__

# @socketio.on('message')
# def handle_message(message):
#     print('received message: ' + message)


@app.route('/', methods=['GET','POST'])
def mainIndex():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']
		
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
		
	return render_template('login.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
	

@app.route('/addwarehouse', methods=['GET', 'POST'])
def showAddWarehouse():
	
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
	
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']

		if (user[5] == 'Administrator'):
			return render_template('addwarehouse.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
		else:
			return render_template('forbidden.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
	else:
		user = ['','','','','','','']
		# currentBasket = ['']
		return render_template('search.html', user=user, cartCount=cartCount)
		
	if request.method == 'POST':
		owner = request.form['owner']
		name=request.form['name']
		address=request.form['address']
		city=request.form['city']
		state=request.form['state']
		zipcode = request.form['zipcode']
		level = request.form['level']
	
	return render_template('addwarehouse.html', user=user, currentBasket=currentBasket, cartCount=cartCount)	

		
@app.route('/warehouseresults', methods=['GET', 'POST'])
def showWarehouseresults():
	noresults = 0
	noemail = 0
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']
	
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
	if request.method == 'POST':	
		try:
			print("ADD WAREHOUSE POST")
			owner = request.form['owner']
			name=request.form['name']
			address=request.form['address']
			city=request.form['city']
			state=request.form['state']
			zipcode = request.form['zipcode']
			level = request.form['level']
			print("***Owner: , NAME: , ADDRESS , CITY, STATE, ZIPCODE, LEVEL: " , owner, name, address, city, state, zipcode, level)
		except:
			print("Error fetching removal characteristics")
			
	print("***Owner: , NAME: , ADDRESS , CITY, STATE, ZIPCODE, LEVEL: " , owner, name, address, city, state, zipcode, level)

	emailcheck = pg.checkEmail(owner)
	if emailcheck == 'No Email Match.':
		noemail = 1
		return render_template('warehouseresults.html', user=user, noresults=noresults, owner=owner, noemail=noemail, currentBasket=currentBasket, cartCount=cartCount)
	else:
		results = pg.addWarehouse(owner, name, address, city, state, zipcode, level)
		print("SHOW: ", results)
		if results == 'No Results.':
			noresults = 1
		return render_template('warehouseresults.html', user=user, noresults=noresults, owner=owner, noemail=noemail, currentBasket=currentBasket, cartCount=cartCount)

	# results = pg.alterCustomer(custemail, fname, lname, zipcode, password)
	# print("SHOW: ", results)
	# if results == 'No Results.':
	# 	noresults = 1
	return render_template('warehouseresults.html', user=user, noresults=noresults, owner=owner, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/manager', methods=['GET','POST'])
def showManager():
	
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
	
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']

		if (user[5] == 'Administrator') or (user[5] == 'Manager'):
			return render_template('manager.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
		else:
			return render_template('forbidden.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
	else:
		user = ['','','','','','','']
		return render_template('search.html', user=user, currentBasket=currentBasket, cartCount=cartCount)	


@app.route('/sales')
def showSales():
	
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']

		if (user[5] == 'Administrator') or (user[5] == 'Manager') or (user[5] == 'Sales Associate'):
			return render_template('sales.html', user=user, currentBasket=currentBasket)
		else:
			return render_template('forbidden.html', user=user, currentBasket=currentBasket)
	else:
		user = ['','','','','','','']

		return render_template('search.html', user=user, currentBasket=currentBasket, cartCount=cartCount)	


@app.route('/profile', methods=['GET','POST'])
def showProfile():
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
	
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']

		return render_template('profile.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
	else:
		user = ['','','','','','','']
		return render_template('login.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/invoice', methods=['GET','POST'])
def showInvoice():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']

	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0

	invoicenum = 1
		
	msg = Message("Hi %s! Your BG Invoice #%s" % (user[2], invoicenum),
		sender=("BG Sales Team","bgsalestest@gmail.com"),
		recipients=[user[0]])
	
	assert msg.sender == "BG Sales Team <bgsalestest@gmail.com>"
	msg.body="testing 1 - This is the test body. The main text of the email shall go here"
	
	msg.html=showInvoiceMaker(user,invoicenum)

	invoicenum = invoicenum + 1
	
	mail.send(msg)

	return render_template('invoice.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


def showInvoiceMaker(user, invoicenum):

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']

	mylist = []
	today = datetime.today().strftime('%Y-%m-%d')
	due1 = datetime.today()+ timedelta(days=30) 
	due = due1.strftime('%Y-%m-%d')
	mylist.append(today)
	mylist.append(due)
	
	timenow = mylist[0]
	timedue = mylist[1]

	message = """
	<!doctype html>
	<html>
		<head>
		    <meta charset="utf-8">
		    <title>Your Invoice</title>
		    
		    <style>
		    .invoice-box {
		        max-width: 800px;
		        margin: auto;
		        padding: 30px;
		        border: 1px solid #eee;
		        box-shadow: 0 0 10px rgba(0, 0, 0, .15);
		        font-size: 16px;
		        line-height: 24px;
		        font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
		        color: #555;
		    }
		    
		    .invoice-box table {
		        width: 100%%;
		        line-height: inherit;
		        text-align: left;
		    }
		    
		    .invoice-box table td {
		        padding: 5px;
		        vertical-align: top;
		    }
		    
		    .invoice-box table tr td:nth-child(2) {
		        text-align: right;
		    }
		    
		    .invoice-box table tr.top table td {
		        padding-bottom: 20px;
		    }
		    
		    .invoice-box table tr.top table td.title {
		        font-size: 45px;
		        line-height: 45px;
		        color: #333;
		    }
		    
		    .invoice-box table tr.information table td {
		        padding-bottom: 40px;
		    }
		    
		    .invoice-box table tr.heading td {
		        background: #eee;
		        border-bottom: 1px solid #ddd;
		        font-weight: bold;
		    }
		    
		    .invoice-box table tr.details td {
		        padding-bottom: 20px;
		    }
		    
		    .invoice-box table tr.item td{
		        border-bottom: 1px solid #eee;
		    }
		    
		    .invoice-box table tr.item.last td {
		        border-bottom: none;
		    }
		    
		    .invoice-box table tr.total td:nth-child(2) {
		        border-top: 2px solid #eee;
		        font-weight: bold;
		    }
		    
		    @media only screen and (max-width: 600px) {
		        .invoice-box table tr.top table td {
		            width: 100%%;
		            display: block;
		            text-align: center;
		        }
		        
		        .invoice-box table tr.information table td {
		            width: 100%%;
		            display: block;
		            text-align: center;
		        }
		    }
		    
		    /** RTL **/
		    .rtl {
		        direction: rtl;
		        font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
		    }
		    
		    .rtl table {
		        text-align: right;
		    }
		    
		    .rtl table tr td:nth-child(2) {
		        text-align: left;
		    }
		    </style>
		</head>
		
		<body>
		    <div class="invoice-box">
		        <table cellpadding="0" cellspacing="0">
		            <tr class="top">
		                <td colspan="2">
		                    <table>
		                        <tr>
		                            <td class="title">
		                                <img src="http://pictures.dealer.com/m/mclartyfordfd/0187/c7ab71a49478cc4ad914a4dd52779aeax.jpg" style="width:100%%; max-width:300px;">
		                            </td>
		                            
		                            <td>
		                                Invoice #: %s<br>
		                                Created: %s<br>
		                                Due: %s
		                            </td>
		                        </tr>
		                    </table>
		                </td>
		            </tr>
		            
		            <tr class="information">
		                <td colspan="2">
		                    <table>
		                        <tr>
		                            <td>
		                                BG of Central Virginia<br>
		                                116 Sylvia Rd<br>
		                                Ashland, VA 23005
		                            </td>
		                            
		                            <td>
		                                %s<br>
		                                %s<br>
		                                User Level: %s
		                            </td>
		                        </tr>
		                    </table>
		                </td>
		            </tr>
		            
		            <tr class="heading">
		                <td>
		                    Item
		                </td>
		                
		                <td>
		                    Price
		                </td>
		            </tr>
		            
		            <tr class="item">
		                <td>
		                    Website design
		                </td>
		                
		                <td>
		                    $300.00
		                </td>
		            </tr>
		            
		            <tr class="item">
		                <td>
		                    Hosting (3 months)
		                </td>
		                
		                <td>
		                    $75.00
		                </td>
		            </tr>
		            
		            <tr class="item last">
		                <td>
		                    Domain name (1 year)
		                </td>
		                
		                <td>
		                    $10.00
		                </td>
		            </tr>
		            
		            <tr class="total">
		                <td></td>
		                
		                <td>
		                   Total: $385.00
		                </td>
		            </tr>
		        </table>
		    </div>
		</body>
	</html>
	"""
	messagef = message % (invoicenum, timenow, timedue, user[2]+" "+user[6], user[0], user[5])

	return messagef


@app.route('/remove', methods=['GET','POST'])
def showRemove():
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0	

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
		if(user[5] == 'Administrator') or (user[5] == 'Manager'):
			return render_template('remove.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
		else:
			return render_template('forbidden.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
	else:
		user = ['','','','','','','']
		return render_template('search.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/removeresults', methods=['GET','POST'])
def showRemoveResults():
	noresults = 0
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']

	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0

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
	if results == 'No Results.':
		noresults = 1
	
	return render_template('removeresults.html', user=user, results=results, noresults = noresults, fname=fname, lname=lname, userlevel=userlevel, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/altercustomer', methods=['GET', 'POST'])
def showAlterCust():
	
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
	
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		
		if(user[5] == 'Administrator') or (user[5] == 'Manager') or (user[5] == 'Sales Associate'):
			return render_template('altercustomer.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
		else:
			return render_template('forbidden.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
	else:
		user = ['','','','','','','']
		return render_template('search.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
	
	return render_template('altercustomer.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/alterresults', methods=['GET', 'POST'])
def showAlterResults():
	noresults = 0
	noemail = 0
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']
	
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
		
	try:
		custemail=request.form['custemail']
		fname=request.form['fname']
		lname=request.form['lname']
		zipcode=request.form['zipcode']
		password=request.form['password']
		print("***FName: , LNAME: , EMAIL , ZIPCODE, PASS: " , fname, lname, zipcode, password)
	except:
		print("Error fetching removal characteristics")
		
	print("***FName: , LNAME: , EMAIL , ZIPCODE, PASS: " , fname, lname, zipcode, password)

	emailcheck = pg.checkAlterEmail(custemail)
	if emailcheck == 'No Email Match.':
		noemail = 1
		return render_template('alterresults.html', user=user, noresults=noresults, custemail=custemail, noemail=noemail, currentBasket=currentBasket, cartCount=cartCount)
	else:
		results = pg.alterCustomer(custemail, fname, lname, zipcode, password)
		print("SHOW: ", results)
		if results == 'No Results.':
			noresults = 1
		return render_template('alterresults.html', user=user, noresults=noresults, custemail=custemail, noemail=noemail, currentBasket=currentBasket, cartCount=cartCount)

	results = pg.alterCustomer(custemail, fname, lname, zipcode, password)
	print("SHOW: ", results)
	if results == 'No Results.':
		noresults = 1
	return render_template('alterresults.html', user=user, noresults=noresults, custemail=custemail, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/form', methods=['GET','POST'])
def showForm():
	
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0

	
	print("-- in showForm()")
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]

		if(user[5] == 'Administrator') or (user[5] == 'Manager') or (user[5] == 'Sales Associate'):
			return render_template('form.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
		else:
			return render_template('forbidden.html', user=user, currentBasket=currentBasket, cartCount=cartCount)

		# cart = session['currentBasket']

	else:
		user = ['','','','','','','']
		return render_template('search.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


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
	
	return render_template('form.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/form2', methods=['GET','POST'])
def showForm2():
	print("-- in showForm2")
	
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']
		
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0

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
					return render_template('badform.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
			except:
				print("ERROR INSERTING INTO login")
			return render_template('form2.html', fname=fname, lname=lname, user=user, email=email, zipcode=zipcode, userlevel=userlevel, currentBasket=currentBasket, cartCount=cartCount)
		else:
			print("ERROR 4")
			return render_template('badform.html', user=user, fname=fname, lname=lname, email=email, pw1=pw1, pw2=pw2, zipcode=zipcode, userlevel=userlevel, cartCount=cartCount, currentBasket=currentBasket)
	else:
		print("ERROR 5")
		return render_template('form3.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/form3', methods=['GET','POST'])
def showRoster():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# currentBasket = [session['currentBasket']]
	else:
		user = ['','','','','','','']
		
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
		
	try:
		results = pg.currentRoster()
	except:
		print("Error executing select")
	return render_template('form3.html', results=results, user=user, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/login', methods=['GET','POST'])
def showLogin():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']

	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0


	if request.method == 'POST':
		email=request.form['username']
		pw=request.form['password']
		if (email != "" and pw == pw2):
			try:
				if results == None:
					return render_template('login.html')
			except:
				print("ERROR logging in")
				
		
	return render_template('login.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


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
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']
		
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0
	
	return render_template('search.html', user=user, cartCount=cartCount, currentBasket=currentBasket)


@app.route('/manageitems', methods=['GET','POST'])
def showManageItems():
	
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
		
		try:
			cartCount = 0
			for item in currentBasket.get_items():
				print(item.get_name())
				cartCount += item.get_quantity()
		except:
			cartCount = 0
		
		if (user[5] == 'Administrator') or (user[5] == 'Manager'):
			return render_template('manageitems.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
		else:
			return render_template('forbidden.html', user=user, currentBasket=currentBasket, cartCount=cartCount)
	else:
		user = ['','','','','','','']
		return render_template('login.html', user=user, currentBasket=currentBasket, cartCount=cartCount)


@app.route('/searchresults', methods=['GET','POST'])
def showSearchResults():

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']
	
	try:
		search=request.form['search']
		print("***Search Term: " , search)
	except:
		print("Error fetching search term")
	
	results = pg.superSearch(search)
	
	items = []
	for item in results:
		itemInfo = pg.getItemInfo(item[0])
		print("get: ",item[0])
		print("0: ",itemInfo[0])
		print("1: ",itemInfo[1])
		print("2 ",itemInfo[2])
		print("3: ",itemInfo[3])
		print("4: ",itemInfo[4])
		# print("5: ",itemInfo[5])
		newItem = Item(itemInfo[3],itemInfo[4],itemInfo[0],float(itemInfo[1]),1,itemInfo[2])
		items.append(newItem)
		print(newItem.get_name())
		
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0

	
	print("SHOW: ", results)
	
	return render_template('searchresults3.html', user=user, results=results, search=search, items=items, cartCount=cartCount, currentBasket=currentBasket)


# @app.route('/addToCart', methods=['GET','POST'])
# def addToCart(item)


@app.route('/cart', methods=['GET','POST'])
def showCart():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']

	# TESTING EXAMPLE
	try:
		# itemQuantity = pg.getItemQuantity(PID,WID)
		itemInfo = pg.getItemInfo(841)
		newItem = Item(itemInfo[3],itemInfo[4],itemInfo[0],float(itemInfo[1]),1,itemInfo[2])
		currentBasket.add_item(newItem)
		
		itemInfo = pg.getItemInfo(985)
		newItem = Item(itemInfo[3],itemInfo[4],itemInfo[0],float(itemInfo[1]),1,itemInfo[2])
		currentBasket.add_item(newItem)
		currentBasket.add_item(newItem)
		currentBasket.add_item(newItem)
		# REMOVE QUANTITY FROM WID
	except:
		print("Error putting item in cart")
	# END TESTING EXAMPLE
		
	try:
		i = 1
		for item in currentBasket.get_items():
			print(i,item.get_productID(),item.get_quantity(),item.get_price(),round(item.get_total_item_price(),2))
			print("testing append")
			cart.append(item)
			# cart.append(i,item.get_productID(),item.get_quantity(),item.get_price(),round(item.get_total_item_price(),2))
			i+=1
			print("end of item")
		print("out of loop, total is next")
		print("Total: $$$", round(currentBasket.get_price(),2))
	except:
		print("Cart is empty?")

		
	try:
		cartCount = 0
		for item in currentBasket.get_items():
			print(item.get_name())
			cartCount += item.get_quantity()
	except:
		cartCount = 0

	return render_template('cart.html', user=user, cart=cart, cartCount=cartCount, currentBasket=currentBasket)


def listCartItems():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		# cart = session['currentBasket']
	else:
		user = ['','','','','','','']
	try:
		i = 1
		for item in currentBasket.get_items():
			print(i,item.get_productID(),item.get_quantity(),item.get_price(),round(item.get_total_item_price(),2))
			cart.append(i,item.get_productID(),item.get_quantity(),item.get_price(),round(item.get_total_item_price(),2))
			i+=1
		print("Total: $$$", round(currentBasket.get_price(),2))
		return cart
	except:
		print("Cart is empty?")
		return cart
	return render_template('cart.html', user=user, currentBasket=currentBasket)


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
		currentBasket = ['']
		flash('You were logged out')
		return render_template('login.html', user=user, currentBasket=currentBasket)
	except:
		user = ['','','','','','','']
		currentBasket = ['']
		return render_template('login.html', user=user, currentBasket=currentBasket)


# Start the server
if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=8080, debug=True)
