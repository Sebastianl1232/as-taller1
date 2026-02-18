import socket
from urllib.parse import urlparse

class ClienteHTTP:
    def __init__(self):
        """Inicializa el cliente HTTP."""
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def solicitar(self, url, host='localhost', puerto=8080):
        """
        Realiza una solicitud HTTP GET a un servidor.
        
        Args:
            url (str): La ruta a solicitar (ej: '/', '/info')
            host (str): Dirección del servidor (por defecto localhost)
            puerto (int): Puerto del servidor (por defecto 8080)
            
        Returns:
            dict: Diccionario con 'status', 'headers' y 'body'
        """
        try:
            print(f"Conectando a {host}:{puerto}...")
            self.socket_cliente.connect((host, puerto))
            print("Conexión establecida.\n")
            
            solicitud = (
                f"GET {url} HTTP/1.1\r\n"
                f"Host: {host}:{puerto}\r\n"
                f"User-Agent: ClienteHTTP/1.0\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )
            
            print("Enviando solicitud:")
            print("-" * 50)
            print(solicitud)
            print("-" * 50 + "\n")
            
            self.socket_cliente.send(solicitud.encode())
            
            respuesta_completa = b""
            while True:
                datos = self.socket_cliente.recv(4096)
                if not datos:
                    break
                respuesta_completa += datos
            
            respuesta_texto = respuesta_completa.decode('utf-8', errors='ignore')
            return self.parsear_respuesta(respuesta_texto)
            
        except ConnectionRefusedError:
            print(f"Error: No se puede conectar a {host}:{puerto}")
            print("Asegúrate de que el servidor está ejecutándose.")
            return None
        except Exception as e:
            print(f"Error durante la solicitud: {e}")
            return None
        finally:
            self.socket_cliente.close()
    
    def parsear_respuesta(self, respuesta):
        """
        Parsea la respuesta HTTP.
        
        Args:
            respuesta (str): La respuesta HTTP completa
            
        Returns:
            dict: Diccionario con 'status', 'headers' y 'body'
        """
        partes = respuesta.split('\r\n\r\n', 1)
        headers_texto = partes[0]
        body = partes[1] if len(partes) > 1 else ""
        
        lineas_headers = headers_texto.split('\r\n')
        linea_estado = lineas_headers[0]
        
        estado_partes = linea_estado.split(' ', 2)
        codigo = estado_partes[1] if len(estado_partes) > 1 else "???"
        mensaje = estado_partes[2] if len(estado_partes) > 2 else ""
        
        headers = {}
        for linea in lineas_headers[1:]:
            if ':' in linea:
                clave, valor = linea.split(':', 1)
                headers[clave.strip()] = valor.strip()
        
        return {
            'status': f"{codigo} {mensaje}",
            'codigo': codigo,
            'headers': headers,
            'body': body
        }
    
    def mostrar_respuesta(self, respuesta):
        """
        Muestra la respuesta HTTP de forma legible.
        
        Args:
            respuesta (dict): Respuesta parseada
        """
        if respuesta is None:
            return
        
        print("\nRespuesta recibida:")
        print("=" * 50)
        print(f"Status: {respuesta['status']}\n")
        
        print("Headers:")
        print("-" * 50)
        for clave, valor in respuesta['headers'].items():
            print(f"{clave}: {valor}")
        
        print("\nBody:")
        print("-" * 50)
        print(respuesta['body'])
        print("=" * 50 + "\n")

def menu_interactivo():
    """Menú interactivo para hacer solicitudes HTTP."""
    cliente = ClienteHTTP()
    
    print("=" * 50)
    print("Cliente HTTP Interactivo")
    print("=" * 50)
    print("Rutas disponibles: /, /info, /desconocida")
    print("=" * 50 + "\n")
    
    while True:
        print("\nOpciones:")
        print("1. Ir a inicio (/)")
        print("2. Ver información del servidor (/info)")
        print("3. Probar página no encontrada (/desconocida)")
        print("4. Solicitud personalizada")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == '1':
            respuesta = cliente.solicitar('/')
            if respuesta:
                cliente.mostrar_respuesta(respuesta)
        elif opcion == '2':
            respuesta = cliente.solicitar('/info')
            if respuesta:
                cliente.mostrar_respuesta(respuesta)
        elif opcion == '3':
            respuesta = cliente.solicitar('/desconocida')
            if respuesta:
                cliente.mostrar_respuesta(respuesta)
        elif opcion == '4':
            ruta = input("Ingresa la ruta (ej: /): ").strip()
            if ruta:
                respuesta = cliente.solicitar(ruta)
                if respuesta:
                    cliente.mostrar_respuesta(respuesta)
        elif opcion == '5':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")
        
        cliente = ClienteHTTP()

if __name__ == '__main__':
    menu_interactivo()
