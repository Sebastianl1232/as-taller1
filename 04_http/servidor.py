import socket
import threading
import os
from datetime import datetime

class ServidorHTTP:
    def __init__(self, host='localhost', puerto=8080):
        
        self.host = host
        self.puerto = puerto
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def parsear_solicitud(self, datos):
        
        lineas = datos.split('\n')
        if lineas:
            primera_linea = lineas[0].strip().split()
            if len(primera_linea) >= 3:
                return primera_linea[0], primera_linea[1], primera_linea[2]
        return 'GET', '/', 'HTTP/1.1'
    
    def construir_respuesta(self, codigo, mensaje, contenido):
        
        fecha = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        longitud = len(contenido.encode())
        
        respuesta = (
            f"HTTP/1.1 {codigo} {mensaje}\r\n"
            f"Date: {fecha}\r\n"
            f"Server: ServidorHTTP/1.0\r\n"
            f"Content-Length: {longitud}\r\n"
            f"Content-Type: text/html; charset=utf-8\r\n"
            f"Connection: close\r\n"
            f"\r\n"
            f"{contenido}"
        )
        return respuesta.encode()
    
    def generar_pagina_inicio(self):
        """Genera la página HTML de inicio."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Servidor HTTP - Taller 1</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }
                h1 { color: #333; }
                .container { background-color: white; padding: 20px; border-radius: 5px; }
                a { color: #0066cc; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>¡Bienvenido al Servidor HTTP Básico!</h1>
                <p>Este es un servidor HTTP implementado desde cero usando sockets en Python.</p>
                <h2>Rutas disponibles:</h2>
                <ul>
                    <li><a href="/">/</a> - Página de inicio</li>
                    <li><a href="/info">/info</a> - Información del servidor</li>
                    <li><a href="/desconocida">/desconocida</a> - Ejemplo de página no encontrada</li>
                </ul>
            </div>
        </body>
        </html>
        """
    
    def generar_pagina_info(self):
        """Genera la página de información."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Información del Servidor</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }}
                h1 {{ color: #333; }}
                .container {{ background-color: white; padding: 20px; border-radius: 5px; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #0066cc; color: white; }}
                a {{ color: #0066cc; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Información del Servidor HTTP</h1>
                <table>
                    <tr>
                        <th>Dato</th>
                        <th>Valor</th>
                    </tr>
                    <tr>
                        <td>Host</td>
                        <td>{self.host}</td>
                    </tr>
                    <tr>
                        <td>Puerto</td>
                        <td>{self.puerto}</td>
                    </tr>
                    <tr>
                        <td>Hora del Servidor</td>
                        <td>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</td>
                    </tr>
                </table>
                <p><a href="/">Volver a inicio</a></p>
            </div>
        </body>
        </html>
        """
    
    def manejar_cliente(self, socket_cliente, direccion):
        
        try:
            datos = socket_cliente.recv(4096).decode('utf-8', errors='ignore')
            
            if datos:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Solicitud de {direccion[0]}:{direccion[1]}")
                print(f"----------------\n{datos.split(chr(10))[0]}")
                
                metodo, ruta, version = self.parsear_solicitud(datos)
                
                if ruta == '/' or ruta == '/index.html':
                    contenido = self.generar_pagina_inicio()
                    respuesta = self.construir_respuesta(200, 'OK', contenido)
                    
                elif ruta == '/info':
                    contenido = self.generar_pagina_info()
                    respuesta = self.construir_respuesta(200, 'OK', contenido)
                    
                else:
                    contenido = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>404 - No Encontrado</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }}
                            h1 {{ color: #d32f2f; }}
                            .container {{ background-color: white; padding: 20px; border-radius: 5px; }}
                            a {{ color: #0066cc; text-decoration: none; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>404 - Página No Encontrada</h1>
                            <p>La ruta "{ruta}" no existe en este servidor.</p>
                            <p><a href="/">Volver a inicio</a></p>
                        </div>
                    </body>
                    </html>
                    """
                    respuesta = self.construir_respuesta(404, 'Not Found', contenido)
                
                # Enviar respuesta
                socket_cliente.send(respuesta)
                print(f"Respuesta enviada (Status: {respuesta.decode('utf-8', errors='ignore').split()[1]})")
                
        except Exception as e:
            print(f"Error manejando cliente {direccion}: {e}")
        finally:
            socket_cliente.close()
    
    def iniciar(self):
        """Inicia el servidor y lo mantiene escuchando conexiones."""
        try:
            self.socket_servidor.bind((self.host, self.puerto))
            self.socket_servidor.listen(5)
            print(f"Servidor HTTP iniciado en http://{self.host}:{self.puerto}")
            print("Presiona Ctrl+C para detener el servidor...\n")
            
            while True:
                socket_cliente, direccion = self.socket_servidor.accept()

                hilo_cliente = threading.Thread(
                    target=self.manejar_cliente,
                    args=(socket_cliente, direccion)
                )
                hilo_cliente.daemon = True
                hilo_cliente.start()
                
        except KeyboardInterrupt:
            print("\nServidor detenido.")
        except Exception as e:
            print(f"Error en el servidor: {e}")
        finally:
            self.socket_servidor.close()

if __name__ == '__main__':
    servidor = ServidorHTTP('localhost', 8080)
    servidor.iniciar()

