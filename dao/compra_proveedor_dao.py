from app.db import get_connection
from modelo.compra_proveedor_vo import CompraProveedorVO


class CompraProveedorDAO:
    def __init__(self):
        self._columna_fecha = None

    def _map(self, row):
        if not row:
            return None
        return CompraProveedorVO(
            id_compra=row["id_compra"],
            id_proveedor=row["id_proveedor"],
            id_producto=row["id_producto"],
            cantidad=row["cantidad"],
            tipo_producto=row["tipo_producto"],
            fecha=row["fecha"],
            fecha_vencimiento=row["fecha_vencimiento"],
            producto=row.get("producto"),
            proveedor_nombre=row.get("proveedor_nombre"),
        )

    def _obtener_columna_fecha(self, cursor):
        if self._columna_fecha:
            return self._columna_fecha

        cursor.execute("SHOW COLUMNS FROM compra_proveedor")
        columnas = set()
        for row in cursor.fetchall():
            if isinstance(row, dict):
                columnas.add(row.get("Field"))
            else:
                columnas.add(row[0])
        if "fecha" in columnas:
            self._columna_fecha = "fecha"
        elif "fecha_hora" in columnas:
            self._columna_fecha = "fecha_hora"
        else:
            raise ValueError("La tabla compra_proveedor no tiene columna 'fecha' ni 'fecha_hora'")
        return self._columna_fecha

    def registrar_compra(self, id_proveedor, id_producto, cantidad, tipo_producto, fecha, fecha_vencimiento):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            columna_fecha = self._obtener_columna_fecha(cursor)
            cursor.execute(
                f"""
                INSERT INTO compra_proveedor (id_proveedor, id_producto, cantidad, tipo_producto, {columna_fecha}, fecha_vencimiento)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (id_proveedor, id_producto, cantidad, tipo_producto, fecha, fecha_vencimiento),
            )
            compra_id = cursor.lastrowid
            cursor.execute(
                """
                UPDATE producto
                SET cantidad = cantidad + %s, id_proveedor = %s
                WHERE id_producto = %s
                """,
                (cantidad, id_proveedor, id_producto),
            )
            cursor.execute(
                """
                INSERT INTO inventario_movimiento (id_producto, tipo_movimiento, cantidad, fecha, id_empleado)
                VALUES (%s, 'Entrada', %s, %s, NULL)
                """,
                (id_producto, cantidad, fecha),
            )
            conn.commit()
            return compra_id
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def listar_compras(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        columna_fecha = self._obtener_columna_fecha(cursor)
        cursor.execute(
            f"""
            SELECT cp.id_compra,
                   cp.id_proveedor,
                   cp.id_producto,
                   pr.nombre AS proveedor_nombre,
                   p.nombre AS producto,
                   cp.cantidad,
                   cp.tipo_producto,
                   cp.{columna_fecha} AS fecha,
                   cp.fecha_vencimiento
            FROM compra_proveedor cp
            JOIN producto p ON cp.id_producto = p.id_producto
            JOIN proveedor pr ON cp.id_proveedor = pr.id_proveedor
            ORDER BY cp.{columna_fecha} DESC, cp.id_compra DESC
            """
        )
        compras = [self._map(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return compras
