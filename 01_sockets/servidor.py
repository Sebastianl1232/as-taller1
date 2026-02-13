# Servidor
import socket
import threading

direccion = ("localhost", 65432)
salidas = {"salir", "exit", "quit"}

def recibir_mensajes(conexion, addr):
    while True:
        datos = conexion.recv(1024)
        if not datos:
            print(f"Cliente {addr} desconectado.")
            break
        texto = datos.decode("utf-8")
        print(f"Cliente: {texto}")
        conexion.sendall(f"Recibido: {texto}".encode("utf-8"))

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(direccion)
        servidor.listen()
        print(f"Servidor escuchando en {direccion[0]}:{direccion[1]}")
        while True:
            conexion, addr = servidor.accept()
            with conexion:
                print(f"Conexión establecida desde {addr}")
                threading.Thread(
                    target=recibir_mensajes,
                    args=(conexion, addr),
                    daemon=True,
                ).start()
                while True:
                    mensaje = input("Servidor: ").strip()
                    if mensaje.lower() in salidas:
                        conexion.close()
                        break
                    if mensaje:
                        conexion.sendall(mensaje.encode("utf-8"))

