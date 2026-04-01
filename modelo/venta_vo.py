class VentaVO:
    def __init__(self, cliente):
        self.cliente = cliente
        self.detalles = []
        self.metodo_pago = None

    def agregar_detalle(self, detalle):
        self.detalles.append(detalle)

    def total(self):
        return sum(detalle.subtotal() for detalle in self.detalles)
