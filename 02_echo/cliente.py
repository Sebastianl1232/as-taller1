import socket

direccion = ("localhost", 65433)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect(direccion)
    print("Conectado. Escribe 'salir' para terminar.\n")
    
    while True:
        mensaje = input("Tú: ").strip()
        if mensaje.lower() in {"salir", "exit", "quit"}:
            break
        if mensaje:
            cliente.sendall(mensaje.encode('utf-8'))
            echo = cliente.recv(1024).decode('utf-8')
            print(f"Echo: {echo}\n")

