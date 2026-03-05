import tkinter as tk
from app.constants import COLOR_BG, COLOR_TEXT, COLOR_HOVER

def create_image_button(parent, text, command, image_manager, filename, image_size=(120, 40)):
    """
    REPLICA EXACTA STEGANO: Botón con sombra profesional (128 opacidad) y efecto de presión.
    """
    # Sombra estándar de Stegano (0, 0, 0, 128) para máxima profundidad y nitidez
    shadow_color = (0, 0, 0, 128)
    
    photo = image_manager.load(
        filename, 
        size=image_size, 
        add_shadow_effect=True,
        shadow_offset=(2, 2),
        shadow_color=shadow_color,
        blur_radius=3,
        border=5
    )

    button = tk.Button(
        parent,
        text=text,
        image=photo,
        compound="center",
        command=command,
        relief="flat",
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        font=("Segoe UI", 11, "bold"),
        activebackground=COLOR_BG,
        activeforeground=COLOR_TEXT,
        borderwidth=0,
        highlightthickness=0,
        cursor="hand2"
    )

    if photo:
        button.photo = photo

    # Efectos Hover (Amarillo/Dorado)
    button.bind("<Enter>", lambda e: button.config(fg=COLOR_HOVER))
    button.bind("<Leave>", lambda e: button.config(fg=COLOR_TEXT))

    # Efecto de presión física
    button.bind("<Button-1>", lambda e: button.place_configure(rely=0.54) if button.winfo_manager() == "place" else None)
    button.bind("<ButtonRelease-1>", lambda e: button.place_configure(rely=0.5) if button.winfo_manager() == "place" else None)
    
    return button
