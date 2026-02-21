import socket
import threading

HOST = "localhost"
PUERTO = 65435
SALIDAS = {"salir", "exit", "quit"}


def enviar_linea(cliente: socket.socket, texto: str) -> None:
	cliente.sendall(f"{texto}\n".encode("utf-8"))


def recibir_mensajes(archivo) -> None:
	while True:
		linea = archivo.readline()
		if not linea:
			print("\nConexión cerrada por el servidor.")
			break

		mensaje = linea.rstrip("\n")
		print(f"\n{mensaje}")
		print("Comando> ", end="", flush=True)


def registrar_usuario(cliente: socket.socket, archivo) -> bool:
	bienvenida = archivo.readline()
	if not bienvenida:
		print("No fue posible iniciar sesión en el servidor.")
		return False

	print(bienvenida.rstrip("\n"))

	while True:
		nombre = input("Tu nombre> ").strip()
		if not nombre:
			continue

		enviar_linea(cliente, f"REGISTER {nombre}")
		respuesta = archivo.readline()
		if not respuesta:
			print("Conexión cerrada durante el registro.")
			return False

		print(respuesta.rstrip("\n"))
		if respuesta.startswith("Registro exitoso"):
			instrucciones = archivo.readline()
			if instrucciones:
				print(instrucciones.rstrip("\n"))
			return True


def bucle_comandos(cliente: socket.socket) -> None:
	while True:
		try:
			comando = input("Comando> ").strip()
		except EOFError:
			comando = "EXIT"

		if not comando:
			continue

		enviar_linea(cliente, comando)
		if comando.lower() in SALIDAS:
			break


def iniciar_cliente():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
		try:
			cliente.connect((HOST, PUERTO))
		except ConnectionRefusedError:
			print(f"No se pudo conectar a {HOST}:{PUERTO}.")
			print("Verifica que el servidor esté ejecutándose.")
			return

		archivo = cliente.makefile("r", encoding="utf-8", newline="\n")
		if not registrar_usuario(cliente, archivo):
			return

		hilo_receptor = threading.Thread(
			target=recibir_mensajes,
			args=(archivo,),
			daemon=True,
		)
		hilo_receptor.start()

		bucle_comandos(cliente)


if __name__ == "__main__":
	try:
		iniciar_cliente()
	except KeyboardInterrupt:
		print("\nCliente finalizado.")

