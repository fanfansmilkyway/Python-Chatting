import socket
import threading

HEADER = 64
PORT = 8081
SERVER = "127.0.0.1"
# Another way to get the local IP address automatically
#SERVER = socket.gethostbyname(socket.gethostname())
#print(SERVER)
#print(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'ascii'
DISCONNECT_MESSAGE = "!DISCONNECT"

# This dictionary stores every message the user receives
MESSAGES = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr, client_username):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            target = conn.recv(1024).decode(FORMAT)
            MESSAGES[target] = msg
            message_receive = MESSAGES[client_username].encode(FORMAT)
            conn.send(message_receive)
            print(f"[{addr}] {msg} {target}")
        conn.send("[Server has received the message]".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        username = str(conn.recv(1024).decode(FORMAT))
        MESSAGES.update({username:""})
        thread = threading.Thread(target=handle_client, args=(conn, addr, username), name=username)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()