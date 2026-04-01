from services.producto_service import ProductoService


class ProductoController:
    def __init__(self):
        self.service = ProductoService()

    def obtener_por_codigo(self, codigo):
        return self.service.obtener_producto(codigo)

    def crear(self, codigo, nombre, precio, cantidad, seccion=None):
        return self.service.crear_producto(codigo, nombre, precio, cantidad, seccion)

    def listar(self):
        return self.service.listar()

    def eliminar(self, codigo):
        return self.service.eliminar(codigo)

    def actualizar(self, codigo, nombre, precio, cantidad, seccion=None):
        return self.service.actualizar(codigo, nombre, precio, cantidad, seccion)

    def buscar(self, filtro):
        return self.service.buscar(filtro)

    def filtrar(self, seccion):
        return self.service.filtrar_seccion(seccion)
