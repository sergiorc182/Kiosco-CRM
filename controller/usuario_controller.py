from services.usuario_service import UsuarioService


class UsuarioController:
    def __init__(self):
        self.service = UsuarioService()

    def login(self, nombre, password):
        return self.service.login(nombre, password)

    def crear_usuario(self, nombre_usuario, password, tipo, nombre_real=None):
        return self.service.crear_usuario(nombre_usuario, password, tipo, nombre_real)

    def listar_usuarios(self):
        return self.service.listar_usuarios()
