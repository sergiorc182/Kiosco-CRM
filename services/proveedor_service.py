import mysql.connector

from dao.proveedor_dao import ProveedorDAO


class ProveedorService:
    def __init__(self, proveedor_dao=None):
        self.proveedor_dao = proveedor_dao or ProveedorDAO()

    def crear_proveedor(self, nombre, contacto, telefono, direccion):
        self._validar_campos_proveedor(nombre, contacto, telefono, direccion)
        self.proveedor_dao.insertar_proveedor(nombre.strip(), contacto.strip(), telefono.strip(), direccion.strip())
        return True, "Proveedor agregado correctamente"

    def listar_proveedores(self):
        return self.proveedor_dao.listar_proveedores()

    def actualizar_proveedor(self, id_proveedor, nombre, contacto, telefono, direccion):
        if not id_proveedor:
            raise ValueError("Debe seleccionar un proveedor")
        self._validar_campos_proveedor(nombre, contacto, telefono, direccion)
        self.proveedor_dao.actualizar_proveedor(int(id_proveedor), nombre.strip(), contacto.strip(), telefono.strip(), direccion.strip())
        return True, "Proveedor actualizado correctamente"

    def eliminar_proveedor(self, id_proveedor):
        if not id_proveedor:
            raise ValueError("Debe seleccionar un proveedor")
        try:
            self.proveedor_dao.eliminar_proveedor(int(id_proveedor))
        except mysql.connector.Error as exc:
            if exc.errno in (1451, 1217):
                raise ValueError("No se puede eliminar el proveedor porque tiene compras o productos asociados") from exc
            raise
        return True, "Proveedor eliminado correctamente"

    def _validar_campos_proveedor(self, nombre, contacto, telefono, direccion):
        if not nombre or not contacto or not telefono or not direccion:
            raise ValueError("Todos los campos del proveedor son obligatorios")
