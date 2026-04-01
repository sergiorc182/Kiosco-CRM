import mysql.connector

from dao.usuario_dao import UsuarioDAO


class UsuarioService:
    def __init__(self):
        self.dao = UsuarioDAO()

    def login(self, nombre, password):
        if not nombre or not password:
            return None
        return self.dao.obtener_usuario(nombre, password)

    def crear_usuario(self, nombre_usuario, password, tipo, nombre_real=None):
        if not nombre_usuario or not password or not tipo:
            raise ValueError("Complete los campos obligatorios")
        if tipo.lower() == "empleado" and not nombre_real:
            raise ValueError("El nombre real del empleado es obligatorio")
        if self.dao.usuario_existe(nombre_usuario):
            raise ValueError("El usuario ya existe")
        try:
            self.dao.crear_usuario(nombre_usuario, password, tipo, nombre_real)
        except mysql.connector.Error as exc:
            raise ConnectionError(f"No se pudo guardar el usuario en la base de datos: {exc}") from exc
        return True, "Usuario creado correctamente"

    def listar_usuarios(self):
        return self.dao.listar_usuarios()
