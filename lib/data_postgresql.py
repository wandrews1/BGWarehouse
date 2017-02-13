# Ron Mitsugo Zacharski
#
#   BP1 (best practices 1): Code that is database specific 
#   should be in a separate file
#
from datetime import date
import psycopg2
import psycopg2.extras

from lib.config import *

def connectToPostgres():
  connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD,POSTGRES_HOST)
  print connectionString
  # BP2  Use try-except blocks
  try:
    return psycopg2.connect(connectionString)
  except Exception as e:    # BP2 especially this part where you print the exception
  	print(type(e))
	print(e)
	print("Can't connect to database")
	return None
	



# generic execute statement
# select=True if it is a select statement
#        False if it is an insert
#
def execute_query(query, conn, select=True, args=None):
	print "in execute query"
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	results = None
	try: 
		quer = cur.mogrify(query, args)   # BP6  never use Python concatenation
		                                  # for database queries
		cur.execute(quer)
		if select:
			results = cur.fetchall()
		conn.commit()   # BP5  commit and rollback frequently
	except Exception as e:
		conn.rollback()
		print(type(e))
		print(e)
	cur.close()      # BP3 Dispose of old cursors as soon as possible
	return results

#
#  app specific
#



def newMember(fname, lname, email, dob, pw1):
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "INSERT INTO login (fname, lname, email, dob, pw1) VALUES (%s, %s, %s, %s, %s)"
	execute_query(query_string, conn, select=False,  args=(fname, lname, email, dob, pw1))
	conn.close()
	return 0

def currentRoster():
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "SELECT fname, lname, dob, email FROM login"
	results = execute_query(query_string, conn, select=True)
	conn.close()
	return results


