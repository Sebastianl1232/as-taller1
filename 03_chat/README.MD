# 03_chat - Chat Multiusuario

## Descripción

Sistema de chat en tiempo real que permite múltiples usuarios conectados simultáneamente. Todos los mensajes se transmiten (broadcast) a todos los clientes conectados.

## Archivos

- `servidor.py`: Servidor que gestiona múltiples clientes y hace broadcast de mensajes.
- `cliente.py`: Cliente de chat con nombre de usuario.

## Características

- **Múltiples usuarios simultáneos**: Varios clientes pueden conectarse al mismo tiempo
- **Broadcast de mensajes**: Los mensajes se envían a todos los usuarios conectados
- **Nombres de usuario**: Cada usuario tiene un nombre identificador
- **Notificaciones**: Avisa cuando alguien se une o sale del chat
- **Threading**: Manejo concurrente de múltiples conexiones
- **Puerto**: 65434

## Uso

```bash
# Terminal 1 - Servidor
python servidor.py

# Terminal 2 - Cliente 1
python cliente.py

# Terminal 3 - Cliente 2
python cliente.py

# Terminal 4 - Cliente N...
python cliente.py
```

## Ejemplo de interacción

**Servidor:**
```text
Servidor de chat multiusuario en localhost:65434
Juan se ha conectado desde ('127.0.0.1', 53422)
María se ha conectado desde ('127.0.0.1', 53423)
Juan: Hola a todos!
María: Hola Juan!
Juan se desconectó
```

**Cliente 1 (Juan):**
```text
Ingresa tu nombre: Juan

Bienvenido al chat, Juan!
Escribe 'salir' para desconectarte.

Tú: Hola a todos!
>>> María se unió al chat
Tú: 
María: Hola Juan!
Tú: salir
```

**Cliente 2 (María):**
```text
Ingresa tu nombre: María

Bienvenido al chat, María!
Escribe 'salir' para desconectarte.

Tú: 
Juan: Hola a todos!
Tú: Hola Juan!
<<< Juan salió del chat
Tú: 
```

## Conceptos Implementados

- **Patrón Publicador/Suscriptor**: Los mensajes se publican a todos los suscriptores
- **Broadcasting**: Envío de mensajes a múltiples destinatarios
- **Threading**: Cada cliente se maneja en un hilo separado
- **Lock/Mutex**: Control de acceso concurrente a recursos compartidos
- **Gestión de estado**: Lista compartida de clientes activos

## Mejoras Posibles

- Salas de chat múltiples
- Mensajes privados entre usuarios
- Lista de usuarios conectados
- Historial de mensajes
- Autenticación de usuarios
