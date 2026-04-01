from services.caja_service import CajaService


class CajaController:
    def __init__(self):
        self.service = CajaService()

    def obtener_estado(self):
        return self.service.obtener_estado()

    def abrir(self, monto, id_empleado=None):
        return self.service.abrir_caja(monto, id_empleado)

    def ingreso(self, monto, motivo):
        return self.service.registrar_ingreso(monto, motivo)

    def retiro(self, monto, motivo):
        return self.service.registrar_retiro(monto, motivo)

    def gasto(self, monto, motivo):
        return self.service.registrar_gasto(monto, motivo)

    def venta(self, total, descripcion):
        return self.service.registrar_venta(total, descripcion)

    def cerrar(self, monto_real):
        return self.service.cerrar_caja(monto_real)
