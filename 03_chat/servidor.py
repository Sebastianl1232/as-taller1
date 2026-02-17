import socket
import threading

direccion = ("localhost", 65434)
clientes = {}  # {conexion: nombre}
lock = threading.Lock()

def broadcast(mensaje, remitente=None):
    """Envía un mensaje a todos los clientes excepto al remitente"""
    with lock:
        for conexion in list(clientes.keys()):
            if conexion != remitente:
                try:
                    conexion.sendall(mensaje.encode('utf-8'))
                except:
                    pass

def manejar_cliente(conexion, addr):
    """Maneja la comunicación con un cliente"""
    nombre = None
    try:
        # Recibir nombre del cliente
        conexion.sendall("Ingresa tu nombre: ".encode('utf-8'))
        nombre = conexion.recv(1024).decode('utf-8').strip()
        
        with lock:
            clientes[conexion] = nombre
        
        print(f"{nombre} ({addr}) se ha conectado")
        broadcast(f">>> {nombre} se ha unido al chat\n", conexion)
        conexion.sendall(f"Bienvenido al chat, {nombre}!\n".encode('utf-8'))
        
        # Recibir mensajes del cliente
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            
            mensaje = datos.decode('utf-8').strip()
            if mensaje.lower() in {"salir", "exit", "quit"}:
                break
            
            print(f"{nombre}: {mensaje}")
            broadcast(f"{nombre}: {mensaje}\n", conexion)
            
    except Exception as e:
        print(f"Error con {nombre or addr}: {e}")
    finally:
        with lock:
            if conexion in clientes:
                nombre = clientes.pop(conexion)
        conexion.close()
        print(f"{nombre} ({addr}) se ha desconectado")
        broadcast(f"<<< {nombre} ha salido del chat\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(direccion)
    servidor.listen()
    print(f"Servidor de chat escuchando en {direccion[0]}:{direccion[1]}")
    print("Esperando conexiones...\n")
    
    try:
        while True:
            conexion, addr = servidor.accept()
            threading.Thread(target=manejar_cliente, args=(conexion, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nServidor detenido")


