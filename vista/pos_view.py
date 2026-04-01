import tkinter as tk
from tkinter import messagebox, ttk

from controller.caja_controller import CajaController
from controller.producto_controller import ProductoController
from controller.venta_controller import VentaController
from vista.theme import CRM_THEME, build_styles


class POSView(tk.Frame):
    def __init__(self, master=None):
        build_styles()
        super().__init__(master, bg=CRM_THEME["mist"], padx=20, pady=20)
        self.caja_controller = CajaController()
        self.producto_controller = ProductoController()
        self.venta_controller = VentaController(caja_service=self.caja_controller.service, producto_service=self.producto_controller.service)
        self.pack(fill="both", expand=True)
        self._crear_ui()

    def _crear_ui(self):
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        header = tk.Frame(self, bg=CRM_THEME["mist"])
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        tk.Label(header, text="Punto de Venta", font=("Segoe UI Semibold", 26), bg=CRM_THEME["mist"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(header, text="Experiencia de cobro rapida", font=("Segoe UI", 10), bg=CRM_THEME["mist"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 0))

        left = tk.Frame(self, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        right = tk.Frame(self, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        right.grid(row=1, column=1, sticky="nsew")

        top_form = tk.Frame(left, bg=CRM_THEME["panel"])
        top_form.pack(fill="x", pady=(0, 14))
        tk.Label(top_form, text="Cliente", bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=0, column=0, sticky="w")
        self.cliente_var = tk.StringVar(value="CONSUMIDOR FINAL")
        ttk.Entry(top_form, textvariable=self.cliente_var, style="CRM.TEntry").grid(row=1, column=0, sticky="ew", padx=(0, 10))
        tk.Label(top_form, text="Codigo", bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=0, column=1, sticky="w")
        self.codigo_entry = ttk.Entry(top_form, style="CRM.TEntry")
        self.codigo_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        self.codigo_entry.bind("<Return>", lambda _e: self.buscar_y_agregar())
        tk.Label(top_form, text="Cantidad", bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=0, column=2, sticky="w")
        self.cantidad_var = tk.IntVar(value=1)
        tk.Spinbox(top_form, from_=1, to=999, textvariable=self.cantidad_var, width=8, relief="solid", bd=1, highlightthickness=0, bg="white", fg=CRM_THEME["text"]).grid(row=1, column=2, sticky="ew", padx=(0, 10))
        ttk.Button(top_form, text="Agregar producto", command=self.buscar_y_agregar, style="CRMPrimary.TButton").grid(row=1, column=3, sticky="ew")
        top_form.columnconfigure(0, weight=2)
        top_form.columnconfigure(1, weight=2)
        top_form.columnconfigure(2, weight=1)
        top_form.columnconfigure(3, weight=1)

        metrics = tk.Frame(left, bg=CRM_THEME["panel"])
        metrics.pack(fill="x", pady=(0, 14))
        self.total_card = self._metric_card(metrics, "Total actual", "$ 0.00", CRM_THEME["coral"])
        self.total_card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.items_card = self._metric_card(metrics, "Items cargados", "0", CRM_THEME["navy"])
        self.items_card.pack(side="left", fill="x", expand=True)

        cols = ("codigo", "descripcion", "cantidad", "precio", "subtotal")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", style="CRM.Treeview")
        widths = {"codigo": 110, "descripcion": 270, "cantidad": 90, "precio": 100, "subtotal": 110}
        for col in cols:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=widths[col], anchor="center")
        self.tree.pack(fill="both", expand=True)

        tk.Label(right, text="Acciones de caja", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(right, text="Controla el cierre de la venta, el metodo de cobro y ajustes rapidos desde un panel lateral.", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"], wraplength=260, justify="left").pack(anchor="w", pady=(4, 14))

        actions = tk.Frame(right, bg=CRM_THEME["panel"])
        actions.pack(fill="x")
        ttk.Button(actions, text="Eliminar producto", command=self.eliminar_producto, style="CRMOutline.TButton").pack(fill="x", pady=5)
        ttk.Button(actions, text="Modificar cantidad", command=self.modificar_cantidad, style="CRMSecondary.TButton").pack(fill="x", pady=5)

        tk.Label(right, text="Metodo de pago", bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).pack(anchor="w", pady=(18, 6))
        self.metodo_pago = ttk.Combobox(right, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly", width=20, style="CRM.TCombobox")
        self.metodo_pago.pack(fill="x")
        self.metodo_pago.current(0)

        footer = tk.Frame(right, bg=CRM_THEME["panel"], padx=16, pady=16, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        footer.pack(fill="x", pady=(20, 0))
        tk.Label(footer, text="Cierre de venta", font=("Segoe UI Semibold", 13), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(footer, text="Toda venta confirmada impacta en inventario y caja automaticamente.", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"], wraplength=240, justify="left").pack(anchor="w", pady=(4, 12))
        ttk.Button(footer, text="Confirmar venta", command=self.confirmar_venta, style="CRMPrimary.TButton").pack(fill="x")

    def _metric_card(self, parent, title, value, accent):
        card = tk.Frame(parent, bg=CRM_THEME["panel_alt"], padx=16, pady=14, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        tk.Label(card, text=title, font=("Segoe UI", 9), bg=CRM_THEME["panel_alt"], fg=CRM_THEME["muted"]).pack(anchor="w")
        value_label = tk.Label(card, text=value, font=("Segoe UI Semibold", 20), bg=CRM_THEME["panel_alt"], fg=accent)
        value_label.pack(anchor="w", pady=(8, 0))
        card.value_label = value_label
        return card

    def _refrescar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for detalle in self.venta_controller.listar_items():
            producto = self.producto_controller.service.obtener_producto_por_id(detalle.id_producto)
            self.tree.insert("", "end", values=(producto.codigo, detalle.producto, detalle.cantidad, f"{detalle.precio:.2f}", f"{detalle.subtotal():.2f}"))
        self.total_card.value_label.config(text=f"$ {self.venta_controller.total():.2f}")
        self.items_card.value_label.config(text=str(len(self.venta_controller.listar_items())))

    def buscar_y_agregar(self):
        try:
            if self.venta_controller.venta.cliente != self.cliente_var.get().strip():
                self.venta_controller.venta.cliente = self.cliente_var.get().strip() or "CONSUMIDOR FINAL"
            producto = self.producto_controller.obtener_por_codigo(self.codigo_entry.get().strip())
            self.venta_controller.agregar_producto(producto, self.cantidad_var.get())
            self.codigo_entry.delete(0, tk.END)
            self.cantidad_var.set(1)
            self._refrescar_tabla()
        except Exception as exc:
            messagebox.showerror("POS", str(exc))

    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        self.venta_controller.eliminar_item(self.tree.index(seleccion[0]))
        self._refrescar_tabla()

    def modificar_cantidad(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        indice = self.tree.index(seleccion[0])
        ventana = tk.Toplevel(self)
        ventana.title("Modificar cantidad")
        ventana.geometry("280x170")
        ventana.configure(bg=CRM_THEME["mist"])
        panel = tk.Frame(ventana, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=12, pady=12)
        tk.Label(panel, text="Nueva cantidad", font=("Segoe UI Semibold", 13), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        cantidad_entry = ttk.Entry(panel, style="CRM.TEntry", justify="center")
        cantidad_entry.pack(fill="x", pady=14)
        cantidad_entry.focus_set()

        def guardar():
            try:
                self.venta_controller.actualizar_cantidad(indice, int(cantidad_entry.get().strip()))
                self._refrescar_tabla()
                ventana.destroy()
            except Exception as exc:
                messagebox.showerror("POS", str(exc))

        ttk.Button(panel, text="Guardar", command=guardar, style="CRMPrimary.TButton").pack(fill="x")

    def confirmar_venta(self):
        try:
            monto_recibido = None
            if self.metodo_pago.get() == "Efectivo":
                monto_recibido = self._pedir_monto_efectivo()
                if monto_recibido is None:
                    return
            resultado = self.venta_controller.confirmar(self.metodo_pago.get(), monto_recibido=monto_recibido)
            self._refrescar_tabla()
            messagebox.showinfo("POS", f"Venta confirmada. Total: ${resultado['total']:.2f}. Vuelto: ${resultado['vuelto']:.2f}")
        except Exception as exc:
            messagebox.showerror("POS", str(exc))

    def _pedir_monto_efectivo(self):
        dialog = tk.Toplevel(self)
        dialog.title("Cobro en efectivo")
        dialog.geometry("320x210")
        dialog.configure(bg=CRM_THEME["mist"])
        panel = tk.Frame(dialog, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=12, pady=12)
        tk.Label(panel, text="Cobro en efectivo", font=("Segoe UI Semibold", 15), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(panel, text=f"Total a cobrar: ${self.venta_controller.total():.2f}", font=("Segoe UI", 10), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 12))
        entry = ttk.Entry(panel, style="CRM.TEntry", justify="center")
        entry.pack(fill="x")
        entry.insert(0, f"{self.venta_controller.total():.2f}")
        result = {"value": None}

        def confirmar():
            try:
                result["value"] = float(entry.get().replace(",", "."))
                dialog.destroy()
            except ValueError:
                messagebox.showerror("POS", "Monto invalido")

        ttk.Button(panel, text="Confirmar cobro", command=confirmar, style="CRMPrimary.TButton").pack(fill="x", pady=(14, 0))
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        self.wait_window(dialog)
        return result["value"]
