# 05 - Proyecto: Chat con Registro de Clientes

## Descripción

Este proyecto implementa un sistema cliente/servidor de chat por sockets TCP.

- El **servidor** permite conexiones concurrentes de múltiples clientes.
- Cada cliente debe **registrar un nombre único** al conectarse.
- Los usuarios pueden enviarse mensajes globales y privados.

## Arquitectura

- **Modelo:** Cliente/Servidor
- **Transporte:** TCP
- **Concurrencia del servidor:** un hilo por cliente (`threading`)
- **Sin dependencias externas:** solo librería estándar de Python

## Puerto usado

- `localhost:65435`

Si el puerto está ocupado, puedes cambiar la constante `PUERTO` en `servidor.py` y `cliente.py`.

## Comandos del cliente

- `REGISTER <nombre>` → registra al cliente (obligatorio al iniciar)
- `USERS` → lista los usuarios conectados
- `ALL <mensaje>` → envía un mensaje global a todos
- `MSG <usuario> <mensaje>` → envía un mensaje privado
- `EXIT` (o `SALIR` / `QUIT`) → cierra la conexión

## Ejecución

En una terminal:

```bash
cd 05_proyecto
python servidor.py
```

En otra terminal:

```bash
cd 05_proyecto
python cliente.py
```

Puedes abrir varias terminales de cliente para probar la comunicación entre usuarios.
