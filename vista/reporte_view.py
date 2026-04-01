import tkinter as tk
from tkinter import messagebox

from controller.reporte_controller import ReporteController


class ReporteView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = ReporteController()
        self.title("Enviar Reporte")
        self.geometry("500x400")
        self.configure(bg="#FFE5B4")
        self.transient(master)
        self.grab_set()
        self._crear_ui()

    def _crear_ui(self):
        main = tk.Frame(self, bg="#FFE5B4", padx=24, pady=24)
        main.pack(fill="both", expand=True)
        tk.Label(main, text="Enviar reporte", font=("Segoe UI", 18, "bold"), bg="#FFE5B4").pack(pady=(0, 12))
        tk.Label(main, text="Su email (opcional)", bg="#FFE5B4").pack(anchor="w")
        self.email_entry = tk.Entry(main)
        self.email_entry.pack(fill="x", pady=(0, 12))
        tk.Label(main, text="Reporte", bg="#FFE5B4").pack(anchor="w")
        self.reporte_text = tk.Text(main, height=10)
        self.reporte_text.pack(fill="both", expand=True, pady=(0, 12))
        actions = tk.Frame(main, bg="#FFE5B4")
        actions.pack(fill="x")
        tk.Button(actions, text="Enviar", command=self.enviar_reporte, bg="#27ae60", fg="white").pack(side="right", padx=4)
        tk.Button(actions, text="Cancelar", command=self.destroy, bg="#e74c3c", fg="white").pack(side="right", padx=4)

    def enviar_reporte(self):
        try:
            enviado, path = self.controller.enviar_reporte(
                self.reporte_text.get("1.0", tk.END).strip(),
                self.email_entry.get().strip(),
            )
            if enviado:
                messagebox.showinfo("Reporte", "Reporte enviado correctamente")
            else:
                messagebox.showwarning("Reporte", f"No se pudo enviar por email. Se guardó copia local en {path}")
            self.destroy()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
