from app.db import get_connection
from modelo.producto_vo import ProductoVO


class ProductoDAO:
    def _map(self, row):
        if not row:
            return None
        return ProductoVO(
            id_producto=row["id_producto"],
            codigo=row["codigo_articulo"],
            nombre=row["nombre"],
            precio=float(row["precio"]),
            stock=int(row["cantidad"]),
            seccion=row.get("seccion"),
            id_categoria=row.get("id_categoria"),
        )

    def buscar_por_codigo(self, codigo):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_producto, codigo_articulo, nombre, precio, cantidad, id_categoria, seccion
            FROM producto
            WHERE codigo_articulo = %s
            """,
            (codigo,),
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return self._map(row)

    def buscar_por_id(self, producto_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_producto, codigo_articulo, nombre, precio, cantidad, id_categoria, seccion
            FROM producto
            WHERE id_producto = %s
            """,
            (producto_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return self._map(row)

    def buscar_por_nombre(self, nombre):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_producto, codigo_articulo, nombre, precio, cantidad, id_categoria, seccion, id_proveedor
            FROM producto
            WHERE LOWER(nombre) = LOWER(%s)
            LIMIT 1
            """,
            (nombre,),
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return self._map(row)

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_producto, codigo_articulo, nombre, precio, cantidad, id_categoria, seccion
            FROM producto
            ORDER BY nombre
            """
        )
        rows = [self._map(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return rows

    def crear(self, codigo, nombre, precio, cantidad, seccion=None, id_categoria=None, id_proveedor=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO producto (codigo_articulo, nombre, precio, cantidad, seccion, id_categoria, id_proveedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (codigo, nombre, precio, cantidad, seccion, id_categoria, id_proveedor),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def actualizar(self, codigo, nombre, precio, cantidad, seccion=None, id_categoria=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE producto
            SET nombre = %s, precio = %s, cantidad = %s, seccion = %s, id_categoria = %s
            WHERE codigo_articulo = %s
            """,
            (nombre, precio, cantidad, seccion, id_categoria, codigo),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def eliminar(self, codigo):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM producto WHERE codigo_articulo = %s", (codigo,))
        conn.commit()
        cursor.close()
        conn.close()

    def buscar(self, filtro):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        like = f"%{filtro}%"
        cursor.execute(
            """
            SELECT id_producto, codigo_articulo, nombre, precio, cantidad, id_categoria, seccion
            FROM producto
            WHERE nombre LIKE %s OR codigo_articulo LIKE %s
            ORDER BY nombre
            """,
            (like, like),
        )
        rows = [self._map(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return rows

    def filtrar_por_seccion(self, seccion):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if seccion and seccion != "Todas":
            cursor.execute(
                """
                SELECT id_producto, codigo_articulo, nombre, precio, cantidad, id_categoria, seccion
                FROM producto
                WHERE seccion = %s
                ORDER BY nombre
                """,
                (seccion,),
            )
        else:
            cursor.execute(
                """
                SELECT id_producto, codigo_articulo, nombre, precio, cantidad, id_categoria, seccion
                FROM producto
                ORDER BY nombre
                """
            )
        rows = [self._map(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return rows

    def descontar_stock(self, id_producto, cantidad):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE producto SET cantidad = cantidad - %s WHERE id_producto = %s",
            (cantidad, id_producto),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def incrementar_stock(self, id_producto, cantidad):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE producto SET cantidad = cantidad + %s WHERE id_producto = %s",
            (cantidad, id_producto),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def registrar_movimiento(self, id_producto, tipo_movimiento, cantidad, id_empleado=None):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO inventario_movimiento (id_producto, tipo_movimiento, cantidad, fecha, id_empleado)
            VALUES (%s, %s, %s, NOW(), %s)
            """,
            (id_producto, tipo_movimiento, cantidad, id_empleado),
        )
        conn.commit()
        cursor.close()
        conn.close()
