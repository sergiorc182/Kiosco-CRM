from services.venta_service import VentaService


class VentaController:
    def __init__(self, caja_service=None, producto_service=None):
        self.service = VentaService(caja_service=caja_service, producto_service=producto_service)
        self.venta = self.service.crear_venta()

    def nueva_venta(self, cliente="CONSUMIDOR FINAL"):
        self.venta = self.service.crear_venta(cliente)
        return self.venta

    def agregar_producto(self, producto, cantidad):
        return self.service.agregar_detalle(self.venta, producto, cantidad)

    def eliminar_item(self, indice):
        self.service.eliminar_detalle(self.venta, indice)

    def actualizar_cantidad(self, indice, cantidad):
        return self.service.actualizar_cantidad(self.venta, indice, cantidad)

    def listar_items(self):
        return self.venta.detalles

    def total(self):
        return self.venta.total()

    def confirmar(self, metodo_pago, monto_recibido=None, id_empleado=None):
        resultado = self.service.confirmar_venta(
            self.venta,
            metodo_pago=metodo_pago,
            monto_recibido=monto_recibido,
            id_empleado=id_empleado,
        )
        self.nueva_venta(self.venta.cliente)
        return resultado
