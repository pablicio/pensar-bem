import socket

servidor = socket.socket()
servidor.bind(("127.0.0.1", 8000))
servidor.listen()

while True:
    cliente, _ = servidor.accept()
    pedido = cliente.recv(1024).decode()
    print(pedido.splitlines()[0])
    cliente.send(b"HTTP/1.1 200 OK\r\n\r\n{}")
    cliente.close()
