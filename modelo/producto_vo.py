class ProductoVO:
    def __init__(self, id_producto, codigo, nombre, precio, stock, seccion=None, id_categoria=None):
        self.id_producto = id_producto
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.seccion = seccion
        self.id_categoria = id_categoria
