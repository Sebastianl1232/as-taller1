import socket

direccion = ("localhost", 65433)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        print(f"Conectando al servidor echo en {direccion[0]}:{direccion[1]}")
        cliente.connect(direccion)
        print("Conectado. Escribe mensajes para enviar al servidor.")
        print("Escribe 'salir', 'exit' o 'quit' para terminar.\n")
        
        try:
            while True:
                mensaje = input("Tú: ").strip()
                
                if mensaje.lower() in {"salir", "exit", "quit"}:
                    print("Cerrando conexión...")
                    break
        
                if mensaje:
                    cliente.sendall(mensaje.encode('utf-8'))
                    
                    datos = cliente.recv(1024)
                    respuesta = datos.decode('utf-8')
                    print(f"Echo del servidor: {respuesta}\n")
                    
        except KeyboardInterrupt:
            print("\nConexión interrumpida por el usuario.")
        except Exception as e:
            print(f"Error: {e}")

