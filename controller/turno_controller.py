from services.turno_service import TurnoService


class TurnoController:
    def __init__(self):
        self.service = TurnoService()

    def listar_empleados(self):
        return self.service.listar_empleados()

    def obtener_empleado_por_usuario(self, usuario_id):
        return self.service.obtener_empleado_por_usuario(usuario_id)

    def listar_turnos(self):
        return self.service.listar_turnos()

    def listar_turnos_por_usuario(self, usuario_id):
        return self.service.listar_turnos_por_usuario(usuario_id)

    def crear_turno(self, nombre, hora_inicio, hora_fin, empleado_id, dia):
        return self.service.crear_turno(nombre, hora_inicio, hora_fin, empleado_id, dia)

    def editar_turno(self, turno_id, nombre, hora_inicio, hora_fin, empleado_id, dia):
        self.service.actualizar_turno(turno_id, nombre, hora_inicio, hora_fin, empleado_id, dia)

    def eliminar_turno(self, turno_id):
        self.service.eliminar_turno(turno_id)

    def comenzar_turno(self, turno):
        return self.service.comenzar_turno(turno)

    def cerrar_turno(self):
        return self.service.cerrar_turno()

    def obtener_turno_activo(self):
        return self.service.obtener_turno_activo()
