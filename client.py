'''import socket
SERVER = socket.gethostname()
PORT = 8000
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((SERVER, PORT))

from tkinter import *
expression = ""

def press(num):
    global expression
    expression = expression + str(num)
    equation.set(expression)
    
def trig_and_log(f):
     global expression
     expression=expression+str(f)+'('
     equation.set(expression)
     
def equalpress():
	global expression
	client.send(expression.encode())
	print("Sending Equation")
	answer = client.recv(1024)
	print("Received Response")
	equation.set(str(answer.decode()))
	expression = ""
        
def clear_equation():
    global expression
    expression = ""
    equation.set("")
    
def close():
     client.send('EXIT'.encode())
     client.close()
     gui.destroy()
    
gui = Tk()
gui.configure(background="grey")
gui.title("Simple Calculator")
gui.geometry("270x150")
equation = StringVar()
expression_field = Entry(gui, textvariable=equation)
expression_field.grid(columnspan=4, ipadx=70)
button1 = Button(gui, text=' 1 ', fg='black', bg='#d0efff',command=lambda: press(1), height=1, width=7)
button1.grid(row=2, column=0) 
button2 = Button(gui, text=' 2 ', fg='black', bg='#d0efff',command=lambda: press(2), height=1, width=7)
button2.grid(row=2, column=1)
button3 = Button(gui, text=' 3 ', fg='black', bg='#d0efff',command=lambda: press(3), height=1, width=7)
button3.grid(row=2, column=2) 
button4 = Button(gui, text=' 4 ', fg='black', bg='#d0efff',command=lambda: press(4), height=1, width=7)
button4.grid(row=3, column=0)
button5 = Button(gui, text=' 5 ', fg='black', bg='#d0efff',command=lambda: press(5), height=1, width=7)
button5.grid(row=3, column=1) 
button6 = Button(gui, text=' 6 ', fg='black', bg='#d0efff',command=lambda: press(6), height=1, width=7)
button6.grid(row=3, column=2)
button7 = Button(gui, text=' 7 ', fg='black', bg='#d0efff',command=lambda: press(7), height=1, width=7)
button7.grid(row=4, column=0)
button8 = Button(gui, text=' 8 ', fg='black', bg='#d0efff',command=lambda: press(8), height=1, width=7)
button8.grid(row=4, column=1)
button9 = Button(gui, text=' 9 ', fg='black', bg='#d0efff',command=lambda: press(9), height=1, width=7)
button9.grid(row=4, column=2)
button0 = Button(gui, text=' 0 ', fg='black', bg='#d0efff',command=lambda: press(0), height=1, width=7)
button0.grid(row=5, column=0)
plus = Button(gui, text=' + ', fg='white', bg='#187bcd',command=lambda: press("+"), height=1, width=7)
plus.grid(row=2, column=3)
minus = Button(gui, text=' - ', fg='white', bg='#187bcd',command=lambda: press("-"), height=1, width=7)
minus.grid(row=3, column=3)
multiply = Button(gui, text=' * ', fg='white', bg='#187bcd',command=lambda: press("*"), height=1, width=7)
multiply.grid(row=4, column=3)
divide = Button(gui, text=' / ', fg='white', bg='#187bcd',command=lambda: press("/"), height=1, width=7)
divide.grid(row=5, column=3)
equal = Button(gui, text=' = ', fg='white', bg='#62bd69',command=equalpress, height=1, width=7)
equal.grid(row=5, column=2)
decimal = Button(gui, text='.', fg='black', bg='#d0efff',command=lambda: press('.'), height=1, width=7)
decimal.grid(row=5, column='1') 
Clear= Button(gui, text='Clear', fg='white', bg='#1167b1',command=clear_equation, height=1, width=7)
Clear.grid(row=6, column=0)
exits= Button(gui, text='EXIT', fg='white', bg='#03254c',command=close, height=1, width=7)
exits.grid(row=6, column=3)
answer= Button(gui, text='ANS', fg='white', bg='#1167b1',command=lambda: press('Ans'), height=1, width=7)
answer.grid(row=6, column=1)
power = Button(gui, text=' ^ ', fg='white', bg='#187bcd',command=lambda: press("^"), height=1, width=7)
power.grid(row=7, column=0)

log10 = Button(gui, text=' log ', fg='white', bg='#187bcd',command=lambda: trig_and_log("log10"), height=1, width=7)
log10.grid(row=7, column=1)

log = Button(gui, text=' ln ', fg='white', bg='#187bcd',command=lambda: trig_and_log("log"), height=1, width=7)
log.grid(row=7, column=2)

sin = Button(gui, text=' sin ', fg='white', bg='#187bcd',command=lambda: trig_and_log("sin"), height=1, width=7)
sin.grid(row=7, column=3)

cos = Button(gui, text=' cos ', fg='white', bg='#187bcd',command=lambda: trig_and_log("cos"), height=1, width=7)
cos.grid(row=8, column=0)

tan = Button(gui, text=' tan ', fg='white', bg='#187bcd',command=lambda: trig_and_log("tan"), height=1, width=7)
tan.grid(row=8, column=3)

gui.mainloop()

'''
import socket
from _thread import *
from math import *

HOST = ""
PORT = 8000
ThreadCount = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(('', PORT))
except socket.error as e:
    print(str(e))

server.listen(5)
print("Server started")
print("Waiting for client request..")


def multi_threaded_client(clientsocket, addr):
    global ThreadCount
    result = '0'
    msg = ''
    while True:
        try:
            # Set timeout of 10 seconds
            clientsocket.settimeout(10)

            data = clientsocket.recv(1024)
            if not data:
                # No data received within 10 seconds, close the connection
                break

            msg = data.decode()
            print("Equation is received")
            if msg == 'EXIT':
                ThreadCount -= 1
                break
            try:
                msg = msg.replace("Ans", result)
                msg = msg.replace("^", "**")
                msg = msg.replace("ln", "log")
                msg = msg.replace("log", "log10")
                exp = compile(msg, "<string>", "eval")
                result = str(eval(exp))
                print(addr + ':\tRESULT=' + result)
                clientsocket.send(result.encode())
            except Exception as e:
                err_type = type(e).name
                err_msg = str(e)
                err = "Error: {}".format(err_type)
                print(addr + ':\tERROR=' + err)
                clientsocket.send(err.encode())
        except socket.timeout:
            # Timeout occurred, close the connection
            break
    clientsocket.close()


while True:
    Client, address = server.accept()
    print('Connected to: ' + str(address))
    start_new_thread(multi_threaded_client, (Client, address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
