import tkinter as tk
from tkinter import messagebox

from controller.categoria_controller import CategoriaController


class CategoriaView:
    def __init__(self, root):
        self.root = root
        self.controller = CategoriaController()
        self.root.title("Agregar Categoria - Kiosco")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        self._crear_ui()

    def _crear_ui(self):
        frame = tk.LabelFrame(self.root, text="Ingresar Categoria", padx=10, pady=10)
        frame.pack(padx=15, pady=15, fill="both", expand=True)
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry = tk.Entry(frame, width=30)
        self.entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Guardar", command=self.guardar).pack(pady=10)

    def guardar(self):
        ok, mensaje = self.controller.crear_categoria(self.entry.get())
        if ok:
            messagebox.showinfo("Exito", mensaje)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)
