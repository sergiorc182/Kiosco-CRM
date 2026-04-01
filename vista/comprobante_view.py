import tkinter as tk
from tkinter import ttk, messagebox

class ComprobanteView(tk.Toplevel):

    def __init__(self, master, total, controller):
        super().__init__(master)

        self.controller = controller
        self.total = total

        self.title("Comprobante")
        self.geometry("400x300")

        self._ui()

    def _ui(self):
        tk.Label(self, text=f"TOTAL: ${self.total:.2f}", font=("Arial", 18)).pack(pady=10)

        self.metodo = tk.StringVar(value="Efectivo")

        ttk.Radiobutton(self, text="Efectivo", variable=self.metodo, value="Efectivo").pack()
        ttk.Radiobutton(self, text="Tarjeta", variable=self.metodo, value="Tarjeta").pack()

        self.entry_monto = tk.Entry(self)
        self.entry_monto.pack()

        tk.Button(self, text="Confirmar", command=self.confirmar).pack(pady=10)

    def confirmar(self):
        try:
            monto = float(self.entry_monto.get())
        except:
            messagebox.showerror("Error", "Monto inválido")
            return

        ok, msg = self.controller.pagar(self.metodo.get(), monto)

        if ok:
            messagebox.showinfo("Éxito", msg)
            self.destroy()
        else:
            messagebox.showerror("Error", msg)