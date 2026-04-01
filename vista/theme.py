from tkinter import ttk


CRM_THEME = {
    "navy": "#132039",
    "navy_soft": "#1c2d4f",
    "coral": "#f26b5e",
    "coral_dark": "#df584c",
    "mist": "#f5f7fb",
    "panel": "#ffffff",
    "panel_alt": "#eef2f8",
    "text": "#14213d",
    "muted": "#64748b",
    "line": "#d8e0ec",
    "success": "#2e8b70",
}


def build_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("CRMPrimary.TButton", background=CRM_THEME["coral"], foreground="white", borderwidth=0, padding=(14, 10), font=("Segoe UI Semibold", 10))
    style.map("CRMPrimary.TButton", background=[("active", CRM_THEME["coral_dark"])])
    style.configure("CRMSecondary.TButton", background=CRM_THEME["navy"], foreground="white", borderwidth=0, padding=(14, 10), font=("Segoe UI Semibold", 10))
    style.map("CRMSecondary.TButton", background=[("active", CRM_THEME["navy_soft"])])
    style.configure("CRMOutline.TButton", background=CRM_THEME["panel_alt"], foreground=CRM_THEME["navy"], borderwidth=0, padding=(12, 9), font=("Segoe UI Semibold", 10))
    style.map("CRMOutline.TButton", background=[("active", "#e5ebf5")])
    style.configure("CRM.TEntry", fieldbackground="white", bordercolor=CRM_THEME["line"], lightcolor=CRM_THEME["line"], darkcolor=CRM_THEME["line"], foreground=CRM_THEME["text"], padding=8)
    style.configure("CRM.TCombobox", fieldbackground="white", background="white", foreground=CRM_THEME["text"], bordercolor=CRM_THEME["line"], lightcolor=CRM_THEME["line"], darkcolor=CRM_THEME["line"], padding=6)
    style.configure("CRM.Treeview", background="white", fieldbackground="white", foreground=CRM_THEME["text"], rowheight=32, bordercolor=CRM_THEME["line"], lightcolor=CRM_THEME["line"], darkcolor=CRM_THEME["line"], font=("Segoe UI", 10))
    style.map("CRM.Treeview", background=[("selected", "#dbe8ff")], foreground=[("selected", CRM_THEME["navy"])])
    style.configure("CRM.Treeview.Heading", background=CRM_THEME["navy"], foreground="white", borderwidth=0, font=("Segoe UI Semibold", 10), padding=10)
    style.map("CRM.Treeview.Heading", background=[("active", CRM_THEME["navy_soft"])])
    return style


def maximize_window(window):
    window.update_idletasks()
    try:
        window.state("zoomed")
    except Exception:
        width = max(window.winfo_screenwidth() - 40, 900)
        height = max(window.winfo_screenheight() - 80, 600)
        window.geometry(f"{width}x{height}+10+10")
    window.minsize(960, 620)
    window.resizable(True, True)
