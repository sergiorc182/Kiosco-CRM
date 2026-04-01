from datetime import datetime

class Caja:
    def __init__(self, id_caja=None, fecha=None, monto_apertura=0, monto_cierre=0, extraccion=0, id_empleado=1):
        self.id_caja = id_caja
        self.fecha = fecha or datetime.now()
        self.monto_apertura = monto_apertura
        self.monto_cierre = monto_cierre
        self.extraccion = extraccion
        self.id_empleado = id_empleado

        self.saldo = monto_apertura
        self.ventas = []
        self.gastos = []