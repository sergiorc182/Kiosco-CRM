import tkinter as tk
from tkinter import messagebox, ttk

from controller.turno_controller import TurnoController
from vista.caja_view import CajaView
from vista.inventario_view import InventarioView
from vista.pos_view import POSView
from vista.proveedor_view import ProveedorView
from vista.reporte_view import ReporteView
from vista.theme import CRM_THEME, build_styles
from vista.turno_view import TurnoView
from vista.usuario_view import UsuarioView


class SistemaKiosco(tk.Frame):
    def __init__(self, master, usuario=None, rol="empleado", usuario_id=None):
        super().__init__(master, bg=CRM_THEME["mist"])
        self.master = master
        self.usuario = usuario or "usuario"
        self.rol = rol
        self.usuario_id = usuario_id
        self.turno_controller = TurnoController()
        self._vista_actual = None
        self._reportes_window = None
        self._nav_buttons = {}
        self._empleado_actual = self.turno_controller.obtener_empleado_por_usuario(usuario_id) if usuario_id else None
        self._turno_requerido = False

        self.master.title("Sistema de Kiosco - Menu Principal")
        self.master.state("zoomed")
        build_styles()
        self.master.configure(bg=CRM_THEME["mist"])
        self.pack(fill="both", expand=True)
        self.bind_all("<<TurnoEstadoActualizado>>", self._on_turno_estado_actualizado)
        self._crear_interfaz_base()
        self._actualizar_estado_turno_inicial()
        self.master.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

    def destroy(self):
        self.unbind_all("<<TurnoEstadoActualizado>>")
        super().destroy()

    def _crear_interfaz_base(self):
        header = tk.Frame(self, bg=CRM_THEME["navy"], height=84)
        header.pack(fill="x")
        header.pack_propagate(False)

        brand = tk.Frame(header, bg=CRM_THEME["navy"])
        brand.pack(side="left", fill="y", padx=24)
        tk.Label(brand, text="Kiosco CRM", font=("Segoe UI Semibold", 24), bg=CRM_THEME["navy"], fg="white").pack(anchor="w", pady=(14, 0))
        tk.Label(brand, text=f"Sesion activa: {self.usuario}  |  Rol: {self.rol}", font=("Segoe UI", 10), bg=CRM_THEME["navy"], fg="#c7d3ea").pack(anchor="w")

        nav = tk.Frame(header, bg=CRM_THEME["navy"])
        nav.pack(side="right", padx=18, pady=18)
        self._crear_nav_button(nav, "Inicio", self._mostrar_inicio).pack(side="left", padx=4)
        self._crear_nav_button(nav, "POS", lambda: self._mostrar_modulo(POSView)).pack(side="left", padx=4)
        self._crear_nav_button(nav, "Inventario", lambda: self._mostrar_modulo(InventarioView)).pack(side="left", padx=4)
        self._crear_nav_button(nav, "Proveedores", lambda: self._mostrar_modulo(ProveedorView)).pack(side="left", padx=4)
        self._crear_nav_button(nav, "Caja", lambda: self._mostrar_modulo(CajaView)).pack(side="left", padx=4)
        self._crear_nav_button(nav, "Turnos", lambda: self._mostrar_modulo(TurnoView)).pack(side="left", padx=4)
        self._crear_nav_button(nav, "Reportes", self._abrir_reportes).pack(side="left", padx=4)
        if self.rol == "admin":
            self._crear_nav_button(nav, "Usuarios", lambda: self._mostrar_modulo(UsuarioView)).pack(side="left", padx=4)

        self.workspace = tk.Frame(self, bg=CRM_THEME["mist"])
        self.workspace.pack(fill="both", expand=True)

        self.barra_estado = tk.Label(
            self,
            text=f"Usuario: {self.usuario} | Rol: {self.rol}",
            anchor="w",
            font=("Segoe UI", 10),
            bg=CRM_THEME["navy"],
            fg="white",
            padx=10,
        )
        self.barra_estado.pack(side="bottom", fill="x")

    def _crear_nav_button(self, parent, text, command):
        style = "CRMPrimary.TButton" if text == "POS" else "CRMSecondary.TButton"
        button = ttk.Button(parent, text=text, command=command, style=style)
        self._nav_buttons[text] = button
        return button

    def _actualizar_estado_turno_inicial(self):
        if self.rol != "empleado":
            self._turno_requerido = False
            self._actualizar_nav()
            self._mostrar_inicio()
            return

        self._turno_requerido = not self._empleado_tiene_turno_activo()
        self._actualizar_nav()
        if self._turno_requerido:
            self._mostrar_modulo(TurnoView, forzar=True)
            messagebox.showinfo("Turnos", "Debes iniciar tu turno antes de usar el resto del sistema.")
        else:
            self._mostrar_inicio()

    def _empleado_tiene_turno_activo(self):
        activo = self.turno_controller.obtener_turno_activo()
        if not activo or not self._empleado_actual:
            return False
        return activo.get("empleado") == self._empleado_actual.get("nombre")

    def _actualizar_nav(self):
        if self.rol == "admin":
            return
        bloqueo = {
            "Inicio": not self._turno_requerido,
            "POS": not self._turno_requerido,
            "Inventario": not self._turno_requerido,
            "Proveedores": not self._turno_requerido,
            "Caja": not self._turno_requerido,
            "Turnos": True,
            "Reportes": not self._turno_requerido,
        }
        for name, button in self._nav_buttons.items():
            if name == "Usuarios":
                button.config(state="disabled")
            elif name in bloqueo:
                button.config(state="normal" if bloqueo[name] else "disabled")

    def _limpiar_workspace(self):
        for child in self.workspace.winfo_children():
            child.destroy()
        self._vista_actual = None

    def _mostrar_inicio(self):
        if self._turno_requerido and self.rol == "empleado":
            self._mostrar_modulo(TurnoView, forzar=True)
            return

        self._limpiar_workspace()

        main = tk.Frame(self.workspace, bg=CRM_THEME["mist"])
        main.pack(fill="both", expand=True)

        hero = tk.Frame(main, bg=CRM_THEME["navy"], height=220)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        hero_content = tk.Frame(hero, bg=CRM_THEME["navy"])
        hero_content.pack(fill="both", expand=True, padx=40, pady=28)
        tk.Label(hero_content, text="Panel principal", font=("Segoe UI Semibold", 30), bg=CRM_THEME["navy"], fg="white").pack(anchor="w")
        tk.Label(hero_content, text="Control operativo para caja, inventario y turnos", font=("Segoe UI", 12), bg=CRM_THEME["navy"], fg="#c7d3ea").pack(anchor="w", pady=(8, 18))
        tk.Label(hero_content, text=f"Bienvenido, {self.usuario}", font=("Segoe UI Semibold", 10), bg=CRM_THEME["coral"], fg="white", padx=14, pady=8).pack(anchor="w")

        body = tk.Frame(main, bg=CRM_THEME["mist"], padx=34, pady=28)
        body.pack(fill="both", expand=True)

        info_strip = tk.Frame(body, bg=CRM_THEME["mist"])
        info_strip.pack(fill="x", pady=(0, 18))
        info_cards = [
            ("POS", "Ventas rapidas y cobro centralizado"),
            ("Inventario", "Gestion de stock y catalogo"),
            ("Proveedores", "Compras, altas y relacion con inventario"),
            ("Caja", "Apertura, movimientos y cierre del efectivo"),
            ("Turnos", "Planificacion operativa del equipo"),
        ]
        if self.rol == "admin":
            info_cards.append(("Usuarios", "Administracion de accesos y perfiles"))

        for title, subtitle in info_cards:
            info = tk.Frame(info_strip, bg=CRM_THEME["panel"], padx=18, pady=16, highlightbackground=CRM_THEME["line"], highlightthickness=1)
            info.pack(side="left", fill="x", expand=True, padx=8)
            tk.Label(info, text=title, font=("Segoe UI Semibold", 13), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
            tk.Label(info, text=subtitle, font=("Segoe UI", 10), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(6, 0))

        card = tk.Frame(body, bg=CRM_THEME["panel"], padx=28, pady=28, highlightbackground=CRM_THEME["line"], highlightthickness=1)
        card.pack(anchor="center")
        tk.Label(card, text="Modulos del sistema", font=("Segoe UI Semibold", 18), bg=CRM_THEME["panel"], fg=CRM_THEME["navy"]).pack(anchor="w")
        tk.Label(card, text="Accede a las 3 areas principales, arriba a la derecha estan otros modulos.", font=("Segoe UI", 10), bg=CRM_THEME["panel"], fg=CRM_THEME["muted"]).pack(anchor="w", pady=(6, 18))

        botones = [
            ("POS", lambda: self._mostrar_modulo(POSView)),
            ("Inventario", lambda: self._mostrar_modulo(InventarioView)),
            ("Proveedores", lambda: self._mostrar_modulo(ProveedorView)),
            ("Caja", lambda: self._mostrar_modulo(CajaView)),
            ("Turnos", lambda: self._mostrar_modulo(TurnoView)),
            ("Reportes", self._abrir_reportes),
        ]
        if self.rol == "admin":
            botones.append(("Usuarios", lambda: self._mostrar_modulo(UsuarioView)))

        for texto, accion in botones:
            estado = "normal"
            if self.rol == "empleado" and self._turno_requerido and texto != "Turnos":
                estado = "disabled"
            ttk.Button(card, text=texto, command=accion, style="CRMPrimary.TButton" if texto == "POS" else "CRMSecondary.TButton", state=estado).pack(fill="x", pady=8, ipady=4)

    def _mostrar_modulo(self, view_class, forzar=False):
        if self._turno_requerido and self.rol == "empleado" and view_class is not TurnoView and not forzar:
            messagebox.showwarning("Turnos", "Primero debes iniciar tu turno.")
            self._mostrar_modulo(TurnoView, forzar=True)
            return

        self._limpiar_workspace()
        kwargs = {}
        if view_class is TurnoView:
            kwargs = {
                "rol": self.rol,
                "usuario": self.usuario,
                "usuario_id": self.usuario_id,
                "empleado_actual": self._empleado_actual,
            }
        self._vista_actual = view_class(self.workspace, **kwargs) if kwargs else view_class(self.workspace)

    def _abrir_reportes(self):
        if self._turno_requerido and self.rol == "empleado":
            messagebox.showwarning("Turnos", "Primero debes iniciar tu turno.")
            self._mostrar_modulo(TurnoView, forzar=True)
            return None

        if self._reportes_window and self._reportes_window.winfo_exists():
            self._reportes_window.deiconify()
            self._reportes_window.lift()
            self._reportes_window.focus_force()
            return self._reportes_window
        self._reportes_window = ReporteView(self)
        self._reportes_window.protocol("WM_DELETE_WINDOW", self._cerrar_reportes)
        return self._reportes_window

    def _cerrar_reportes(self):
        if self._reportes_window and self._reportes_window.winfo_exists():
            self._reportes_window.destroy()
        self._reportes_window = None

    def _on_turno_estado_actualizado(self, _event=None):
        self._turno_requerido = not self._empleado_tiene_turno_activo() if self.rol == "empleado" else False
        self._actualizar_nav()

    def confirmar_salida(self):
        if messagebox.askyesno("Salir", "Seguro que desea salir del sistema?"):
            self.master.destroy()
