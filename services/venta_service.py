from dao.venta_dao import VentaDAO
from modelo.detalle_venta_vo import DetalleVentaVO
from modelo.venta_vo import VentaVO
from services.caja_service import CajaService
from services.producto_service import ProductoService


class VentaService:
    def __init__(self, caja_service=None, producto_service=None):
        self.dao = VentaDAO()
        self.caja_service = caja_service or CajaService()
        self.producto_service = producto_service or ProductoService()

    def crear_venta(self, cliente="CONSUMIDOR FINAL"):
        return VentaVO(cliente)

    def agregar_detalle(self, venta, producto, cantidad):
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        detalle = DetalleVentaVO(
            id_producto=producto.id_producto,
            producto=producto.nombre,
            cantidad=cantidad,
            precio=float(producto.precio),
        )
        venta.agregar_detalle(detalle)
        return detalle

    def eliminar_detalle(self, venta, indice):
        if indice < 0 or indice >= len(venta.detalles):
            raise IndexError("Detalle inválido")
        del venta.detalles[indice]

    def actualizar_cantidad(self, venta, indice, cantidad):
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        venta.detalles[indice].cantidad = cantidad
        return venta.detalles[indice]

    def confirmar_venta(self, venta, metodo_pago, monto_recibido=None, id_empleado=None):
        if not venta.detalles:
            raise ValueError("No hay productos en la venta")
        for detalle in venta.detalles:
            producto = self.producto_service.obtener_producto_por_id(detalle.id_producto)
            self.producto_service.descontar_stock(producto, detalle.cantidad, id_empleado)
        venta.metodo_pago = metodo_pago
        estado_caja = self.caja_service.obtener_estado()
        venta_id = self.dao.guardar(
            venta,
            metodo_pago=metodo_pago,
            id_empleado=id_empleado,
            id_caja=estado_caja.get("id_caja"),
        )
        descripcion = "; ".join(f"{d.producto} x{d.cantidad}" for d in venta.detalles)
        self.caja_service.registrar_venta(venta.total(), descripcion)
        vuelto = 0.0
        if monto_recibido is not None and metodo_pago.lower() == "efectivo":
            vuelto = float(monto_recibido) - venta.total()
        return {"venta_id": venta_id, "total": venta.total(), "vuelto": vuelto}
