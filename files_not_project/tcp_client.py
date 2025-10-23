import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 20216)
client_socket.connect(server_address)
message = "Hello, server"
client_socket.send(message.encode())
response = client_socket.recv(1024).decode()
print(f"Answer from server: {response}")
client_socket.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
message2 = "How are you?"
client_socket.send(message2.encode())
response2 = client_socket.recv(1024).decode()
print(f"Answer from server: {response2}")
client_socket.close()