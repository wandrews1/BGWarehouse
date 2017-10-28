# Billy Andrews
from datetime import date
import psycopg2
import psycopg2.extras

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

	
	


def newMember(fname, lname, email, dob, zipcode, pw1, level):
	print (" - in newMember()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "INSERT INTO login (fname, lname, email, dob, zipcode, pw1, userLevel) VALUES (%s, %s, %s, %s, %s, crypt(%s, gen_salt('bf')), %s)" 
	execute_query(query_string, conn, select=False,  args=(fname, lname, email, dob, zipcode, pw1, userLevel))
	conn.close()
	return 0


def currentRoster():
	print (" - in currentRoster()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT fname, lname, dob, email, zipcode FROM login"
	results = execute_query(query_string, conn, select=True)
	conn.close()
	return results

	
	
# def superSearch(zipcode, cat, search):
# 	print (" - in superSearch()")
# 	conn = connectToPostgres()
# 	if conn == None:
# 		return None
# 	print (" - connected to database")
# 	if cat in ['name','category','subcategory','address','city','state','country','phone']:
# 		query_string = "SELECT * FROM items WHERE zipcode = %s AND " + cat + " = %s"
# 	print(" - Query String: " + query_string)
# 	results2 = execute_query(query_string, conn, select=True, args=(zipcode, search))
# 	print(" - Results: " , results2)
# 	if results2:
# 		return results2
# 	else:
# 		if zipcode == '':
# 			if cat in ['name','category','subcategory','address','city','state','country','phone']:
# 				query_string = "SELECT * FROM items WHERE " + cat + " = %s"
# 				results2 = execute_query(query_string, conn, select=True, args=(search,))
# 		else:
# 			query_string = "SELECT * FROM items WHERE zipcode = %s"
# 			results2 = execute_query(query_string, conn, select=True, args=(zipcode,))
# 			if results2:
# 				return " - Invalid Category"
# 			else:
# 				return " - No data for your zipcode"
# 	conn.close()
# 	return results2
	
	
def superSearch(search):
	print (" - in superSearch()")
	conn = connectToPostgres()
	if conn == None:
		return None
	print (" - connected to database")

	query_string = "SELECT * FROM items WHERE item LIKE %s"
	print(" - Query String: " + query_string)
	results2 = execute_query(query_string, conn, select=True, args=('%' + search + '%',))
	print(" - Results: " , results2)
	if results2:
		return results2
	else:
		return " - No luck finding your search term."
	conn.close()
	return results2
	
	
# def superSearch(search):
# 	print (" - in superSearch()")
# 	conn = connectToPostgres()
# 	if conn == None:
# 		return None
# 	print (" - connected to database")
	
# 	query_string = "SELECT * FROM items WHERE " + cat + " = %s"
	
# 	print(" - Query String: " + query_string)
	
# 	results2 = execute_query(query_string, conn, select=True, args=(search,))
	
# 	print(" - Results: " , results2)
	
# 	if results2:
# 		return results2
# 	# else:
# 	# 	if zipcode == '':
# 	# 		if cat in ['productID','cost','quantity','category','name','description']:
# 	# 			query_string = "SELECT * FROM items WHERE " + cat + " = %s"
# 	# 			results2 = execute_query(query_string, conn, select=True, args=(search,))
# 	# 	else:
# 	# 		query_string = "SELECT * FROM items WHERE zipcode = %s"
# 	# 		results2 = execute_query(query_string, conn, select=True, args=(zipcode,))
# 	# 		if results2:
# 	# 			return " - Invalid Category"
# 	# 		else:
# 	# 			return " - No data for your zipcode"
# 	conn.close()
# 	return results2



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
	
def getAddress(email,pw1):
	print (" - in getAddress()")
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT address FROM login WHERE email = %s AND pw1 = crypt(%s,pw1)"
	results = execute_query(query_string, conn, select=True, args=(email, pw1))
	conn.close()
	return results[0][0]