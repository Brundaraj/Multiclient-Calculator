import socket
from _thread import *

HOST = socket.gethostname()
PORT = 8000
ThreadCount=0

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	server.bind(('', PORT))
except socket.error as e:
	print(str(e))

server.listen(5)
print("Server started")
print("Waiting for client request..")

def multi_threaded_client(clientsocket,addr):
	global ThreadCount
	result='0'
	msg=''
	while True:
		data = clientsocket.recv(1024)
		msg = data.decode()
		print("Equation is received")
		if(msg=='EXIT'):
			ThreadCount-=1
			break
		try:
			msg=msg.replace("Ans",result)
			result = str(eval(msg))
			clientsocket.send(result.encode())
		except Exception as e:
			err_type = type(e)._name_
			err_msg = str(e)
			err = "Error: {}".format(err_type)
			clientsocket.send(err.encode())
	clientsocket.close()

while True:
    Client, address = server.accept()
    print('Connected to: ' + str(address))
    start_new_thread(multi_threaded_client, (Client,address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
