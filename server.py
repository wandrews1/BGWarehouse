from datetime import datetime
from datetime import timedelta
import os
import psycopg2
import psycopg2.extras
import uuid
import binascii
from lib.config import *
from lib import data_postgresql as pg
from flask import Flask, render_template, request, redirect, session, flash, url_for, g, abort
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

# Flask_socketIO initialization
socketio = SocketIO(app)

usernames = {}


@app.route('/', methods=['GET','POST'])
def mainIndex():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		cart = [session['cart']]
	else:
		user = ['','','','','','','']
		cart = []
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
		return render_template('profile.html', user=user)
	else:
		user = ['','','','','','','']
		return render_template('login.html', user=user)


@app.route('/invoice', methods=['GET','POST'])
def showInvoice():
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
	else:
		user = ['','','','','','','']

	invoicenum = 1
		
	msg = Message("Hi %s! Your BG Invoice #%s" % (user[2], invoicenum),
		sender=("BG Sales Team","bgsalestest@gmail.com"),
		recipients=[user[0]])
	
	assert msg.sender == "BG Sales Team <bgsalestest@gmail.com>"
	msg.body="testing 1 - This is the test body. The main text of the email shall go here"
	
	msg.html=showInvoiceMaker(user,invoicenum)

	invoicenum = invoicenum + 1
	
	mail.send(msg)

	return render_template('invoice.html', user=user)


def showInvoiceMaker(user, invoicenum):

	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
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
	noresults = 0
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
	if results == 'No Results.':
		noresults = 1
	
	return render_template('removeresults.html', user=user, results=results, noresults = noresults, fname=fname, lname=lname, userlevel = userlevel)


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
			return render_template('form2.html', fname=fname, lname=lname, user=user, email=email, zipcode=zipcode, userlevel=userlevel)
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
	results = pg.superSearch(search)
	print("SHOW: ", results)
	
	return render_template('searchresults.html', user=user, results=results, search=search)
	



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
		return ("Item: " + self._name + "\nDescription: " + self._description + "\nProductID: " + str(self._productID) + "\nPrice: $" + int(self._price) + "\nQuantity: " + str(self._quantity) + "\nCategory: " + str(self._cat))
		
	def __repr__(self):
		return ("Item(" + self._name + ", " + self._description + ", " + self._productID + ", " + self._price + ", " + self._quantity + ", " + self._cat + ")")

	# Mutator methods for Item class
	def set_description(self, description):
		self._description = description
		
	def set_price(self, price):
		self._price = price
		
	def set_units(self, quantity):
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
		
	def __str__(self):
		output = ("Items currently in your basket: ")
		for x in self._items:
			output += x.get_name() + ", " # Add each item to the string, followed by a comma
		return output[0:-2] + "." # When the final item in the string is reached, remove the comma and add a full stop

			
	def __repr__(self):
		for x in self._items:
			return str(x)
		
	def get_price(self):
		return self._price
		
	def get_items(self):
		return self._items
		
	def add_item(self, item): 
		self._items.append(item) # Add item to the current list of items 
		self._price += item.get_price() # Add price of current item to the price of items already added 
		
	def remove_item(self, item):
		for x in self._items:
			if item == x:
				self._items.remove(item)
				self._price -= item.get_price()
		return(currentBasket)


# item = pg.getItemInfo(841)

item = pg.getItemQuantity(841,4)
print(item)
# book = Item('Pride and Prejudice', 'Jane Austen', '4394839', 10, '1', '0.1')

# currentBasket = Basket() 
# currentBasket.add_item(book)


	

def addToCart(item):
	if 'username' in session:
		user = [session['username'],session['password'],session['firstname'],session['zipcode'],' - Logout',session['level'],session['lastname']]
		cart = [session['cart']]
	else:
		user = ['','','','','','','']
		cart = []
	return render_template('login.html', user=user)
	
	# book = Item('Pride and Prejudice', 'Jane Austen', '4394839', 10, '1', '0.1')
	
	# currentBasket = Basket() 
	# currentBasket.add_item(book)


	
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
