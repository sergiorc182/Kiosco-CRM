import tkinter as tk
from tkinter import messagebox, ttk

from controller.usuario_controller import UsuarioController
from vista.theme import CRM_THEME, build_styles


class UsuarioView(tk.Frame):
    def __init__(self, master=None):
        build_styles()
        super().__init__(master, bg=CRM_THEME["mist"], padx=20, pady=20)
        self.controller = UsuarioController()
        self.pack(fill="both", expand=True)
        self._crear_ui()
        self.cargar_usuarios()

    def _crear_ui(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        header = tk.Frame(self, bg=CRM_THEME["mist"])
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        tk.Label(header, text="Usuarios", font=("Segoe UI Semibold", 26), bg=CRM_THEME["mist"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(header, text="Administracion de accesos y perfiles", font=("Segoe UI", 10), bg=CRM_THEME["mist"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 0))

        left = tk.Frame(self, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        right = tk.Frame(self, bg=CRM_THEME["panel"], padx=18, pady=18, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        right.grid(row=1, column=1, sticky="nsew")

        tk.Label(left, text="Nuevo usuario", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(left, text="Carga credenciales y define el tipo de acceso desde un formulario", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"], wraplength=280, justify="left").pack(anchor="w", pady=(4, 14))

        form = tk.Frame(left, bg=CRM_THEME["panel"])
        form.pack(fill="x")
        self.usuario = self._field(form, "Usuario", 0)
        self.password = self._field(form, "Contraseña", 1, show="*")
        tk.Label(form, text="Tipo", bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=4, column=0, sticky="w", pady=(12, 6))
        self.tipo = ttk.Combobox(form, values=["admin", "empleado"], state="readonly", style="CRM.TCombobox")
        self.tipo.grid(row=5, column=0, sticky="ew")
        self.tipo.current(1)
        self.nombre_real = self._field(form, "Nombre real", 3)
        form.columnconfigure(0, weight=1)

        actions = tk.Frame(left, bg=CRM_THEME["panel"])
        actions.pack(fill="x", pady=(18, 0))
        ttk.Button(actions, text="Crear usuario", command=self.crear_usuario, style="CRMPrimary.TButton").pack(fill="x", pady=5)
        ttk.Button(actions, text="Limpiar formulario", command=self._limpiar, style="CRMOutline.TButton").pack(fill="x", pady=5)

        metrics = tk.Frame(left, bg=CRM_THEME["panel"])
        metrics.pack(fill="x", pady=(18, 0))
        stat = tk.Frame(metrics, bg=CRM_THEME["panel_alt"], padx=16, pady=14, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        stat.pack(fill="x")
        tk.Label(stat, text="Usuarios registrados", font=("Segoe UI", 9), bg=CRM_THEME["panel_alt"], fg=CRM_THEME["muted"]).pack(anchor="w")
        self.total_label = tk.Label(stat, text="0", font=("Segoe UI Semibold", 22), bg=CRM_THEME["panel_alt"], fg=CRM_THEME["coral"])
        self.total_label.pack(anchor="w", pady=(8, 0))

        tk.Label(right, text="Listado general", font=("Segoe UI Semibold", 16), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(right, text="Visualiza rapidamente los usuarios actuales y su nivel de acceso.", font=("Segoe UI", 9), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(4, 12))
        self.tabla = ttk.Treeview(right, columns=("id", "usuario", "tipo"), show="headings", style="CRM.Treeview")
        self.tabla.heading("id", text="Id")
        self.tabla.heading("usuario", text="Usuario")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.column("id", width=80, anchor="center")
        self.tabla.column("usuario", width=280, anchor="center")
        self.tabla.column("tipo", width=140, anchor="center")
        self.tabla.pack(fill="both", expand=True)

    def _field(self, parent, label, row, show=None):
        tk.Label(parent, text=label, bg=CRM_THEME["panel"], fg=CRM_THEME["navy"], font=("Segoe UI Semibold", 10)).grid(row=row * 2, column=0, sticky="w", pady=(0 if row == 0 else 12, 6))
        entry = ttk.Entry(parent, style="CRM.TEntry")
        entry.grid(row=row * 2 + 1, column=0, sticky="ew")
        if show:
            entry.config(show=show)
        return entry

    def cargar_usuarios(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        rows = self.controller.listar_usuarios()
        for row in rows:
            self.tabla.insert("", "end", values=(row["id_usuario"], row["nombre"], row["tipo"]))
        self.total_label.config(text=str(len(rows)))

    def crear_usuario(self):
        try:
            _, mensaje = self.controller.crear_usuario(
                self.usuario.get().strip(),
                self.password.get().strip(),
                self.tipo.get().strip(),
                self.nombre_real.get().strip(),
            )
            messagebox.showinfo("Usuarios", mensaje)
            self.cargar_usuarios()
            self.event_generate("<<UsuariosActualizados>>", when="tail")
            self._limpiar()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _limpiar(self):
        for entry in (self.usuario, self.password, self.nombre_real):
            entry.delete(0, tk.END)
        self.tipo.current(1)
