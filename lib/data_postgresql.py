# Billy Andrews
from datetime import date
import psycopg2
import psycopg2.extras
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from lib.config import *

def connectToPostgres():
	connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD,POSTGRES_HOST)
	print(connectionString)
	# BP2  Use try-except blocks
	try:
		print("*** Connected to database")
		return psycopg2.connect(connectionString)
	except Exception as e:    # BP2 especially this part where you print the exception
		print(type(e))
		print(e)
		print("*** Can't connect to database")
		return None
	

#

# generic execute statement
# select=True if it is a select statement
#        False if it is an insert
#
def execute_query(query, conn, select=True, args=None):
	print (" - in execute_query")
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	results1 = None
	print (query)
	print (args)
	quer = cur.mogrify(query, args)   # BP6  never use Python concatenation for database queries
	print (quer)
	try: 
		print (" - Trying cur.execute")
		cur.execute(quer)
		print (" - cur.execute has executed")
		if select:
			print (" - select = True")
			results1 = cur.fetchall()
			print (" - cur.fetchall just happened")
		conn.commit()   # BP5  commit and rollback frequently
		print (" - conn.commit()")
	except Exception as e:
		conn.rollback()
		print (" - conn.rollback()!!!!!!!!!!!!!!!!!!")
		print(type(e))
		print(e)
	cur.close()      # BP3 Dispose of old cursors as soon as possible
	print (" - cur.close()")
	print (" - RESULTS1 ",results1)
	return results1

#
#  app specific
#

