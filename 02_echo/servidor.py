import socket

direccion = ("localhost", 65433)

def manejar_cliente(conexion, addr):
    """Maneja la conexión con un cliente"""
    print(f"Conexión establecida desde {addr}")
    
    try:
        while True:

            datos = conexion.recv(1024)
            
            if not datos:
                print(f"Cliente {addr} desconectado.")
                break
            
            mensaje = datos.decode('utf-8')
            print(f"Recibido de {addr}: {mensaje}")
            
            
            conexion.sendall(datos)
            print(f"Echo enviado a {addr}: {mensaje}")
            
    except Exception as e:
        print(f"Error con cliente {addr}: {e}")
    finally:
        conexion.close()
        print(f"Conexión cerrada con {addr}")

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(direccion)
        servidor.listen()
        print(f"Servidor Echo escuchando en {direccion[0]}:{direccion[1]}")
        print("Esperando conexiones...")
        
        try:
            while True:
                conexion, addr = servidor.accept()
                manejar_cliente(conexion, addr)
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario.")

