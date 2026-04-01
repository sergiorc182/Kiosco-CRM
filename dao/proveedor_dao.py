from app.db import get_connection
from modelo.proveedor_vo import ProveedorVO


class ProveedorDAO:
    def _map(self, row):
        if not row:
            return None
        return ProveedorVO(
            id_proveedor=row["id_proveedor"],
            nombre=row["nombre"],
            contacto=row["contacto"],
            telefono=row["telefono"],
            direccion=row["direccion"],
        )

    def insertar_proveedor(self, nombre, contacto, telefono, direccion):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO proveedor (nombre, contacto, telefono, direccion)
            VALUES (%s, %s, %s, %s)
            """,
            (nombre, contacto, telefono, direccion),
        )
        conn.commit()
        proveedor_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return proveedor_id

    def listar_proveedores(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_proveedor, nombre, contacto, telefono, direccion
            FROM proveedor
            ORDER BY nombre
            """
        )
        proveedores = [self._map(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return proveedores

    def actualizar_proveedor(self, id_proveedor, nombre, contacto, telefono, direccion):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE proveedor
            SET nombre = %s, contacto = %s, telefono = %s, direccion = %s
            WHERE id_proveedor = %s
            """,
            (nombre, contacto, telefono, direccion, id_proveedor),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def eliminar_proveedor(self, id_proveedor):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        conn.commit()
        cursor.close()
        conn.close()
