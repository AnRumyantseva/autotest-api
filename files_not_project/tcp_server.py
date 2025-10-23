import socket


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 20216)
    server_socket.bind(server_address)

    server_socket.listen(10)
    print("Server started and wait connections ....")

    messages: list[str] = []
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        message = client_socket.recv(1024).decode()
        messages.append(message)
        print(f"Received message: {messages}")
        response = f"Server received : {messages}"

        client_socket.send(response.encode())
        client_socket.close()

if __name__ == '__main__':
    server()
