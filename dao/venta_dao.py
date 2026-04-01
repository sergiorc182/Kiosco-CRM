import csv
import os
from datetime import datetime

from app.db import get_connection


class VentaDAO:
    def guardar(self, venta, metodo_pago="Efectivo", id_empleado=None, id_caja=None):
        venta_id = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_metodo FROM metodo_pago WHERE tipo = %s LIMIT 1",
                (metodo_pago,),
            )
            metodo = cursor.fetchone()
            metodo_id = metodo[0] if metodo else None
            cursor.execute(
                """
                INSERT INTO venta (fecha, total, id_empleado, id_caja, id_metodo, id_cliente)
                VALUES (NOW(), %s, %s, %s, %s, 1)
                """,
                (venta.total(), id_empleado, id_caja, metodo_id),
            )
            venta_id = cursor.lastrowid
            for detalle in venta.detalles:
                cursor.execute(
                    """
                    INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (venta_id, detalle.id_producto, detalle.cantidad, detalle.precio),
                )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception:
            venta_id = None

        os.makedirs("data/ventas", exist_ok=True)
        ruta = "data/ventas/ventas.csv"
        existe = os.path.isfile(ruta)
        with open(ruta, "a", newline="", encoding="utf-8") as file_obj:
            writer = csv.writer(file_obj)
            if not existe:
                writer.writerow(["Fecha", "Cliente", "Total", "Metodo", "Detalles"])
            detalles_str = "; ".join(
                f"{detalle.producto} x{detalle.cantidad} (${detalle.precio:.2f})"
                for detalle in venta.detalles
            )
            writer.writerow(
                [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    venta.cliente,
                    f"{venta.total():.2f}",
                    metodo_pago,
                    detalles_str,
                ]
            )
        return venta_id