def printMessages():
	print (" - in printMessages()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT * FROM messages" 
	results = execute_query(query_string, conn, select=True)
	conn.close()
	return results
	
def searchMessages(search):
	print (" - in searchMessages()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT * FROM messages WHERE message LIKE '%%s'%'" 
	print(" - Query String: " + query_string)
	results = execute_query(query_string, conn, select=True, args=(search,))
	print(" - Results: " , results)
	if results:
		return results
	else:
		return " - No luck finding your search term."
	conn.close()
	return results

def newMessage(fname, lname, message):
	print (" - in newMessage()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "INSERT INTO messages (fname, lname, message) VALUES (%s, %s, %s)" 
	execute_query(query_string, conn, select=False,  args=(fname, lname, message))
	conn.close()
	return 0
	
	
def chatSearch(search):
	print (" - in chatSearch()")
	conn = connectToPostgres()
	if conn == None:
		return None
	print (" - connected to database")

	query_string = "SELECT * FROM messages WHERE message LIKE %s"
	print(" - Query String: " + query_string)
	results2 = execute_query(query_string, conn, select=True, args=('%' + search + '%',))
	print(" - Results: " , results2)
	if results2:
		return results2
	else:
		return " - No luck finding your search term."
	conn.close()
	return results2

	
	
def newMember(email, fname, lname, pw1, zipcode, userLevel):
# def newMember(fname, lname, email, zipcode, pw1, userlevel):
	print (" - in newMember()")
	conn = connectToPostgres()
	print(conn)
	if conn == None:
		return None
	query_string = "INSERT INTO login (email, fname, lname, pw1, zipcode, userLevel) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s, %s)" 
	execute_query(query_string, conn, select=False,  args=(email, fname, lname, pw1, zipcode, userLevel))
	conn.close()
	return 0


def currentRoster():
	print (" - in currentRoster()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT fname, lname, email, zipcode FROM login"
	results = execute_query(query_string, conn, select=True)
	conn.close()
	return results

def removeUser(fname, lname, email, userlevel):
	print (" - in remove user()")
	noresults = ("No Results.")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "DELETE from login WHERE fname=%s and lname=%s and email=%s and userlevel=%s"
	results = execute_query(query_string, conn, select=False, args = (fname, lname, email, userlevel))
	print("-Results: ", results)
	
	if results:
		return results
	else:
		return noresults
	conn.close()
	return results
	
def alterCustomer(custemail, fname, lname, zipcode, password):
	noresults = ("No Results.")
	updateCust = ''
	updateCustvars = []
	updateCustnum = 0
	print("- in alter customer()")
	conn = connectToPostgres()
	if conn == None:
		return None
	if(fname != ""):
		updateCust = "fname = '" + fname + "'"
		updateCustvars.append(fname)
		updateCustnum+=1
	if(lname != ""):
		if(fname != ""):
			updateCust+= ", lname = '" + lname + "'"
			updateCustvars.append(lname)
			updateCustnum+=1
		else:
			updateCust = "lname = '" + lname + "'"
			updateCustvars.append(lname)
			updateCustnum+=1
	if(password != ""):
		if(fname != "") or (lname != ""):
			updateCust+= ", pw1 = crypt('" + password + "' , gen_salt('bf'))"
			updateCustvars.append(password)
			updateCustnum+=1
		else:
			updateCust = "pw1 = crypt('" + password + "', gen_salt('bf'))"
			updateCustvars.append(password)
			updateCustnum+=1
	if(zipcode != ""):
		if(fname != "") or (lname != "") or (password != ""):
			updateCust+= ", zipcode = '" + zipcode + "'"
			updateCustvars.append(zipcode)
			updateCustnum+=1
		else:
			updateCust = "zipcode = '" + zipcode + "'"
			updateCustvars.append(zipcode)
			updateCustnum+=1

	if(updateCustnum == 1):
		query_string = "UPDATE login SET " + updateCust + " WHERE email = '" + custemail + "'"
		results = execute_query(query_string, conn, select=False)
		return results
	elif(updateCustnum == 2):
		query_string = "UPDATE login SET " + updateCust + " WHERE email = '" + custemail + "'"
		results = execute_query(query_string, conn, select=False)
		return results
	elif(updateCustnum == 3):
		query_string = "UPDATE login SET " + updateCust + " WHERE email = '" + custemail + "'"
		results = execute_query(query_string, conn, select=False)
		return results
	elif(updateCustnum == 4):	
		query_string = "UPDATE login SET " + updateCust + " WHERE email = '" + custemail + "'"
		results = execute_query(query_string, conn, select=False)
		return results
	else:
		return noresults
	conn.close()
		
		
def superSearch(search):
	noresults = ("No Results.",)
	print (" - in superSearch()")
	conn = connectToPostgres()
	if conn == None:
		return None
	print (" - connected to database")

	query_string = "SELECT * FROM items WHERE (LOWER(productID) LIKE LOWER(%s)) OR (LOWER(category) LIKE LOWER(%s)) OR (LOWER(name) LIKE LOWER(%s)) OR (LOWER(description) LIKE LOWER(%s))"
	print(" - Query String: " + query_string)
	results = execute_query(query_string, conn, select=True, args=('%' + search + '%','%' + search + '%','%' + search + '%','%' + search + '%',))
	print(" - Results: " , results)

	if results:
		return results
	else:
		return noresults
	conn.close()
	return results
	


def login(email, pw1):
	print (" - in login()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT * FROM login WHERE email = %s AND pw1 = crypt(%s,pw1)"
	results = execute_query(query_string, conn, select=True, args=(email, pw1))
	if results:
		return "SUCCESS!"
	else:
		query_string = "SELECT * FROM login WHERE email = %s"
		results = execute_query(query_string, conn, select=True, args=(email,))
		if results:
			return "Invalid Password"
		else:
			return "Username does not exist"
	conn.close()
	return results
	
	
def getFirstName(email, pw1):
	print (" - in getFirstName()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT fname FROM login WHERE email = %s AND pw1 = crypt(%s,pw1)"
	print (" - Query String: ", query_string)
	results = execute_query(query_string, conn, select=True, args=(email, pw1))
	conn.close()
	return results[0][0]
	
	
def getLastName(email, pw1):
	print (" - in getLastName()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT lname FROM login WHERE email = %s AND pw1 = crypt(%s,pw1)"
	results = execute_query(query_string, conn, select=True, args=(email, pw1))
	conn.close()
	return results[0][0]
	
	
def getZip(email,pw1):
	print (" - in getZip()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT zipcode FROM login WHERE email = %s AND pw1 = crypt(%s,pw1)"
	results = execute_query(query_string, conn, select=True, args=(email, pw1))
	conn.close()
	return results[0][0]
	
def getLevel(email,pw1):
	print (" - in getLevel()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT userLevel FROM login WHERE email = %s AND pw1 = crypt(%s,pw1)"
	results = execute_query(query_string, conn, select=True, args=(email, pw1))
	conn.close()
	return results[0][0]
	
# select description from items where productID like (select itemid from invoiceItems where itemid like '206' AND invoiceid = 1);








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
	
	
	# Import item info from bg.sql method
	def getItemInfo(self, prodID):
		noresults = ("No Results.",)
		print (" - in getItemInfo()")
		conn = connectToPostgres()
		if conn == None:
			return None
		print (" - connected to database")
		query_string = "SELECT * FROM items WHERE (LOWER(productID) LIKE LOWER(%s)) )"
		print(" - Query String: " + query_string)
		results = execute_query(query_string, conn, select=True, args=(prodID,))
		print(" - Results: " , results)
	
		if results:
			# sql order is: productID, cost, quantity, category, name, description
			self._productID = results[0]
			self._price = results[1]
			self._quantity = results[2]
			self._cat = results[3]
			self._name = results[4]
			self._description = results[5]
		else:
			print(" - No results for ProductID : ", prodID )
		conn.close()

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


# book = Item('Pride and Prejudice', 'Jane Austen', '4394839', 10, '1', '0.1')

# currentBasket = Basket() 
# currentBasket.add_item(book)
