from services.proveedor_service import ProveedorService


class ProveedorController:
    def __init__(self):
        self.service = ProveedorService()

    def crear_proveedor(self, nombre, contacto, telefono, direccion):
        return self.service.crear_proveedor(nombre, contacto, telefono, direccion)

    def editar_proveedor(self, id_proveedor, nombre, contacto, telefono, direccion):
        return self.service.actualizar_proveedor(id_proveedor, nombre, contacto, telefono, direccion)

    def eliminar_proveedor(self, id_proveedor):
        return self.service.eliminar_proveedor(id_proveedor)

    def listar_proveedores(self):
        return self.service.listar_proveedores()
