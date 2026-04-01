class DetalleVentaVO:
    def __init__(self, id_producto, producto, cantidad, precio):
        self.id_producto = id_producto
        self.producto = producto
        self.cantidad = cantidad
        self.precio = precio

    def subtotal(self):
        return self.cantidad * self.precio
