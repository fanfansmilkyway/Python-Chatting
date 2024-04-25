import socket

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
client.connect(ADDR)

# Ask username
username = str(input("Input your username: ")).encode(FORMAT)
client.send(username)

def send(msg:str, target:str):
    message = msg.encode(FORMAT)
    # Target is the user whom you want to send to
    target = target.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    client.send(target)
    print(client.recv(2048).decode(FORMAT))
    #print(client.recv(2048).decode(FORMAT))

while True:
    message = str(input("Message: "))
    target = str(input("Target: "))
    send(message, target)