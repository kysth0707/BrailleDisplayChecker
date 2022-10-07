import socket
from threading import Thread, Lock
import time

Value = ""

lock = Lock()

def SetValue(_Value):
	global Value
	lock.acquire()
	Value = _Value
	lock.release()

def SocketTCPForUnity():
	while True:
		HOST = '127.0.0.1'
		PORT = 8000

		print(HOST)
		print(PORT)

		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		server_socket.bind((HOST, PORT))
		print('소켓 생성 완료. 기다리는 중 입니다..')

		server_socket.listen()

		client_socket, address = server_socket.accept()
		print(str(address)+' 에서 연결되었습니다.')

		RunSocket = True

		while RunSocket:
			try:
				client_socket.sendall(Value.encode())
			except:
				RunSocket = False


			time.sleep(0.03)

		client_socket.close()
		server_socket.close()


TempVariable = Thread(target = SocketTCPForUnity, daemon=True)
TempVariable.start()