from app.db import get_connection


class TurnoDAO:
    def listar_empleados(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_empleado, dni, nombre FROM empleado ORDER BY nombre")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def obtener_empleado_por_usuario(self, usuario_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_empleado, nombre
            FROM empleado
            WHERE id_usuario = %s
            LIMIT 1
            """,
            (usuario_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def crear_turno(self, nombre, hora_inicio, hora_fin):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO turno(nombre_turno, hora_inicio, hora_fin) VALUES (%s, %s, %s)",
            (nombre, hora_inicio, hora_fin),
        )
        conn.commit()
        turno_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return turno_id

    def asignar_turno(self, turno_id, empleado_id, fecha):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO turno_empleado (id_turno, id_empleado, fecha) VALUES (%s, %s, %s)",
            (turno_id, empleado_id, fecha),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def listar_turnos(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT t.id_turno, t.nombre_turno, t.hora_inicio, t.hora_fin, e.nombre AS empleado, te.id_empleado, te.fecha
            FROM turno_empleado te
            JOIN turno t ON te.id_turno = t.id_turno
            JOIN empleado e ON te.id_empleado = e.id_empleado
            ORDER BY te.fecha, t.hora_inicio
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def listar_turnos_por_usuario(self, usuario_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT t.id_turno, t.nombre_turno, t.hora_inicio, t.hora_fin, e.nombre AS empleado, te.id_empleado, te.fecha
            FROM turno_empleado te
            JOIN turno t ON te.id_turno = t.id_turno
            JOIN empleado e ON te.id_empleado = e.id_empleado
            WHERE e.id_usuario = %s
            ORDER BY te.fecha, t.hora_inicio
            """,
            (usuario_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def obtener_conflictos(self, empleado_id, fecha, ignorar_turno_id=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t.hora_inicio, t.hora_fin
            FROM turno_empleado te
            JOIN turno t ON te.id_turno = t.id_turno
            WHERE te.id_empleado = %s AND te.fecha = %s
        """
        params = [empleado_id, fecha]
        if ignorar_turno_id is not None:
            query += " AND te.id_turno != %s"
            params.append(ignorar_turno_id)
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def actualizar_turno(self, turno_id, nombre, hora_inicio, hora_fin, empleado_id, fecha):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE turno
            SET nombre_turno = %s, hora_inicio = %s, hora_fin = %s
            WHERE id_turno = %s
            """,
            (nombre, hora_inicio, hora_fin, turno_id),
        )
        cursor.execute(
            """
            UPDATE turno_empleado
            SET id_empleado = %s, fecha = %s
            WHERE id_turno = %s
            """,
            (empleado_id, fecha, turno_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def eliminar_turno(self, turno_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM turno_empleado WHERE id_turno = %s", (turno_id,))
        cursor.execute("DELETE FROM turno WHERE id_turno = %s", (turno_id,))
        conn.commit()
        cursor.close()
        conn.close()
