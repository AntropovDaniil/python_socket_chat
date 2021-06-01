import socket, threading, os, random

host = "localhost"
port = 1234


MSG_SIZE = 1024


COMMANDS = (
	'/clients',
	'/connect',
	'/exit',
	'/help',
)

reciever_list = []

HELP_TEXT = "/clients - get list of active users \n/connect <client> - connect to client\n/exit - disconnect from server\n/help - show help message"

def listen(client_socket, host, port):
	while True:
		message, address = client_socket.recvfrom(MSG_SIZE)
		msg_port = address[-1]
		message = message.decode("utf-8")
		allowed_ports = threading.current_thread().allowed_ports
		if msg_port not in allowed_ports:
			continue

		if not message:
			continue

		if "__" in message:
			command, content = message.split('__')
			if command == "clients":
				for n, client in enumerate(content.split(';'), start = 1):
					print('\r\r' + f'{n}) {client}' + '\n' + 'you: ', end='')
		else:
			peer_name = f'User{msg_port}'
			print('\r\r' + f'{peer_name}: ' + message +'\n' + 'you: ', end='')


def start_listen(target, socket, host, port):
	thread = threading.Thread(target = target, args=(socket, host, port), daemon = True)
	thread.start()
	return thread

def connect(host, port):
	client_port = random.randint(2000,3000)
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.bind((host, client_port))

	thread = start_listen(listen, client_socket, host, port)
	allowed_ports = [port]
	thread.allowed_ports = allowed_ports
	reciever = (host, port)
	client_socket.sendto('__join'.encode("utf-8"), reciever)
	while True:
		message = input(f'::: ')

		command = message.split(' ')[0]
		if command in COMMANDS:
			if message == '/help':
				print(HELP_TEXT)
			
			if message == '/clients':
				client_socket.sendto('__clients'.encode("utf-8"), reciever)

			if message == '/exit':
				reciever_list.remove(reciever)
				peer_port = reciever[-1]
				allowed_ports.remove(peer_port)
				reciever = (host,port)
				print(f"Disconnect from User{peer_port}")

			if message.startswith('/connect'):
				peer = message.split(' ')[-1]
				peer_port = int(peer.replace('User', ''))
				allowed_ports.append(peer_port)
				reciever = (host,peer_port)
				reciever_list.append(reciever)
				print(f"Connect to User{peer_port}")

		else: 
			for addr in reciever_list:
				client_socket.sendto(message.encode("utf-8"), addr)


if __name__ == '__main__':
	os.system('clear')
	connect(host, port)

			
















