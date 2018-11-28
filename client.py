'''
 The client is receving a random hashed value from the server & combining it with the password the user enters.
 Then, that is being sent to the server. If it matches the value that the server gets, then the authentication is valid.
'''

import socket, sys, time
from Crypto.Cipher import AES

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 8000)


def hashFunction(input):
	''' Used to return a hash value of the password & the password+serverVal '''
	return hash(input)

def getHashVal():
	message = socks.recv(1024)  
	message = message.decode('ASCII')
	return message

def sendData(data):
	sock.send(data + "\n")
	return

def main():
	server.connect(server_address)
	#Maybe make a login/registration part?

	uname = raw_input("Enter your username")
	passw = raw_input("Enter your password")
	serverVal = getHashVal()

	finalHashVal = hashFunction(serverVal + passw)

	send((uname,finalHashVal))

