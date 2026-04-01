from services.compra_proveedor_service import CompraProveedorService


class CompraProveedorController:
    def __init__(self):
        self.service = CompraProveedorService()

    def listar_compras(self):
        return self.service.listar_compras()

    def registrar_compra(self, id_proveedor, id_producto, cantidad, tipo_producto, fecha_vencimiento):
        return self.service.registrar_compra(
            id_proveedor=id_proveedor,
            id_producto=id_producto,
            cantidad=cantidad,
            tipo_producto=tipo_producto,
            fecha_vencimiento=fecha_vencimiento,
        )
