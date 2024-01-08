import socket
import threading

userSockets = {}
groups = {}
usernameAndPasswords = {}

def validateUsername(uname1):
    if uname1 == 'panda':
        return False
    for u in userSockets:
        if u == uname1:
            return False
    return True


def handle_client(my_client_socket, my_addr):

    print(f"Accepted connection from {my_addr}")
    welcome_message = "Welcome to the server!"
    my_client_socket.send(welcome_message.encode())
    username = 'panda'
    password = '1234'
    while True:
        data = my_client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        datasp = data.split(':')
        # b: hello
        if datasp[0] == 'b':
            broadcast_data = f"Client {username}: {datasp[1]}"
            print(broadcast_data)
            for c in clients:
                if c != my_client_socket:
                    c.send(broadcast_data.encode())
        elif datasp[0] == 'u':
            myusername = datasp[1]
            mypassword = datasp[2]
            if validateUsername(myusername):
                username = datasp[1]
                password = mypassword
                usernameAndPasswords[username] = hash(password)
                my_client_socket.send('username changed or added'.encode('utf-8'))
                userSockets[username] = my_client_socket
            else:
                my_client_socket.send('username repeated or panda'.encode('utf-8'))
        elif datasp[0] == 's':
            receiver = datasp[1]
            text = datasp[2]
            for u in userSockets:
                if u == receiver:
                    s = userSockets[u]
                    message = username + " whispers: " + text
                    s.send(message.encode('utf-8'))
        elif datasp[0] == 'cg':  # create group
            groupName = datasp[1]
            groups[groupName] = []
            for i in range(2, len(datasp)):
                groups[groupName].append(datasp[i])
        elif datasp[0] == 'sg':  # send group
            groupName = datasp[1]
            text = datasp[2]
            for member in groups[groupName]:
                s = userSockets[member]
                if isinstance(s, socket.socket):
                    s.send(text.encode('utf-8'))


    clients.remove(my_client_socket)
    my_client_socket.close()
    print(f"Connection from {my_addr} closed.")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1235

server_socket.bind((host, port))
server_socket.listen(10)
print(f"Server listening on {host}:{port}...")
clients = []

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
