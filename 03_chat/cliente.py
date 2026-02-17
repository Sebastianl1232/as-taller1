import socket
import threading
import sys

direccion = ("localhost", 65434)

def recibir_mensajes(cliente):
    """Recibe y muestra mensajes del servidor"""
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(f"\r{mensaje}", end="")
            print("Tú: ", end="", flush=True)
        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    try:
        cliente.connect(direccion)
        
        # Recibir solicitud de nombre y enviarlo
        solicitud = cliente.recv(1024).decode('utf-8')
        nombre = input(solicitud)
        cliente.sendall(nombre.encode('utf-8'))
        
        # Iniciar hilo para recibir mensajes
        hilo = threading.Thread(target=recibir_mensajes, args=(cliente,), daemon=True)
        hilo.start()
        
        # Enviar mensajes
        while True:
            mensaje = input("Tú: ").strip()
            if mensaje.lower() in {"salir", "exit", "quit"}:
                cliente.sendall(mensaje.encode('utf-8'))
                break
            if mensaje:
                cliente.sendall(mensaje.encode('utf-8'))
                
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor")
    except KeyboardInterrupt:
        print("\nDesconectado")

