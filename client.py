import socket
import threading


def receive_messages(my_client_socket):
    while True:
        try:
            data = my_client_socket.recv(1024)
            if not data:
                break

            print(data.decode())
        except:
            break


def send_messages(client_socket_client):
    while True:
        message = input('>  ')
        client_socket_client.send(message.encode())


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1235
client_socket.connect((host, port))
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
send_thread = threading.Thread(target=send_messages, args=(client_socket,))
receive_thread.start()
send_thread.start()
