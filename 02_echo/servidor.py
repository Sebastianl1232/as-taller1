import socket

direccion = ("localhost", 65433)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(direccion)
    servidor.listen()
    print(f"Servidor Echo escuchando en {direccion[0]}:{direccion[1]}")
    
    while True:
        conexion, addr = servidor.accept()
        print(f"Conexión desde {addr}")
        
        with conexion:
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                print(f"Recibido: {datos.decode('utf-8')}")
                conexion.sendall(datos)

