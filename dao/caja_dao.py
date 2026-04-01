from datetime import date

from app.db import get_connection


class CajaDAO:
    def crear_apertura(self, monto_apertura, id_empleado=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO caja (fecha, monto_apertura, extraccion, monto_cierre, id_empleado)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (date.today(), monto_apertura, 0, 0, id_empleado),
        )
        conn.commit()
        caja_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return caja_id

    def actualizar_cierre(self, caja_id, monto_cierre, extraccion):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE caja
            SET monto_cierre = %s, extraccion = %s
            WHERE id_caja = %s
            """,
            (monto_cierre, extraccion, caja_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def registrar_gasto(self, descripcion, monto, id_empleado=None, id_caja=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO gasto (descripcion, monto, fecha, id_empleado, id_caja)
            VALUES (%s, %s, CURDATE(), %s, %s)
            """,
            (descripcion, monto, id_empleado, id_caja),
        )
        conn.commit()
        cursor.close()
        conn.close()
