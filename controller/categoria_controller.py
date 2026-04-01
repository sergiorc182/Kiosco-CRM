from dao.categoria_dao import CategoriaDAO
from modelo.categoria_vo import Categoria


class CategoriaController:
    def __init__(self):
        self.dao = CategoriaDAO()

    def crear_categoria(self, nombre):
        if not nombre.strip():
            return False, "El nombre no puede estar vacío"
        categoria = Categoria(nombre.strip())
        if self.dao.guardar(categoria):
            return True, "Categoría guardada correctamente"
        return False, "Error al guardar la categoría"
