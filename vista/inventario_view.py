import tkinter as tk
from tkinter import messagebox, ttk

from controller.producto_controller import ProductoController
from vista.theme import CRM_THEME, build_styles


class InventarioView(tk.Frame):
    def __init__(self, master=None):
        build_styles()
        super().__init__(master, bg=CRM_THEME["mist"], padx=20, pady=20)
        self.controller = ProductoController()
        self.pack(fill="both", expand=True)
        self._crear_ui()
        self.cargar_datos()

    def _crear_ui(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        header = tk.Frame(self, bg=CRM_THEME["mist"])
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        tk.Label(header, text="Inventario", font=("Segoe UI Semibold", 26), bg=CRM_THEME["mist"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(header, text="Catalogo, existencias y actualizacion de productos", font=("Segoe UI", 10), bg=CRM_THEME["mist"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 0))

        left = tk.Frame(self, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        right = tk.Frame(self, bg=CRM_THEME["panel"], highlightbackground=CRM_THEME["line"], highlightthickness=1)
        right.grid(row=1, column=1, sticky="nsew")
        canvas = tk.Canvas(right, bg=CRM_THEME["panel"], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=CRM_THEME["panel"], padx=18, pady=18)
        content.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        content.bind(
            "<Enter>",
            lambda _event: canvas.bind_all(
                "<MouseWheel>",
                lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
            ),
        )
        content.bind("<Leave>", lambda _event: canvas.unbind_all("<MouseWheel>"))

        tk.Label(left, text="Listado de productos", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(left, text="Visualiza precios, stock y seccion con un formato limpio para operacion diaria.", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 10))

        search_bar = tk.Frame(left, bg=CRM_THEME["panel"])
        search_bar.pack(fill="x", pady=(0, 12))
        self.filtro = ttk.Entry(search_bar, style="CRM.TEntry")
        self.filtro.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(search_bar, text="Buscar", command=self.buscar, style="CRMOutline.TButton").pack(side="left")
        ttk.Button(search_bar, text="Recargar", command=self.cargar_datos, style="CRMSecondary.TButton").pack(side="left", padx=(8, 0))

        cols = ("codigo", "nombre", "precio", "cantidad", "seccion")
        self.tabla = ttk.Treeview(left, columns=cols, show="headings", style="CRM.Treeview")
        widths = {"codigo": 120, "nombre": 240, "precio": 110, "cantidad": 100, "seccion": 140}
        for col in cols:
            self.tabla.heading(col, text=col.title())
            self.tabla.column(col, width=widths[col], anchor="center")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._cargar_seleccion)

        tk.Label(content, text="Panel de edicion", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(content, text="Alta y edicion del catalogo.", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 10))

        form = tk.Frame(content, bg=CRM_THEME["panel"])
        form.pack(fill="x", anchor="n")
        self.codigo = self._field(form, "Codigo", 0)
        self.nombre = self._field(form, "Nombre", 1)
        self.precio = self._field(form, "Precio", 2)
        self.cantidad = self._field(form, "Cantidad", 3)
        tk.Label(form, text="Seccion", bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=8, column=0, sticky="w", pady=(12, 6))
        self.seccion = ttk.Combobox(form, values=["Golosinas", "Lacteos", "Limpieza", "Bebidas", "Panaderia", "Otro"], style="CRM.TCombobox", state="readonly")
        self.seccion.grid(row=9, column=0, sticky="ew")
        self.seccion.current(0)
        form.columnconfigure(0, weight=1)

        actions = tk.Frame(content, bg=CRM_THEME["panel"])
        actions.pack(fill="x", side="bottom", pady=(14, 0))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)
        ttk.Button(actions, text="Agregar producto", command=self.agregar, style="CRMPrimary.TButton").grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=4)
        ttk.Button(actions, text="Actualizar producto", command=self.actualizar, style="CRMSecondary.TButton").grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=4)
        ttk.Button(actions, text="Eliminar seleccionado", command=self.eliminar, style="CRMOutline.TButton").grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=4)
        ttk.Button(actions, text="Limpiar formulario", command=self._limpiar, style="CRMOutline.TButton").grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=4)

    def _field(self, parent, label, row):
        tk.Label(parent, text=label, bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=row * 2, column=0, sticky="w", pady=(0 if row == 0 else 12, 6))
        entry = ttk.Entry(parent, style="CRM.TEntry")
        entry.grid(row=row * 2 + 1, column=0, sticky="ew")
        return entry

    def _filas(self, productos):
        return [(producto.codigo, producto.nombre, f"{producto.precio:.2f}", producto.stock, producto.seccion or "") for producto in productos]

    def cargar_datos(self):
        self._poblar(self._filas(self.controller.listar()))

    def _poblar(self, filas):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for fila in filas:
            self.tabla.insert("", "end", values=fila)

    def _cargar_seleccion(self, _event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        codigo, nombre, precio, cantidad, seccion = self.tabla.item(seleccion[0], "values")
        for entry, value in ((self.codigo, codigo), (self.nombre, nombre), (self.precio, precio), (self.cantidad, cantidad)):
            entry.delete(0, tk.END)
            entry.insert(0, value)
        self.seccion.set(seccion)

    def agregar(self):
        try:
            _, mensaje = self.controller.crear(self.codigo.get().strip(), self.nombre.get().strip(), self.precio.get().strip(), self.cantidad.get().strip(), self.seccion.get().strip())
            messagebox.showinfo("Inventario", mensaje)
            self.cargar_datos()
            self._limpiar()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def actualizar(self):
        try:
            _, mensaje = self.controller.actualizar(self.codigo.get().strip(), self.nombre.get().strip(), self.precio.get().strip(), self.cantidad.get().strip(), self.seccion.get().strip())
            messagebox.showinfo("Inventario", mensaje)
            self.cargar_datos()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        codigo = self.tabla.item(seleccion[0], "values")[0]
        try:
            _, mensaje = self.controller.eliminar(codigo)
            messagebox.showinfo("Inventario", mensaje)
            self.cargar_datos()
            self._limpiar()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def buscar(self):
        filtro = self.filtro.get().strip()
        productos = self.controller.buscar(filtro) if filtro else self.controller.listar()
        self._poblar(self._filas(productos))

    def _limpiar(self):
        for entry in (self.codigo, self.nombre, self.precio, self.cantidad, self.filtro):
            entry.delete(0, tk.END)
        self.seccion.current(0)
