import socket

host = "localhost"
port = 1234

MSG_SIZE = 1024


def listen(host, port):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	server_socket.bind((host, port))
	print(f"Server started at port: {port}")

	clients = []

	while True:
		message, address = server_socket.recvfrom(MSG_SIZE)

		if address not in clients:
			clients.append(address)

		if not message:
			continue

		client_id = address[1]
		message = message.decode("utf-8")
		if message == "__join":
			print(f"User{client_id} joined chat")
			continue

		msg_template = "{}__{}"
		if message == "__clients":
			print(f"User{client_id} requested client list")
			active_clients = [f'User{m[1]}' for m in clients if m!=address]
			client_msg = ';'.join(active_clients)
			server_socket.sendto(msg_template.format('clients', client_msg).encode("utf-8"), address)


if __name__ == '__main__':
	listen(host, port)





	


	
