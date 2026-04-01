# model/vo/movimiento_caja_vo.py
class MovimientoCajaVO:
    def __init__(self, tipo, monto, descripcion, fecha):
        self.tipo = tipo  # ingreso / egreso
        self.monto = monto
        self.descripcion = descripcion
        self.fecha = fecha