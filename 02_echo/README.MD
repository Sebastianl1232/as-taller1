# 02_echo - Servidor Echo

## Descripción

Implementación del patrón Echo donde el servidor devuelve exactamente lo que recibe del cliente.

## Archivos

- `servidor.py`: Escucha conexiones y devuelve de cada mensaje recibido.
- `cliente.py`: Se conecta al servidor, envía mensajes y recibe el echo.

## Características

- Servidor que devuelve exactamente lo que recibe 
- Comunicación TCP confiable
- Manejo de desconexiones
- Comando de salida: `salir`, `exit` o `quit`
- Conexión TCP con `localhost:65433`

## Uso

```bash
# Terminal 1 - Servidor
python 02_echo/servidor.py

# Terminal 2 - Cliente
python 02_echo/cliente.py
```

## Ejemplo de interacción

```text
Servidor Echo escuchando en localhost:65433
Esperando conexiones...
Conexión establecida desde ('127.0.0.1', 53422)
Recibido de ('127.0.0.1', 53422): Hola mundo
Echo enviado a ('127.0.0.1', 53422): Hola mundo
```

Cliente:
```text
Conectando al servidor echo en localhost:65433
Conectado. Escribe mensajes para enviar al servidor.

Tú: Hola mundo
Echo del servidor: Hola mundo

Tú: Este es un test
Echo del servidor: Este es un test

Tú: salir
Cerrando conexión...
```

## Conceptos Clave

- **Patrón Request/Response**: El cliente envía una solicitud y espera una respuesta
- **Echo Server**: Devuelve exactamente los mismos datos que recibe
- **Sockets TCP**: Garantiza entrega ordenada y confiable de mensajes

## Diferencias con 01_sockets

- Más simple: solo hace echo, no permite conversación bidireccional
- Sin threading: maneja un cliente a la vez (secuencial)
- Enfoque en el patrón básico de petición/respuesta
