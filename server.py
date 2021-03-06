import socket, sqlite3
import hashlib
import pickle, sys
import random

HOST, PORT = '127.0.0.1', 8000

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind((HOST, PORT))
listen_socket.listen(5)

print ('serving HTTP on port ', PORT)

#Dummy data
unames = [("subedir", "berea2015"), ("karkig", "berea2016"), ("scottw", "college201"),("alex", "berea2018"), ("vasant","berea2010"),
 ("peter", "berea2011"), ("ronaldo", "realmadrid"), ("messi", "barcelona"), ("neymar", "psg2017")]

def create_random_str(length):
	number = '0123456789'
	alpha = 'abcdefghijklmnopqrstuvwxyz'
	id = ''
	for i in range(0,length,2):
		id += random.choice(number)
		id += random.choice(alpha)
	return id

def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by db_file
		:param db_file: database file
		:return: Connection object or None
	"""
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return None

def create_table(conn, query):
	""" create a table from the create_table_sql statement
		:param conn: Connection object
		:param create_table_sql: a CREATE TABLE statement
		:return:
	"""
	try:
		c = conn.cursor()
		c.execute(query)

	except Error as e:
		print(e)

def dummy_data(db):
	''' Inputs the dummy data into the db '''
	conn = create_connection(db)
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM usernames")
	row = cursor.fetchone()
	if row == None:
		for uname in unames:
			cursor.execute('insert into usernames (username, password) values (?, ?)', (uname[0], hashFunction(uname[1]),))
		conn.commit()

def add_user(db, username, password):
	''' Adds a registered user into the db '''
	conn = create_connection(db)
	cursor = conn.cursor()
	cursor.execute('insert into usernames (username, password) values (?, ?)', (username, password,))
	conn.commit()

def hashFunction(input):
	''' Used to return a hash value of the password+serverVal to compare with user's value '''
	h = hashlib.md5(input.encode())
	return h.hexdigest()

def main():
	''' Main driver of the program. Creates a db connection, and send and receives data from the user. '''
	db = "users.db"
	conn = create_connection(db)

	sql_query = """ CREATE TABLE IF NOT EXISTS usernames(
			id integer primary key AUTOINCREMENT,
			username nvarchar(40) not null,
			password nvarchar(32) not null
		); """

	if conn is not None:
		create_table(conn, sql_query)
	else:
		print("Error! cannot create the database connection.") 

	listen_socket.listen(1)
	print("Waiting for a connection..")
	dummy_data(db)
	client_connection, client_address = listen_socket.accept()
	tries = 0
	while True:
		request = client_connection.recv(1024)
		request = pickle.loads(request)
		username  = request[1]

		if request[0] == "login":
			random_str = create_random_str(16)
			client_connection.sendall(random_str.encode("ASCII"))
			request = ""

			while True:
				request = client_connection.recv(1024).decode("ASCII")
				break

			c = conn.cursor()
			c.execute('SELECT password FROM usernames WHERE username = ?', (username, ) )
			passw = ""
			account_flag = 0
			try:
				passw = c.fetchone()[0]
			except:
				pass

			account_flag = 1	
			hash_val = passw + random_str
			hash_val = hashFunction(hash_val)	

			if hash_val == request:
				result = pickle.dumps(("You have been authenticated.", 1))
				client_connection.sendall(result)
				client_connection.close()
				break
			else:
				if account_flag == 1:
					result = pickle.dumps(("That account does not exist. Please try again.", 0))
				
				tries += 1
				if tries == 10:
					result = pickle.dumps(("You have exceeded the limit of tries. Please try again later.", 2))
				else:
					result = pickle.dumps(("Sorry, the username and password don't match. Please try again.", 0))
				client_connection.sendall(result)

		elif request[0] == "register":
			add_user(db, request[1], request[2])
			response = "User has been created."
			client_connection.sendall(response.encode("ASCII"))

main()
