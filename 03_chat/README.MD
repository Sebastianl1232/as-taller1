# 03_chat - Chat Multiusuario

## Descripción

Sistema de chat que permite que múltiples usuarios se conecten simultáneamente y vean los mensajes de todos en tiempo real.

## Archivos

- `servidor.py`: Servidor central que maneja múltiples conexiones y hace broadcasting de mensajes.
- `cliente.py`: Cliente que se conecta al servidor con un nombre de usuario.

## Características

- ✅ **Multiusuario**: Múltiples clientes conectados simultáneamente
- ✅ **Broadcasting**: Los mensajes se envían a todos los usuarios
- ✅ **Nombres de usuario**: Cada cliente se identifica con un nombre
- ✅ **Notificaciones**: Avisa cuando alguien se une o sale del chat
- ✅ **Threading**: Manejo concurrente de múltiples clientes
- ✅ **Puerto**: 65434

## Uso

### 1. Iniciar el servidor

```bash
python servidor.py
```

### 2. Conectar múltiples clientes

En terminales separadas:

```bash
python cliente.py
```

Cada cliente deberá ingresar un nombre al conectarse.

## Ejemplo de interacción

**Servidor:**
```
Servidor de chat escuchando en localhost:65434
Esperando conexiones...

Ana (127.0.0.1, 54321) se ha conectado
Carlos (127.0.0.1, 54322) se ha conectado
Ana: Hola a todos!
Carlos: Hola Ana, ¿cómo estás?
```

**Cliente 1 (Ana):**
```
Ingresa tu nombre: Ana
Bienvenido al chat, Ana!
>>> Carlos se ha unido al chat
Tú: Hola a todos!
Carlos: Hola Ana, ¿cómo estás?
Tú: Muy bien, gracias!
```

**Cliente 2 (Carlos):**
```
Ingresa tu nombre: Carlos
Bienvenido al chat, Carlos!
Ana: Hola a todos!
Tú: Hola Ana, ¿cómo estás?
Ana: Muy bien, gracias!
```

## Conceptos Clave

- **Broadcasting**: Envío de mensajes a todos los clientes conectados
- **Threading**: Cada cliente se maneja en un hilo separado
- **Locks**: Sincronización para evitar conflictos al acceder a la lista de clientes
- **Patrón Publicador/Suscriptor**: El servidor publica mensajes a todos los suscriptores (clientes)

## Comandos

- `salir`, `exit`, `quit`: Desconectarse del chat

## Diferencias con ejemplos anteriores

- Manejo de múltiples clientes simultáneos
- Sistema de nombres de usuario
- Broadcasting de mensajes a todos
- Notificaciones de entrada/salida de usuarios
