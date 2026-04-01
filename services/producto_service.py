from dao.producto_dao import ProductoDAO
import re
from datetime import datetime


class ProductoService:
    def __init__(self):
        self.dao = ProductoDAO()

    def obtener_producto(self, codigo):
        producto = self.dao.buscar_por_codigo(codigo)
        if not producto:
            raise ValueError("Producto no encontrado")
        return producto

    def obtener_producto_por_id(self, producto_id):
        producto = self.dao.buscar_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        return producto

    def obtener_producto_por_nombre(self, nombre):
        if not nombre:
            raise ValueError("El nombre del producto es obligatorio")
        return self.dao.buscar_por_nombre(nombre.strip())

    def crear_producto(self, codigo, nombre, precio, cantidad, seccion=None):
        if not codigo or not nombre:
            raise ValueError("Codigo y nombre son obligatorios")
        if self.dao.buscar_por_codigo(codigo):
            raise ValueError("El codigo del producto ya existe")
        self.dao.crear(codigo, nombre, float(precio), int(cantidad), seccion)
        return True, "Producto agregado correctamente"

    def crear_producto_desde_compra(self, nombre, cantidad, seccion=None, id_proveedor=None, precio=0):
        if not nombre:
            raise ValueError("El nombre del producto es obligatorio")
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        codigo = self._generar_codigo(nombre)
        while self.dao.buscar_por_codigo(codigo):
            codigo = self._generar_codigo(nombre, con_sufijo=True)
        self.dao.crear(codigo, nombre.strip(), float(precio), cantidad, seccion, None, id_proveedor)
        producto = self.dao.buscar_por_codigo(codigo)
        if producto:
            self.dao.registrar_movimiento(producto.id_producto, "Entrada", cantidad)
        return producto

    def listar(self):
        return self.dao.listar()

    def eliminar(self, codigo):
        self.dao.eliminar(codigo)
        return True, "Producto eliminado correctamente"

    def actualizar(self, codigo, nombre, precio, cantidad, seccion=None):
        self.dao.actualizar(codigo, nombre, float(precio), int(cantidad), seccion)
        return True, "Producto actualizado correctamente"

    def buscar(self, filtro):
        return self.dao.buscar(filtro)

    def filtrar_seccion(self, seccion):
        return self.dao.filtrar_por_seccion(seccion)

    def descontar_stock(self, producto, cantidad, id_empleado=None):
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente de {producto.nombre}")
        self.dao.descontar_stock(producto.id_producto, cantidad)
        self.dao.registrar_movimiento(producto.id_producto, "Salida", cantidad, id_empleado)

    def incrementar_stock(self, producto, cantidad, id_empleado=None):
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        self.dao.incrementar_stock(producto.id_producto, cantidad)
        self.dao.registrar_movimiento(producto.id_producto, "Entrada", cantidad, id_empleado)

    def _generar_codigo(self, nombre, con_sufijo=False):
        base = re.sub(r"[^A-Z0-9]", "", nombre.upper())[:8] or "PROD"
        timestamp = datetime.now().strftime("%H%M%S%f" if con_sufijo else "%M%S%f")
        return f"{base}-{timestamp}"
