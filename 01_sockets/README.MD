# 01_sockets - Sockets basicos

## Descripcion

Ejemplo basico de comunicacion cliente-servidor usando sockets TCP.

## Archivos

- `servidor.py`: escucha conexiones, recibe mensajes y puede responder.
- `cliente.py`: se conecta al servidor y envia mensajes.

## Caracteristicas

- Comunicacion bidireccional (cliente y servidor pueden enviar mensajes).
- Respuesta automatica del servidor a cada mensaje recibido.
- Comando de salida: `salir`, `exit` o `quit`.
- Conexion TCP con `localhost:65432`.

## Uso

```bash
# Terminal 1 - Servidor
python 01_sockets/servidor.py

# Terminal 2 - Cliente
python 01_sockets/cliente.py
```

## Ejemplo de interaccion

```text
Servidor escuchando en localhost:65432
Conexion establecida desde ('127.0.0.1', 53421)
Cliente: Hola
Servidor: (escribe una respuesta y presiona Enter)
```

## Notas

- El servidor responde con `Recibido: <mensaje>` de forma automatica.
- Para terminar la sesion, escribe `salir` en el cliente o en el servidor.
