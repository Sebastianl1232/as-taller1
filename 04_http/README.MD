# 4. Servidor HTTP Básico

## Descripción

Este ejercicio implementa un **servidor HTTP básico desde cero** usando sockets en Python, sin depender de librerías como `Flask` o `Django`. El objetivo es entender cómo funciona el protocolo HTTP a nivel fundamental.

## Conceptos Clave

### Protocolo HTTP
- **HTTP (Hypertext Transfer Protocol):** Protocolo de aplicación que define cómo los clientes (navegadores) y servidores intercambian información.
- **Solicitud HTTP:** Mensaje enviado por el cliente al servidor con la siguiente estructura:
  ```
  GET /ruta HTTP/1.1
  Host: localhost:8080
  User-Agent: ...
  
  ```
- **Respuesta HTTP:** Mensaje enviado por el servidor con la siguiente estructura:
  ```
  HTTP/1.1 200 OK
  Content-Type: text/html
  Content-Length: 1234
  
  <contenido HTML>
  ```

### Códigos de Estado HTTP
- **200 OK:** La solicitud fue exitosa
- **404 Not Found:** La ruta solicitada no existe
- **500 Internal Server Error:** Error del servidor

## Funcionalidades

### Servidor (`servidor.py`)
- Escucha en `localhost:8080`
- Maneja múltiples clientes simultáneamente usando **threading**
- Genera páginas HTML dinámicamente
- Maneja diferentes rutas:
  - `/` - Página de inicio
  - `/info` - Información del servidor
  - Cualquier otra ruta - Respuesta 404

### Cliente (`cliente.py`)
- Interfaz interactiva para hacer solicitudes HTTP
- Parsea respuestas HTTP
- Muestra status, headers y contenido

## Instrucciones de Uso

### 1. Iniciar el Servidor

Abre una terminal en la carpeta `04_http` y ejecuta:

```bash
python servidor.py
```

Deberías ver:
```
Servidor HTTP iniciado en http://localhost:8080
Presiona Ctrl+C para detener el servidor...
```

### 2. Usar el Cliente

En **otra terminal** (en la misma carpeta), ejecuta:

```bash
python cliente.py
```

Se abrirá un menú interactivo donde puedes:
1. **Ir a inicio (/)** - Ver la página principal
2. **Ver información del servidor (/info)** - Datos del servidor
3. **Probar página no encontrada (/desconocida)** - Ejemplo de error 404
4. **Solicitud personalizada** - Ingresa tu propia ruta
5. **Salir** - Cerrar el cliente

### 3. Alternativa: Usar un Navegador Web

También puedes usar tu navegador favorito:
1. Asegúrate que el servidor está ejecutándose
2. Abre: `http://localhost:8080`
3. Navega por los enlaces disponibles

## Estructura del Código

### Clase `ServidorHTTP`

**Métodos principales:**
- `__init__()` - Crea el socket del servidor
- `parsear_solicitud()` - Extrae método, ruta y versión HTTP
- `construir_respuesta()` - Crea una respuesta HTTP válida con headers
- `manejar_cliente()` - Procesa cada conexión de cliente en un hilo separado
- `iniciar()` - Inicia la escucha de conexiones

**Métodos auxiliares:**
- `generar_pagina_inicio()` - HTML para la página raíz
- `generar_pagina_info()` - HTML con información del servidor

### Clase `ClienteHTTP`

**Métodos principales:**
- `solicitar()` - Realiza una solicitud HTTP GET
- `parsear_respuesta()` - Extrae status, headers y body
- `mostrar_respuesta()` - Imprime la respuesta de forma legible

## Conceptos Aprendidos

1. **Protocolo TCP:** El servidor escucha y acepta conexiones
2. **Protocolo HTTP:** Formato de solicitudes y respuestas
3. **Parsing:** Extracción de información de mensajes de texto
4. **Threading:** Manejo de múltiples clientes simultáneamente
5. **Sockets:** Puntos de conexión en la red

## Ejemplo de Sesión

```
Conectando a localhost:8080...
Conexión establecida.

Enviando solicitud:
--------------------------------------------------
GET / HTTP/1.1
Host: localhost:8080
User-Agent: ClienteHTTP/1.0
Connection: close

--------------------------------------------------

Respuesta recibida:
==================================================
Status: 200 OK

Headers:
--------------------------------------------------
Date: Mon, 17 Feb 2026 14:30:45 GMT
Server: ServidorHTTP/1.0
Content-Length: 523
Content-Type: text/html; charset=utf-8
Connection: close

Body:
--------------------------------------------------
<!DOCTYPE html>
<html>
...
</html>
==================================================
```

## Mejoras Sugeridas

1. Agregar soporte para POST requests
2. Servir archivos estáticos (CSS, imágenes)
3. Agregar logging configurable
4. Implementar manejo de errores más robusto
5. Agregar soporte para parámetros GET en la URL
6. Implementar caché de respuestas
7. Usar `async`/`await` en lugar de threading

## Recursos

- [RFC 7231 - HTTP/1.1 Semantics](https://tools.ietf.org/html/rfc7231)
- [HTTP Status Codes](https://httpwg.org/specs/rfc7231.html#status.codes)
- [Python socket documentation](https://docs.python.org/3/library/socket.html)
