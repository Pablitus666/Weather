import tkinter as tk
from tkinter import Toplevel
import os
from app.constants import COLOR_BG, COLOR_TEXT, COLOR_HOVER, IMAGE_LOGO_ICO, IMAGE_ROBOT, IMAGE_BOTON, APP_VERSION
from core.resources import get_resource_path
from core.i18n import _

class InfoWindow(Toplevel):
    """
    REPLICA EXACTA STEGANO: Ventana de información con robot y botón perfecto.
    """
    def __init__(self, parent, image_manager):
        super().__init__(parent)
        self.withdraw()
        self.image_manager = image_manager
        self.title(f"{_('title.info')} v{APP_VERSION}")
        self.config(bg=COLOR_BG)
        self.resizable(False, False)
        
        # --- CONFIGURACIÓN MODAL PREMIUM ---
        self.transient(parent)   
        self.grab_set()          
        # ----------------------------------

        try:
            icon_path = get_resource_path(IMAGE_LOGO_ICO)
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass

        self._create_widgets()
        self._center_window(370, 230) # Dimensiones optimas Stegano
        self.deiconify()

    def _create_widgets(self):
        # Réplica exacta de la estructura de Stegano     
        frame_info = tk.Frame(self, bg=COLOR_BG)
        frame_info.pack(pady=10, padx=10, fill="both", expand=True)

        frame_info.grid_columnconfigure(0, weight=1)
        frame_info.grid_columnconfigure(1, weight=1)
        frame_info.grid_rowconfigure(0, weight=1)
        frame_info.grid_rowconfigure(1, weight=1)
        frame_info.grid_rowconfigure(2, weight=1)

        # Robot grande (160x160) como en Stegano
        robot_photo = self.image_manager.load(IMAGE_ROBOT, size=(160, 160))
        if robot_photo:
            img_label = tk.Label(frame_info, image=robot_photo, bg=COLOR_BG)
            img_label.image = robot_photo
            img_label.grid(row=0, column=0, padx=(5, 10), pady=0, rowspan=3, sticky="nsew")

        message = tk.Label(
            frame_info,
            text=_("info.developed_by"),
            justify="center",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=("Segoe UI", 14, "bold"),
            wraplength=160
        )
        message.grid(row=0, column=1, rowspan=2, sticky="s", pady=(0, 10), padx=(0, 20))

        # Botón con efectos de sombra EXACTOS de Stegano
        # (shadow_color usa el default 128 que el usuario considera perfecto)
        btn_normal = self.image_manager.load(
            IMAGE_BOTON, size=(110, 40), add_shadow_effect=True,
            shadow_offset=(2, 2), blur_radius=3, border=5
        )

        # Contenedor rígido más amplio para evitar recortes en la sombra
        btn_holder = tk.Frame(frame_info, bg=COLOR_BG, width=140, height=60)
        btn_holder.pack_propagate(False)
        btn_holder.grid(row=2, column=1, sticky="n", pady=(10, 0))

        self.close_btn = tk.Button(
            btn_holder,
            text=_("button.close"),
            image=btn_normal,
            compound="center",
            font=("Segoe UI", 12, "bold"),
            command=self.destroy,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            bd=0,
            relief="flat",          # Forzar relieve plano
            borderwidth=0,          # Doble seguridad
            highlightthickness=0,   # Eliminar borde de foco
            padx=0, pady=0,         # Eliminar padding interno
            cursor="hand2",
            activebackground=COLOR_BG,
            activeforeground=COLOR_HOVER,
            anchor="center",
            justify="center"
        )
        self.close_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Efectos Hover y Presión EXACTOS
        def on_press(e):
            self.close_btn.place_configure(rely=0.54)
        def on_release(e):
            self.close_btn.place_configure(rely=0.5)

        self.close_btn.bind("<Enter>", lambda e: self.close_btn.config(fg=COLOR_HOVER))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn.config(fg=COLOR_TEXT))
        self.close_btn.bind("<Button-1>", on_press)
        self.close_btn.bind("<ButtonRelease-1>", on_release)

    def _center_window(self, width, height):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
