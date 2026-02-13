import socket

direccion = ("localhost", 65432)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    print(f"Conectando a {direccion[0]}:{direccion[1]}")
    cliente.connect(direccion)
    cliente.sendall(b"Hola, servidor!")
    respuesta = cliente.recv(1024).decode()
    print(f"Respuesta: {respuesta}")

