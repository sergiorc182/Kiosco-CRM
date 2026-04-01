class CompraProveedorVO:
    def __init__(
        self,
        id_compra,
        id_proveedor,
        id_producto,
        cantidad,
        tipo_producto,
        fecha,
        fecha_vencimiento,
        producto=None,
        proveedor_nombre=None,
    ):
        self.id_compra = id_compra
        self.id_proveedor = id_proveedor
        self.id_producto = id_producto
        self.producto = producto
        self.cantidad = cantidad
        self.tipo_producto = tipo_producto
        self.fecha = fecha
        self.fecha_vencimiento = fecha_vencimiento
        self.proveedor_nombre = proveedor_nombre
