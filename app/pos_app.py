import tkinter as tk

from vista.pos_view import POSView


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema POS - Kiosco")
    root.geometry("1100x700")
    POSView(root)
    root.mainloop()
