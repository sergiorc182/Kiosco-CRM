import json
import os
from datetime import datetime, timedelta

from dao.turno_dao import TurnoDAO


class TurnoService:
    ESTADO_PATH = "estado_turno.json"
    DIAS = {
        "Lunes": 0,
        "Martes": 1,
        "Miércoles": 2,
        "Jueves": 3,
        "Viernes": 4,
        "Sábado": 5,
        "Domingo": 6,
    }

    def __init__(self):
        self.dao = TurnoDAO()

    def listar_empleados(self):
        return self.dao.listar_empleados()

    def obtener_empleado_por_usuario(self, usuario_id):
        return self.dao.obtener_empleado_por_usuario(usuario_id)

    def _fecha_para_dia(self, nombre_dia):
        hoy = datetime.now()
        dia_deseado = self.DIAS[nombre_dia]
        diferencia = dia_deseado - hoy.weekday()
        if diferencia <= 0:
            diferencia += 7
        return (hoy + timedelta(days=diferencia)).date()

    def _hay_conflicto(self, empleado_id, fecha, hora_inicio, hora_fin, ignorar_turno_id=None):
        existentes = self.dao.obtener_conflictos(empleado_id, fecha, ignorar_turno_id)
        nuevo_inicio = datetime.strptime(hora_inicio, "%H:%M:%S").time()
        nuevo_fin = datetime.strptime(hora_fin, "%H:%M:%S").time()
        for row in existentes:
            inicio = datetime.strptime(str(row["hora_inicio"]), "%H:%M:%S").time()
            fin = datetime.strptime(str(row["hora_fin"]), "%H:%M:%S").time()
            if nuevo_inicio < fin and nuevo_fin > inicio:
                return True
        return False

    def listar_turnos(self):
        return self.dao.listar_turnos()

    def listar_turnos_por_usuario(self, usuario_id):
        return self.dao.listar_turnos_por_usuario(usuario_id)

    def crear_turno(self, nombre, hora_inicio, hora_fin, empleado_id, dia):
        fecha = self._fecha_para_dia(dia)
        if self._hay_conflicto(empleado_id, fecha, hora_inicio, hora_fin):
            raise ValueError("El turno se superpone con otro existente")
        turno_id = self.dao.crear_turno(nombre, hora_inicio, hora_fin)
        self.dao.asignar_turno(turno_id, empleado_id, fecha)
        return turno_id

    def actualizar_turno(self, turno_id, nombre, hora_inicio, hora_fin, empleado_id, dia):
        fecha = self._fecha_para_dia(dia)
        if self._hay_conflicto(empleado_id, fecha, hora_inicio, hora_fin, turno_id):
            raise ValueError("El turno se superpone con otro existente")
        self.dao.actualizar_turno(turno_id, nombre, hora_inicio, hora_fin, empleado_id, fecha)

    def eliminar_turno(self, turno_id):
        self.dao.eliminar_turno(turno_id)

    def obtener_turno_activo(self):
        if not os.path.exists(self.ESTADO_PATH):
            return None
        with open(self.ESTADO_PATH, "r", encoding="utf-8") as file_obj:
            return json.load(file_obj)

    def comenzar_turno(self, turno):
        activo = self.obtener_turno_activo()
        if activo:
            raise ValueError("Ya existe un turno activo")
        payload = {
            "id": turno["id_turno"],
            "empleado": turno["empleado"],
            "inicio": datetime.now().isoformat(),
            "nombre_turno": turno["nombre_turno"],
        }
        with open(self.ESTADO_PATH, "w", encoding="utf-8") as file_obj:
            json.dump(payload, file_obj, indent=2, ensure_ascii=False)
        return payload

    def cerrar_turno(self):
        activo = self.obtener_turno_activo()
        if not activo:
            raise ValueError("No hay un turno activo")
        inicio = datetime.fromisoformat(activo["inicio"])
        horas = (datetime.now() - inicio).seconds / 3600
        if os.path.exists(self.ESTADO_PATH):
            os.remove(self.ESTADO_PATH)
        return {"empleado": activo["empleado"], "horas": horas}
