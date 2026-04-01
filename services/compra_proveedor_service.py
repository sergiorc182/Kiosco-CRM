from datetime import datetime

import mysql.connector

from dao.compra_proveedor_dao import CompraProveedorDAO
from services.producto_service import ProductoService


class CompraProveedorService:
    def __init__(self, compra_dao=None, producto_service=None):
        self.compra_dao = compra_dao or CompraProveedorDAO()
        self.producto_service = producto_service or ProductoService()

    def listar_compras(self):
        return self.compra_dao.listar_compras()

    def registrar_compra(self, id_proveedor, id_producto, cantidad, tipo_producto, fecha_vencimiento):
        if not id_proveedor:
            raise ValueError("Debe seleccionar un proveedor")
        if not id_producto:
            raise ValueError("Debe seleccionar un producto")
        if not tipo_producto or not fecha_vencimiento:
            raise ValueError("Todos los campos de la compra son obligatorios")

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError) as exc:
            raise ValueError("La cantidad debe ser numerica") from exc

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        self._validar_fecha(fecha_vencimiento.strip())
        self.producto_service.obtener_producto_por_id(int(id_producto))
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.compra_dao.registrar_compra(
                id_proveedor=int(id_proveedor),
                id_producto=int(id_producto),
                cantidad=cantidad,
                tipo_producto=tipo_producto.strip(),
                fecha=fecha,
                fecha_vencimiento=fecha_vencimiento.strip(),
            )
        except mysql.connector.Error as exc:
            raise ValueError(f"No se pudo registrar la compra: {exc.msg}") from exc

        return True, "Compra registrada correctamente"

    def _validar_fecha(self, fecha_vencimiento):
        try:
            datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("La fecha de vencimiento debe tener formato YYYY-MM-DD") from exc
