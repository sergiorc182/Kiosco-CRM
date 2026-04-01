import tkinter as tk
from tkinter import messagebox, ttk

from controller.turno_controller import TurnoController
from vista.theme import CRM_THEME, build_styles


class TurnoView(tk.Frame):
    DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

    def __init__(self, master=None, rol="empleado", usuario=None, usuario_id=None, empleado_actual=None):
        build_styles()
        super().__init__(master, bg=CRM_THEME["mist"], padx=20, pady=20)
        self.controller = TurnoController()
        self.rol = rol
        self.usuario = usuario
        self.usuario_id = usuario_id
        self.empleado_actual = empleado_actual
        self._empleados = {}
        self.pack(fill="both", expand=True)
        self._crear_ui()
        self.bind_all("<<UsuariosActualizados>>", self._on_usuarios_actualizados)
        self.refrescar_empleados()
        self.cargar_turnos()
        self._aplicar_permisos()

    def destroy(self):
        self.unbind_all("<<UsuariosActualizados>>")
        super().destroy()

    def _crear_ui(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        header = tk.Frame(self, bg=CRM_THEME["mist"])
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        tk.Label(header, text="Turnos", font=("Segoe UI Semibold", 26), bg=CRM_THEME["mist"], fg=CRM_THEME["navy"]).pack(anchor="w")
        header_text = "Planificacion del equipo con una vista operativa clara y profesional."
        if self.rol == "empleado":
            header_text = "Selecciona tu turno asignado y comienza la jornada para habilitar el sistema."
        tk.Label(header, text=header_text, font=("Segoe UI", 10), bg=CRM_THEME["mist"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 0))

        left = tk.Frame(self, bg=CRM_THEME["panel"], highlightbackground=CRM_THEME["line"], highlightthickness=1)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        right = tk.Frame(self, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        right.grid(row=1, column=1, sticky="nsew")

        canvas = tk.Canvas(left, bg=CRM_THEME["panel"], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=CRM_THEME["panel"], padx=18, pady=18)
        content.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        content.bind("<Enter>", lambda _event: canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")))
        content.bind("<Leave>", lambda _event: canvas.unbind_all("<MouseWheel>"))
        content.grid_columnconfigure(0, weight=1)

        tk.Label(content, text="Gestion de turnos", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        subtitle = "Asigna personal, horario y dia."
        if self.rol == "empleado":
            subtitle = "Visualiza tus turnos asignados y comienza el correspondiente."
        tk.Label(content, text=subtitle, font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 10))

        form = tk.Frame(content, bg=CRM_THEME["panel"])
        form.pack(fill="x", anchor="n")
        self.tipo_turno = self._combo_field(form, "Tipo de turno", ["Manana", "Tarde", "Noche"], 0)
        self.hora_inicio = self._entry_field(form, "Hora inicio (HH:MM)", 1)
        self.hora_fin = self._entry_field(form, "Hora fin (HH:MM)", 2)
        self.empleado = self._combo_field(form, "Empleado", [], 3)
        self.dia = self._combo_field(form, "Dia", self.DIAS, 4)
        self.dia.current(0)

        actions = tk.Frame(content, bg=CRM_THEME["panel"])
        actions.pack(fill="x", pady=(14, 0))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)
        self.btn_crear = ttk.Button(actions, text="Crear turno", command=self.crear_turno, style="CRMPrimary.TButton")
        self.btn_crear.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=4)
        self.btn_editar = ttk.Button(actions, text="Editar turno", command=self.editar_turno, style="CRMSecondary.TButton")
        self.btn_editar.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=4)
        self.btn_eliminar = ttk.Button(actions, text="Eliminar turno", command=self.eliminar_turno, style="CRMOutline.TButton")
        self.btn_eliminar.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=4)
        self.btn_comenzar = ttk.Button(actions, text="Comenzar turno", command=self.comenzar_turno, style="CRMSecondary.TButton")
        self.btn_comenzar.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=4)
        self.btn_cerrar = ttk.Button(actions, text="Cerrar turno", command=self.cerrar_turno, style="CRMOutline.TButton")
        self.btn_cerrar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4)

        tk.Label(right, text="Agenda operativa", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(right, text="Consulta todos los turnos cargados y selecciona uno para editar o ejecutar acciones.", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 12))
        cols = ("id", "turno", "inicio", "fin", "empleado", "fecha")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", style="CRM.Treeview")
        widths = {"id": 70, "turno": 140, "inicio": 100, "fin": 100, "empleado": 220, "fecha": 120}
        for col in cols:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=widths[col], anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._cargar_seleccion)

    def _entry_field(self, parent, label, row):
        tk.Label(parent, text=label, bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=row * 2, column=0, sticky="w", pady=(0 if row == 0 else 12, 6))
        entry = ttk.Entry(parent, style="CRM.TEntry")
        entry.grid(row=row * 2 + 1, column=0, sticky="ew")
        parent.columnconfigure(0, weight=1)
        return entry

    def _combo_field(self, parent, label, values, row):
        tk.Label(parent, text=label, bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=row * 2, column=0, sticky="w", pady=(0 if row == 0 else 12, 6))
        combo = ttk.Combobox(parent, values=values, state="readonly", style="CRM.TCombobox")
        combo.grid(row=row * 2 + 1, column=0, sticky="ew")
        if values:
            combo.current(0)
        parent.columnconfigure(0, weight=1)
        return combo

    def _aplicar_permisos(self):
        es_admin = self.rol == "admin"
        form_state = "readonly" if es_admin else "disabled"
        self.tipo_turno.config(state=form_state)
        self.empleado.config(state=form_state)
        self.dia.config(state=form_state)
        self.hora_inicio.config(state="normal" if es_admin else "disabled")
        self.hora_fin.config(state="normal" if es_admin else "disabled")
        self.btn_crear.config(state="normal" if es_admin else "disabled")
        self.btn_editar.config(state="normal" if es_admin else "disabled")
        self.btn_eliminar.config(state="normal" if es_admin else "disabled")

    def refrescar_empleados(self):
        empleados = self.controller.listar_empleados()
        self._empleados = {row["nombre"]: row["id_empleado"] for row in empleados}
        if self.rol == "admin":
            self.empleado["values"] = list(self._empleados.keys())
            if empleados:
                self.empleado.current(0)
        elif self.empleado_actual:
            nombre = self.empleado_actual["nombre"]
            self.empleado["values"] = [nombre]
            self.empleado.set(nombre)

    def cargar_turnos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = self.controller.listar_turnos() if self.rol == "admin" else self.controller.listar_turnos_por_usuario(self.usuario_id)
        for row in rows:
            self.tree.insert("", "end", values=(row["id_turno"], row["nombre_turno"], row["hora_inicio"], row["hora_fin"], row["empleado"], row["fecha"]))

    def _datos_form(self):
        return (self.tipo_turno.get(), f"{self.hora_inicio.get().strip()}:00", f"{self.hora_fin.get().strip()}:00", self._empleados[self.empleado.get()], self.dia.get())

    def crear_turno(self):
        try:
            self.controller.crear_turno(*self._datos_form())
            messagebox.showinfo("Turnos", "Turno creado correctamente")
            self.cargar_turnos()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def editar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        turno_id = self.tree.item(seleccion[0], "values")[0]
        try:
            self.controller.editar_turno(turno_id, *self._datos_form())
            messagebox.showinfo("Turnos", "Turno actualizado correctamente")
            self.cargar_turnos()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def eliminar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        turno_id = self.tree.item(seleccion[0], "values")[0]
        try:
            self.controller.eliminar_turno(turno_id)
            messagebox.showinfo("Turnos", "Turno eliminado correctamente")
            self.cargar_turnos()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def comenzar_turno(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Turnos", "Selecciona un turno para comenzar.")
            return
        values = self.tree.item(seleccion[0], "values")
        if self.rol == "empleado" and self.empleado_actual and values[4] != self.empleado_actual["nombre"]:
            messagebox.showerror("Error", "Solo puedes comenzar tu turno asignado.")
            return
        payload = {"id_turno": values[0], "nombre_turno": values[1], "hora_inicio": values[2], "hora_fin": values[3], "empleado": values[4], "fecha": values[5]}
        try:
            activo = self.controller.comenzar_turno(payload)
            self.event_generate("<<TurnoEstadoActualizado>>", when="tail")
            messagebox.showinfo("Turnos", f"Turno iniciado para {activo['empleado']}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def cerrar_turno(self):
        activo = self.controller.obtener_turno_activo()
        if self.rol == "empleado" and self.empleado_actual and activo and activo.get("empleado") != self.empleado_actual["nombre"]:
            messagebox.showerror("Error", "Solo puedes cerrar tu turno activo.")
            return
        try:
            cierre = self.controller.cerrar_turno()
            self.event_generate("<<TurnoEstadoActualizado>>", when="tail")
            messagebox.showinfo("Turnos", f"Turno cerrado. Horas trabajadas: {cierre['horas']:.2f}")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _cargar_seleccion(self, _event=None):
        if self.rol != "admin":
            return
        seleccion = self.tree.selection()
        if not seleccion:
            return
        _, turno, inicio, fin, empleado, _fecha = self.tree.item(seleccion[0], "values")
        self.tipo_turno.set(turno)
        self.hora_inicio.delete(0, tk.END)
        self.hora_inicio.insert(0, str(inicio)[:5])
        self.hora_fin.delete(0, tk.END)
        self.hora_fin.insert(0, str(fin)[:5])
        self.empleado.set(empleado)

    def _on_usuarios_actualizados(self, _event=None):
        if self.winfo_exists():
            self.refrescar_empleados()
