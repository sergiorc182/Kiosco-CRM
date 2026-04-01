import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from controller.compra_proveedor_controller import CompraProveedorController
from controller.producto_controller import ProductoController
from controller.proveedor_controller import ProveedorController
from vista.theme import CRM_THEME, build_styles


class ProveedorView(tk.Frame):
    def __init__(self, master=None):
        build_styles()
        super().__init__(master, bg=CRM_THEME["mist"], padx=20, pady=20)
        self.controller = ProveedorController()
        self.compra_controller = CompraProveedorController()
        self.producto_controller = ProductoController()
        self.proveedores_cache = []
        self.productos_cache = []
        self.proveedor_seleccionado_id = None
        self.pack(fill="both", expand=True)
        self._crear_ui()
        self.cargar_datos()

    def _crear_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = tk.Frame(self, bg=CRM_THEME["mist"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        tk.Label(header, text="Proveedores", font=("Segoe UI Semibold", 26), bg=CRM_THEME["mist"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(header, text="Alta de proveedores y registro de compras integrado con inventario.", font=("Segoe UI", 10), bg=CRM_THEME["mist"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 0))

        body = tk.Frame(self, bg=CRM_THEME["mist"])
        body.grid(row=1, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        left = tk.Frame(body, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right = tk.Frame(body, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew")
        left.columnconfigure(0, weight=1)
        left.rowconfigure(2, weight=1)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(2, weight=1)

        tk.Label(left, text="Formulario proveedor", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).grid(row=0, column=0, sticky="w")
        form = tk.Frame(left, bg=CRM_THEME["panel"])
        form.grid(row=1, column=0, sticky="ew", pady=(12, 14))
        form.columnconfigure(0, weight=1)
        self.nombre = self._field(form, "Nombre", 0)
        self.contacto = self._field(form, "Contacto", 1)
        self.telefono = self._field(form, "Telefono", 2)
        self.direccion = self._field(form, "Direccion", 3)

        acciones = tk.Frame(form, bg=CRM_THEME["panel"])
        acciones.grid(row=8, column=0, sticky="ew", pady=(14, 0))
        acciones.columnconfigure(0, weight=1)
        acciones.columnconfigure(1, weight=1)
        acciones.columnconfigure(2, weight=1)
        ttk.Button(acciones, text="Agregar", command=self.agregar_proveedor, style="CRMPrimary.TButton").grid(row=0, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(acciones, text="Editar", command=self.editar_proveedor, style="CRMSecondary.TButton").grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(acciones, text="Eliminar", command=self.eliminar_proveedor, style="CRMOutline.TButton").grid(row=0, column=2, sticky="ew", padx=(4, 0))

        tabla_frame = tk.Frame(left, bg=CRM_THEME["panel"])
        tabla_frame.grid(row=2, column=0, sticky="nsew")
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)
        cols = ("id", "nombre", "contacto", "telefono", "direccion")
        self.tabla_proveedores = ttk.Treeview(tabla_frame, columns=cols, show="headings", style="CRM.Treeview")
        headers = {
            "id": ("ID", 60),
            "nombre": ("Nombre", 150),
            "contacto": ("Contacto", 150),
            "telefono": ("Telefono", 120),
            "direccion": ("Direccion", 220),
        }
        for col, (texto, width) in headers.items():
            self.tabla_proveedores.heading(col, text=texto)
            self.tabla_proveedores.column(col, width=width, anchor="center")
        self.tabla_proveedores.grid(row=0, column=0, sticky="nsew")
        self.tabla_proveedores.bind("<<TreeviewSelect>>", self._cargar_proveedor_seleccionado)

        ttk.Button(right, text="Registrar compra", command=self.abrir_popup_compra, style="CRMPrimary.TButton").grid(row=0, column=0, sticky="e")
        tk.Label(right, text="Compras registradas", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).grid(row=1, column=0, sticky="w", pady=(12, 8))

        compras_frame = tk.Frame(right, bg=CRM_THEME["panel"])
        compras_frame.grid(row=2, column=0, sticky="nsew")
        compras_frame.columnconfigure(0, weight=1)
        compras_frame.rowconfigure(0, weight=1)
        compras_cols = ("proveedor", "producto", "cantidad", "tipo")
        self.tabla_compras = ttk.Treeview(compras_frame, columns=compras_cols, show="headings", style="CRM.Treeview")
        compras_headers = {
            "proveedor": ("Nombre proveedor", 170),
            "producto": ("Producto", 160),
            "cantidad": ("Cantidad ingresada", 130),
            "tipo": ("Tipo producto", 120),
        }
        for col, (texto, width) in compras_headers.items():
            self.tabla_compras.heading(col, text=texto)
            self.tabla_compras.column(col, width=width, anchor="center")
        self.tabla_compras.grid(row=0, column=0, sticky="nsew")

    def _field(self, parent, label, row):
        tk.Label(parent, text=label, bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=row * 2, column=0, sticky="w", pady=(0 if row == 0 else 10, 6))
        entry = ttk.Entry(parent, style="CRM.TEntry")
        entry.grid(row=row * 2 + 1, column=0, sticky="ew")
        return entry

    def cargar_datos(self):
        self.proveedores_cache = self.controller.listar_proveedores()
        self.productos_cache = self.producto_controller.listar()
        self._poblar_proveedores()
        self._poblar_compras()

    def _poblar_proveedores(self):
        for item in self.tabla_proveedores.get_children():
            self.tabla_proveedores.delete(item)
        for proveedor in self.proveedores_cache:
            self.tabla_proveedores.insert(
                "",
                "end",
                values=(
                    proveedor.id_proveedor,
                    proveedor.nombre,
                    proveedor.contacto,
                    proveedor.telefono,
                    proveedor.direccion,
                ),
            )

    def _poblar_compras(self):
        for item in self.tabla_compras.get_children():
            self.tabla_compras.delete(item)
        for compra in self.compra_controller.listar_compras():
            self.tabla_compras.insert(
                "",
                "end",
                values=(
                    compra.proveedor_nombre,
                    compra.producto,
                    compra.cantidad,
                    compra.tipo_producto,
                ),
            )

    def _cargar_proveedor_seleccionado(self, _event=None):
        seleccion = self.tabla_proveedores.selection()
        if not seleccion:
            return
        proveedor_id, nombre, contacto, telefono, direccion = self.tabla_proveedores.item(seleccion[0], "values")
        self.proveedor_seleccionado_id = proveedor_id
        for entry, valor in (
            (self.nombre, nombre),
            (self.contacto, contacto),
            (self.telefono, telefono),
            (self.direccion, direccion),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def agregar_proveedor(self):
        try:
            _, mensaje = self.controller.crear_proveedor(
                self.nombre.get().strip(),
                self.contacto.get().strip(),
                self.telefono.get().strip(),
                self.direccion.get().strip(),
            )
            messagebox.showinfo("Proveedores", mensaje)
            self.cargar_datos()
            self._limpiar_formulario()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def editar_proveedor(self):
        try:
            _, mensaje = self.controller.editar_proveedor(
                self.proveedor_seleccionado_id,
                self.nombre.get().strip(),
                self.contacto.get().strip(),
                self.telefono.get().strip(),
                self.direccion.get().strip(),
            )
            messagebox.showinfo("Proveedores", mensaje)
            self.cargar_datos()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def eliminar_proveedor(self):
        if not self.proveedor_seleccionado_id:
            messagebox.showerror("Error", "Debe seleccionar un proveedor")
            return
        try:
            _, mensaje = self.controller.eliminar_proveedor(self.proveedor_seleccionado_id)
            messagebox.showinfo("Proveedores", mensaje)
            self.cargar_datos()
            self._limpiar_formulario()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def abrir_popup_compra(self):
        if not self.proveedores_cache:
            messagebox.showerror("Error", "Primero debe registrar al menos un proveedor")
            return
        if not self.productos_cache:
            messagebox.showerror("Error", "Primero debe registrar al menos un producto en inventario")
            return
        PopupCompraProveedor(
            self,
            self.compra_controller,
            self.proveedores_cache,
            self.productos_cache,
            self._on_compra_registrada,
        )

    def _on_compra_registrada(self):
        self.cargar_datos()

    def _limpiar_formulario(self):
        self.proveedor_seleccionado_id = None
        for entry in (self.nombre, self.contacto, self.telefono, self.direccion):
            entry.delete(0, tk.END)


class PopupCompraProveedor(tk.Toplevel):
    def __init__(self, master, controller, proveedores, productos, on_success):
        super().__init__(master)
        self.controller = controller
        self.proveedores = proveedores
        self.productos = productos
        self.on_success = on_success
        self.title("Registrar compra a proveedor")
        self.configure(bg=CRM_THEME["panel"])
        self.transient(master.winfo_toplevel())
        self.grab_set()
        self.resizable(False, False)
        self._crear_ui()

    def _crear_ui(self):
        container = tk.Frame(self, bg=CRM_THEME["panel"], padx=20, pady=20)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)

        tk.Label(container, text="Proveedor", bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.proveedor_var = tk.StringVar()
        self.proveedor_combo = ttk.Combobox(
            container,
            textvariable=self.proveedor_var,
            values=[proveedor.nombre for proveedor in self.proveedores],
            style="CRM.TCombobox",
        )
        self.proveedor_combo.grid(row=1, column=0, sticky="ew")
        self.proveedor_combo.bind("<KeyRelease>", self._filtrar_proveedores)

        tk.Label(container, text="Producto", bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=2, column=0, sticky="w", pady=(10, 6))
        self.producto_var = tk.StringVar()
        self.producto_combo = ttk.Combobox(
            container,
            textvariable=self.producto_var,
            values=[producto.nombre for producto in self.productos],
            style="CRM.TCombobox",
        )
        self.producto_combo.grid(row=3, column=0, sticky="ew")
        self.producto_combo.bind("<KeyRelease>", self._filtrar_productos)

        self.cantidad_entry = self._field(container, "Cantidad", 2)
        self.tipo_entry = self._field(container, "Tipo producto", 3)
        self.fecha_hora_entry = self._field(container, "Fecha y hora", 4)
        self.fecha_hora_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.fecha_hora_entry.configure(state="readonly")
        self.fecha_vencimiento_entry = self._field(container, "Fecha vencimiento (YYYY-MM-DD)", 5)

        ttk.Button(container, text="Confirmar compra", command=self.confirmar_compra, style="CRMPrimary.TButton").grid(row=12, column=0, sticky="ew", pady=(16, 0))

    def _field(self, parent, label, row):
        tk.Label(parent, text=label, bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=row * 2, column=0, sticky="w", pady=(10, 6))
        entry = ttk.Entry(parent, style="CRM.TEntry")
        entry.grid(row=row * 2 + 1, column=0, sticky="ew")
        return entry

    def _filtrar_proveedores(self, _event=None):
        texto = self.proveedor_var.get().lower().strip()
        coincidencias = [proveedor.nombre for proveedor in self.proveedores if texto in proveedor.nombre.lower()]
        self.proveedor_combo["values"] = coincidencias or [proveedor.nombre for proveedor in self.proveedores]

    def _filtrar_productos(self, _event=None):
        texto = self.producto_var.get().lower().strip()
        coincidencias = [producto.nombre for producto in self.productos if texto in producto.nombre.lower()]
        self.producto_combo["values"] = coincidencias or [producto.nombre for producto in self.productos]

    def confirmar_compra(self):
        try:
            proveedor = self._buscar_proveedor_por_nombre(self.proveedor_var.get().strip())
            producto = self._buscar_producto_por_nombre(self.producto_var.get().strip())
            if not proveedor:
                raise ValueError("Debe seleccionar un proveedor valido")
            if not producto:
                raise ValueError("Debe seleccionar un producto valido")
            _, mensaje = self.controller.registrar_compra(
                proveedor.id_proveedor,
                producto.id_producto,
                self.cantidad_entry.get().strip(),
                self.tipo_entry.get().strip(),
                self.fecha_vencimiento_entry.get().strip(),
            )
            messagebox.showinfo("Compras", mensaje)
            self.on_success()
            self.destroy()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _buscar_proveedor_por_nombre(self, nombre):
        for proveedor in self.proveedores:
            if proveedor.nombre.lower() == nombre.lower():
                return proveedor
        return None

    def _buscar_producto_por_nombre(self, nombre):
        for producto in self.productos:
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None
