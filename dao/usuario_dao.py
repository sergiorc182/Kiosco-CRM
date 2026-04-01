import mysql.connector

from app.db import get_connection
from modelo.usuario_vo import UsuarioVO


class UsuarioDAO:
    def _password_column(self, cursor):
        cursor.execute("SHOW COLUMNS FROM usuario")
        for row in cursor.fetchall():
            field_name = row[0] if not isinstance(row, dict) else row["Field"]
            if "contra" in field_name.lower():
                return field_name
        raise ValueError("No se encontro la columna de contrasena en la tabla usuario")

    def obtener_usuario(self, nombre, password):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        password_column = self._password_column(cursor)
        cursor.execute(
            f"SELECT id_usuario, nombre, `{password_column}` AS password, tipo FROM usuario WHERE nombre=%s AND `{password_column}`=%s",
            (nombre, password),
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        return UsuarioVO(
            id_usuario=row["id_usuario"],
            nombre=row["nombre"],
            password=row["password"],
            tipo=row["tipo"],
        )

    def usuario_existe(self, nombre_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM usuario WHERE nombre = %s LIMIT 1", (nombre_usuario,))
        existe = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return existe

    def crear_usuario(self, nombre_usuario, password, tipo, nombre_real=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            password_column = self._password_column(cursor)
            cursor.execute(
                f"INSERT INTO usuario (nombre, `{password_column}`, tipo) VALUES (%s, %s, %s)",
                (nombre_usuario, password, tipo),
            )
            usuario_id = cursor.lastrowid
            if tipo.lower() == "admin":
                cursor.execute("INSERT INTO admin (id_usuario) VALUES (%s)", (usuario_id,))
            else:
                cursor.execute(
                    "INSERT INTO empleado (id_usuario, nombre) VALUES (%s, %s)",
                    (usuario_id, nombre_real or nombre_usuario),
                )
            conn.commit()
            return usuario_id
        except mysql.connector.Error:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def listar_usuarios(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nombre, tipo FROM usuario ORDER BY nombre")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
