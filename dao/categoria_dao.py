import mysql.connector

class CategoriaDAO:

    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "kiosco"
        }

    def _conectar(self):
        return mysql.connector.connect(**self.config)

    def guardar(self, categoria):
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()

            query = "INSERT INTO categoria (nombre) VALUES (%s)"
            cursor.execute(query, (categoria.nombre,))

            conexion.commit()
            conexion.close()
            return True

        except Exception as e:
            print("Error DAO:", e)
            return False