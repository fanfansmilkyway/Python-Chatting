import socket
import curses
import time

# Colors
NORMAL = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
YELLOW = '\033[93m'
PINK = '\033[95m'

HEADER = 64
PORT = 8081
FORMAT = 'ascii'
DISCONNECT_MESSAGE = "!DISCONNECT"
# Whatever IP address you found from running ifconfig in terminal.
# SERVER = ""
SERVER = "127.0.0.1"

ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Officially connecting to the server.
try:
    client.connect(ADDR)
except:
    print(RED, "[ERROR] Cannot connect to the server.\nPlease check the server status or your network.\nIf you still can't connect to the server, please contact us with fanfansmilkyway@gmail.com")
    exit()
else:
    print(GREEN, "[SERVER CONNECTED] Successfully connect to the server!")
    time.sleep(0.5)

# Ask username
username = str(input(NORMAL + "Input your username: ")).encode(FORMAT)
client.send(username)

def receive(target: str):
    pass

def send_msg(message: str, target: str, action="SEND"):
    action = action.encode(FORMAT)
    message = message.encode(FORMAT)
    # Target is the user whom you want to send to
    target = target.encode(FORMAT)
    client.send(action)
    time.sleep(0.15)
    client.send(message)
    time.sleep(0.15)
    client.send(target)

def receive_msg(action="RECEIVE"):
    action = action.encode(FORMAT)
    client.send(action)
    NumberOfMessage = int(client.recv(256).decode(FORMAT)) # The number of messages
    print(NumberOfMessage)
    if NumberOfMessage == 0:
        print(YELLOW + "No message receive.")
    else:
        for i in range(NumberOfMessage):
            message = str(client.recv(2048).decode(FORMAT))
            message_from = str(client.recv(2048).decode(FORMAT))
            print(message_from + " >> " + message)

try:
    while True:
        message = str(input(NORMAL + "Message: "))
        target = str(input(NORMAL + "Target: "))
        send_msg(message=message, target=target)
        time.sleep(0.5)
        receive_msg()
except:
    send_msg(message=DISCONNECT_MESSAGE, target="!SERVER")