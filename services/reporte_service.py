import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class ReporteService:
    EMAIL_FROM = "Software.Kiosco@gmail.com"
    EMAIL_PASSWORD = "feyu zacq rcsc jedy"
    EMAIL_TO = "sergiomanslla384@gmail.com"

    def guardar_reporte_local(self, email, reporte):
        os.makedirs("data/reportes", exist_ok=True)
        path = os.path.join(
            "data",
            "reportes",
            f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        )
        with open(path, "w", encoding="utf-8") as file_obj:
            file_obj.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            file_obj.write(f"Email: {email or 'No proporcionado'}\n")
            file_obj.write(f"Reporte:\n{reporte}\n")
        return path

    def enviar_reporte(self, reporte, email_usuario=""):
        if not reporte.strip():
            raise ValueError("El reporte no puede estar vacío")
        path = self.guardar_reporte_local(email_usuario, reporte)
        mensaje = MIMEMultipart()
        mensaje["From"] = self.EMAIL_FROM
        mensaje["To"] = self.EMAIL_TO
        mensaje["Subject"] = f"Reporte Sistema Kiosco - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        cuerpo = (
            "NUEVO REPORTE DEL SISTEMA DE KIOSCO\n\n"
            f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Email del usuario: {email_usuario or 'No proporcionado'}\n\n"
            f"{reporte}\n"
        )
        mensaje.attach(MIMEText(cuerpo, "plain"))
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.EMAIL_FROM, self.EMAIL_PASSWORD)
                server.send_message(mensaje)
            return True, path
        except Exception:
            return False, path
