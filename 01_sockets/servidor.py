# Servidor
import socket
import threading

direccion = ("localhost", 65432)

def recibir_mensajes(conexion, addr):
    while True:
        try:
            datos = conexion.recv(1024)
            if not datos:
                print(f"Cliente {addr} desconectado.")
                break
            print(f"Cliente: {datos.decode('utf-8')}")
        except OSError:
            break

def manejar_cliente(conexion, addr):
    print(f"Conexión establecida desde {addr}")
    hilo = threading.Thread(target=recibir_mensajes, args=(conexion, addr), daemon=True)
    hilo.start()
    while True:
        mensaje = input("Servidor: ").strip()
        if mensaje.lower() in {"salir", "exit", "quit"}:
            conexion.close()
            break
        if mensaje:
            conexion.sendall(mensaje.encode("utf-8"))

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(direccion)
        servidor.listen()
        print(f"Servidor escuchando en {direccion[0]}:{direccion[1]}")
        while True:
            try:
                conexion, addr = servidor.accept()
                with conexion:
                    manejar_cliente(conexion, addr)
            except Exception as e:
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    iniciar_servidor()

