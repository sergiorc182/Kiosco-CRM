import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from controller.caja_controller import CajaController
from vista.theme import CRM_THEME, build_styles


class CajaView(tk.Frame):
    def __init__(self, master=None):
        build_styles()
        super().__init__(master, bg=CRM_THEME["mist"], padx=20, pady=20)
        self.controller = CajaController()
        self.pack(fill="both", expand=True)
        self._crear_ui()
        self._refrescar_estado()

    def _crear_ui(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        header = tk.Frame(self, bg=CRM_THEME["mist"])
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        tk.Label(header, text="Caja", font=("Segoe UI Semibold", 26), bg=CRM_THEME["mist"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(header, text="Control simple de apertura, movimientos y cierre.", font=("Segoe UI", 10), bg=CRM_THEME["mist"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 0))

        left = tk.Frame(self, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        right = tk.Frame(self, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        right.grid(row=1, column=1, sticky="nsew")

        tk.Label(left, text="Control de caja", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(left, text="El monto de apertura solo se usa para abrir. El monto de cierre solo se usa para cerrar. El motivo se usa solo en ingresos, retiros y gastos.", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"], wraplength=290, justify="left").pack(anchor="w", pady=(4, 12))

        form = tk.Frame(left, bg=CRM_THEME["panel"])
        form.pack(fill="x")
        self.monto_apertura = self._field(form, "Monto de apertura", 0)
        self.monto_apertura.insert(0, "0")
        self.monto_cierre = self._field(form, "Monto de cierre", 1)
        self.motivo = self._field(form, "Motivo", 2)
        self.motivo.insert(0, "Movimiento manual")
        form.columnconfigure(0, weight=1)

        actions = tk.Frame(left, bg=CRM_THEME["panel"])
        actions.pack(fill="x", pady=(16, 0))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)
        self.btn_abrir = ttk.Button(actions, text="Abrir caja", command=self.abrir, style="CRMPrimary.TButton")
        self.btn_abrir.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=4)
        self.btn_ingreso = ttk.Button(actions, text="Ingreso", command=self.ingreso, style="CRMSecondary.TButton")
        self.btn_ingreso.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=4)
        self.btn_retiro = ttk.Button(actions, text="Retiro", command=self.retiro, style="CRMOutline.TButton")
        self.btn_retiro.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=4)
        self.btn_gasto = ttk.Button(actions, text="Gasto", command=self.gasto, style="CRMOutline.TButton")
        self.btn_gasto.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=4)
        self.btn_cerrar = ttk.Button(actions, text="Cerrar caja", command=self.cerrar, style="CRMPrimary.TButton")
        self.btn_cerrar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4)

        tk.Label(right, text="Estado de la caja", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(right, text="El saldo se actualiza con movimientos manuales y ventas del POS mientras la caja esta abierta.", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"], wraplength=320, justify="left").pack(anchor="w", pady=(4, 12))

        stats = tk.Frame(right, bg=CRM_THEME["panel"])
        stats.pack(fill="x")
        self.estado_label = self._stat(stats, "Estado", "-")
        self.estado_label.pack(fill="x", pady=4)
        self.saldo_label = self._stat(stats, "Saldo", "$ 0.00")
        self.saldo_label.pack(fill="x", pady=4)
        self.apertura_label = self._stat(stats, "Monto de apertura", "$ 0.00")
        self.apertura_label.pack(fill="x", pady=4)

        tk.Label(right, text="Movimientos", font=("Segoe UI Semibold", 13), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w", pady=(18, 8))
        self.movimientos = tk.Listbox(right, height=12, bd=0, highlightthickness=1, highlightbackground=CRM_THEME["line"])
        self.movimientos.pack(fill="both", expand=True)

    def _field(self, parent, label, row):
        tk.Label(parent, text=label, bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=row * 2, column=0, sticky="w", pady=(0 if row == 0 else 12, 6))
        entry = ttk.Entry(parent, style="CRM.TEntry")
        entry.grid(row=row * 2 + 1, column=0, sticky="ew")
        return entry

    def _stat(self, parent, title, value):
        card = tk.Frame(parent, bg=CRM_THEME["panel_alt"], padx=14, pady=12, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        tk.Label(card, text=title, font=("Segoe UI", 9), bg=CRM_THEME["panel_alt"], fg=CRM_THEME["muted"]).pack(anchor="w")
        value_label = tk.Label(card, text=value, font=("Segoe UI Semibold", 18), bg=CRM_THEME["panel_alt"], fg=CRM_THEME["navy"])
        value_label.pack(anchor="w", pady=(6, 0))
        card.value_label = value_label
        return card

    def _float_value(self, entry, default=None):
        raw = entry.get().strip()
        if not raw and default is not None:
            return float(default)
        return float(raw.replace(",", "."))

    def _set_entry_state(self, entry, enabled):
        entry.config(state="normal" if enabled else "disabled")

    def _pedir_monto_movimiento(self, tipo):
        return simpledialog.askfloat(
            "Caja",
            f"Ingrese el monto para {tipo.lower()}",
            parent=self.winfo_toplevel(),
            minvalue=0.01,
        )

    def _registrar_movimiento(self, tipo, callback, ok_message):
        try:
            motivo = self.motivo.get().strip()
            if not motivo:
                raise ValueError("Ingrese un motivo para el movimiento")
            monto = self._pedir_monto_movimiento(tipo)
            if monto is None:
                return
            callback(monto, motivo)
            self._refrescar_estado()
            self.motivo.delete(0, tk.END)
            self.motivo.insert(0, "Movimiento manual")
            messagebox.showinfo("Caja", ok_message)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _refrescar_estado(self):
        estado = self.controller.obtener_estado()
        abierta = estado["abierta"]
        self.estado_label.value_label.config(text="Abierta" if abierta else "Cerrada")
        self.saldo_label.value_label.config(text=f"$ {estado['saldo']:.2f}")
        self.apertura_label.value_label.config(text=f"$ {estado['monto_apertura']:.2f}")

        self._set_entry_state(self.monto_apertura, not abierta)
        self._set_entry_state(self.monto_cierre, abierta)
        self._set_entry_state(self.motivo, abierta)

        self.btn_abrir.config(state="normal" if not abierta else "disabled")
        movimientos_habilitados = "normal" if abierta else "disabled"
        self.btn_ingreso.config(state=movimientos_habilitados)
        self.btn_retiro.config(state=movimientos_habilitados)
        self.btn_gasto.config(state=movimientos_habilitados)
        self.btn_cerrar.config(state=movimientos_habilitados)

        if not abierta:
            self.monto_cierre.delete(0, tk.END)
        else:
            self.monto_apertura.delete(0, tk.END)
            self.monto_apertura.insert(0, f"{estado['monto_apertura']:.2f}")

        self.movimientos.delete(0, tk.END)
        movimientos_visibles = [mov for mov in estado["movimientos"] if mov["tipo"] in ("ingreso", "retiro", "gasto")]
        if not movimientos_visibles:
            self.movimientos.insert(tk.END, "Sin movimientos manuales")
            return
        for mov in movimientos_visibles:
            descripcion = f" - {mov['descripcion']}" if mov.get("descripcion") else ""
            self.movimientos.insert(
                tk.END,
                f"{mov['fecha']} | {mov['tipo']} | ${mov['monto']:.2f}{descripcion}",
            )

    def abrir(self):
        try:
            self.controller.abrir(self._float_value(self.monto_apertura, default=0))
            self._refrescar_estado()
            messagebox.showinfo("Caja", "Caja abierta correctamente")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def ingreso(self):
        self._registrar_movimiento("Ingreso", self.controller.ingreso, "Ingreso registrado")

    def retiro(self):
        self._registrar_movimiento("Retiro", self.controller.retiro, "Retiro registrado")

    def gasto(self):
        self._registrar_movimiento("Gasto", self.controller.gasto, "Gasto registrado")

    def cerrar(self):
        try:
            resumen = self.controller.cerrar(self._float_value(self.monto_cierre, default=0))
            self._refrescar_estado()
            messagebox.showinfo("Caja", f"Caja cerrada. Diferencia: {resumen['diferencia']:.2f}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
