import socket
import threading

direccion = ("localhost", 65432)

def recibir_mensajes(cliente):
    while True:
        try:
            datos = cliente.recv(1024)
            if not datos:
                print("Servidor desconectado.")
                break
            print(f"Servidor: {datos.decode('utf-8')}")
        except OSError:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    print(f"Conectando a {direccion[0]}:{direccion[1]}")
    cliente.connect(direccion)

    hilo = threading.Thread(target=recibir_mensajes, args=(cliente,), daemon=True)
    hilo.start()

    while True:
        mensaje = input("Cliente: ").strip()
        if mensaje.lower() in {"salir", "exit", "quit"}:
            cliente.close()
            break
        if mensaje:
            cliente.sendall(mensaje.encode("utf-8"))

