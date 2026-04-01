from services.reporte_service import ReporteService


class ReporteController:
    def __init__(self):
        self.service = ReporteService()

    def enviar_reporte(self, reporte, email_usuario=""):
        return self.service.enviar_reporte(reporte, email_usuario)
