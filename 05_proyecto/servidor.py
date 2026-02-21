import socket
import threading

HOST = "localhost"
PUERTO = 65435
SALIDAS = {"SALIR", "EXIT", "QUIT"}


class ChatServer:
	def __init__(self, host: str, puerto: int) -> None:
		self.host = host
		self.puerto = puerto
		self.clientes = {}
		self.bloqueo = threading.Lock()

	def enviar(self, conexion: socket.socket, texto: str) -> None:
		conexion.sendall(f"{texto}\n".encode("utf-8"))

	def broadcast(self, mensaje: str, excluir: socket.socket | None = None) -> None:
		with self.bloqueo:
			conexiones = list(self.clientes.keys())

		for conexion in conexiones:
			if conexion == excluir:
				continue
			try:
				self.enviar(conexion, mensaje)
			except OSError:
				pass

	def listar_usuarios(self) -> str:
		with self.bloqueo:
			nombres = sorted(self.clientes.values())

		if not nombres:
			return "No hay usuarios conectados."
		return "Usuarios conectados: " + ", ".join(nombres)

	def buscar_conexion_por_nombre(self, nombre: str) -> socket.socket | None:
		with self.bloqueo:
			for conexion, nombre_cliente in self.clientes.items():
				if nombre_cliente == nombre:
					return conexion
		return None

	def registrar_usuario(self, conexion: socket.socket, archivo) -> str | None:
		self.enviar(conexion, "Bienvenido. Regístrate con: REGISTER <nombre>")

		while True:
			linea = archivo.readline()
			if not linea:
				return None

			partes = linea.strip().split(maxsplit=1)
			comando_valido = len(partes) == 2 and partes[0].upper() == "REGISTER"
			if not comando_valido:
				self.enviar(conexion, "Debes registrarte primero. Uso: REGISTER <nombre>")
				continue

			nombre = partes[1].strip()
			if not nombre:
				self.enviar(conexion, "Nombre inválido. Intenta de nuevo.")
				continue

			with self.bloqueo:
				if nombre in self.clientes.values():
					self.enviar(conexion, "Ese nombre ya está en uso. Elige otro.")
					continue
				self.clientes[conexion] = nombre

			self.enviar(conexion, f"Registro exitoso como {nombre}.")
			self.enviar(conexion, "Comandos: USERS | ALL <mensaje> | MSG <usuario> <mensaje> | EXIT")
			self.broadcast(f"[SISTEMA] {nombre} se ha conectado.", excluir=conexion)
			return nombre

	def manejar_comando(self, conexion: socket.socket, nombre: str, linea: str) -> bool:
		texto = linea.strip()
		if not texto:
			self.enviar(conexion, "Comando vacío.")
			return False

		partes = texto.split(maxsplit=2)
		comando = partes[0].upper()

		if comando in SALIDAS:
			self.enviar(conexion, "Conexión cerrada. ¡Hasta luego!")
			return True

		if comando == "USERS":
			self.enviar(conexion, self.listar_usuarios())
			return False

		if comando == "ALL":
			if len(partes) < 2 or not partes[1].strip():
				self.enviar(conexion, "Uso: ALL <mensaje>")
				return False

			mensaje = texto.split(maxsplit=1)[1].strip()
			self.broadcast(f"[GLOBAL] {nombre}: {mensaje}", excluir=conexion)
			self.enviar(conexion, "Mensaje global enviado.")
			return False

		if comando == "MSG":
			if len(partes) < 3:
				self.enviar(conexion, "Uso: MSG <usuario> <mensaje>")
				return False

			destino = partes[1].strip()
			mensaje = partes[2].strip()
			if not destino or not mensaje:
				self.enviar(conexion, "Uso: MSG <usuario> <mensaje>")
				return False

			conexion_destino = self.buscar_conexion_por_nombre(destino)
			if conexion_destino is None:
				self.enviar(conexion, f"Usuario no encontrado: {destino}")
				return False

			try:
				self.enviar(conexion_destino, f"[PRIVADO] {nombre}: {mensaje}")
				self.enviar(conexion, f"Mensaje privado enviado a {destino}.")
			except OSError:
				self.enviar(conexion, f"No se pudo enviar el mensaje a {destino}.")
			return False

		self.enviar(conexion, "Comando no reconocido. Usa USERS, ALL, MSG o EXIT.")
		return False

	def desconectar_cliente(self, conexion: socket.socket, nombre: str | None) -> None:
		with self.bloqueo:
			nombre_salida = self.clientes.pop(conexion, nombre)

		conexion.close()
		if nombre_salida:
			self.broadcast(f"[SISTEMA] {nombre_salida} se ha desconectado.")

	def manejar_cliente(self, conexion: socket.socket, direccion) -> None:
		print(f"Cliente conectado desde {direccion[0]}:{direccion[1]}")
		nombre = None

		try:
			archivo = conexion.makefile("r", encoding="utf-8", newline="\n")
			nombre = self.registrar_usuario(conexion, archivo)
			if nombre is None:
				return

			while True:
				linea = archivo.readline()
				if not linea:
					break
				if self.manejar_comando(conexion, nombre, linea):
					break
		except Exception as error:
			print(f"Error con cliente {direccion}: {error}")
		finally:
			self.desconectar_cliente(conexion, nombre)
			print(f"Cliente desconectado: {direccion[0]}:{direccion[1]}")

	def iniciar(self) -> None:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
			servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			servidor.bind((self.host, self.puerto))
			servidor.listen()

			print(f"Servidor de chat escuchando en {self.host}:{self.puerto}")
			print("Presiona Ctrl+C para detenerlo.")

			try:
				while True:
					conexion, direccion = servidor.accept()
					hilo = threading.Thread(
						target=self.manejar_cliente,
						args=(conexion, direccion),
						daemon=True,
					)
					hilo.start()
			except KeyboardInterrupt:
				print("\nServidor detenido.")


if __name__ == "__main__":
	ChatServer(HOST, PUERTO).iniciar()

