class Categoria:
    def __init__(self, nombre, id_categoria=None):
        self.id_categoria = id_categoria
        self.nombre = nombre

    def __str__(self):
        return f"Categoria({self.id_categoria}, {self.nombre})"