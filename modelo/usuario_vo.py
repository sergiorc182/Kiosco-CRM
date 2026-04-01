# model/vo/usuario_vo.py
class UsuarioVO:
    def __init__(self, id_usuario, nombre, password, tipo):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.password = password
        self.tipo = tipo