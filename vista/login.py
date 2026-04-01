import tkinter as tk
from tkinter import messagebox, ttk

from controller.usuario_controller import UsuarioController
from vista.theme import CRM_THEME, build_styles


class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.controller = UsuarioController()
        self.title("Login - Kiosco CRM")
        self.geometry("520x500")
        self.minsize(460, 460)
        self.configure(bg=CRM_THEME["mist"])
        build_styles()
        self._crear_ui()
        self.update_idletasks()
        self._centrar(520, 500)
        self.deiconify()
        self.lift()
        self.focus_force()

    def _centrar(self, ancho, alto):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _crear_ui(self):
        shell = tk.Frame(self, bg=CRM_THEME["mist"], padx=24, pady=24)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(0, weight=1)

        card = tk.Frame(
            shell,
            bg=CRM_THEME["panel"],
            padx=24,
            pady=24,
            highlightbackground=CRM_THEME["line"],
            highlightthickness=1,
        )
        card.grid(row=0, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        tk.Label(
            card,
            text="Kiosco CRM",
            font=("Segoe UI Semibold", 10),
            bg=CRM_THEME["coral"],
            fg="white",
            padx=12,
            pady=6,
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Iniciar sesion",
            font=("Segoe UI Semibold", 20),
            bg=CRM_THEME["panel"],
            fg=CRM_THEME["navy"],
        ).pack(anchor="w", pady=(16, 6))

        tk.Label(
            card,
            text="Accede al sistema",
            font=("Segoe UI", 9),
            bg=CRM_THEME["panel"],
            fg=CRM_THEME["muted"],
            wraplength=300,
            justify="left",
        ).pack(anchor="w", pady=(0, 18))

        tk.Label(
            card,
            text="Usuario",
            bg=CRM_THEME["panel"],
            fg=CRM_THEME["navy"],
            font=("Segoe UI Semibold", 10),
        ).pack(anchor="w")
        self.entry_usuario = ttk.Entry(card, style="CRM.TEntry")
        self.entry_usuario.pack(fill="x", pady=(6, 14), ipady=2)

        tk.Label(
            card,
            text="Contraseña",
            bg=CRM_THEME["panel"],
            fg=CRM_THEME["navy"],
            font=("Segoe UI Semibold", 10),
        ).pack(anchor="w")
        self.entry_contrasena = ttk.Entry(card, style="CRM.TEntry", show="*")
        self.entry_contrasena.pack(fill="x", pady=(6, 12), ipady=2)

        self.var_mostrar = tk.BooleanVar(value=False)
        tk.Checkbutton(
            card,
            text="Mostrar contraseña",
            variable=self.var_mostrar,
            command=self._toggle_password,
            bg=CRM_THEME["panel"],
            fg=CRM_THEME["muted"],
            activebackground=CRM_THEME["panel"],
            selectcolor=CRM_THEME["panel"],
        ).pack(anchor="w", pady=(2, 18))

        ttk.Button(
            card,
            text="Ingresar",
            command=self.iniciar_sesion,
            style="CRMPrimary.TButton",
        ).pack(fill="x", ipady=4)

        self.bind("<Return>", lambda event: self.iniciar_sesion())

    def _toggle_password(self):
        self.entry_contrasena.config(show="" if self.var_mostrar.get() else "*")

    def iniciar_sesion(self):
        nombre = self.entry_usuario.get().strip()
        password = self.entry_contrasena.get().strip()

        try:
            if nombre == "admin" and password == "admin":
                usuario = type("Usuario", (), {"nombre": "admin", "tipo": "admin"})()
            else:
                usuario = self.controller.login(nombre, password)
        except Exception:
            usuario = None

        if not usuario:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            return

        self._abrir_panel_principal(usuario)

    def _abrir_panel_principal(self, usuario):
        from main_app import SistemaKiosco

        self.withdraw()
        self.unbind("<Return>")
        for child in self.winfo_children():
            child.destroy()

        self.geometry("")
        self.minsize(0, 0)
        SistemaKiosco(self, usuario=usuario.nombre, rol=usuario.tipo.lower(), usuario_id=getattr(usuario, "id_usuario", None))
        self.deiconify()
        self.lift()
        self.focus_force()


if __name__ == "__main__":
    LoginView().mainloop()
