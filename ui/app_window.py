import tkinter as tk
from customtkinter import CTk, CTkEntry
import asyncio
import threading
import os
import ctypes

from app.constants import *
from core.resources import get_resource_path
from utils.validator import validate_city_name
from ui.info_window import InfoWindow
from ui.widgets import create_image_button
from core.image_manager import ImageManager
from core.settings_manager import SettingsManager
from core.i18n import _, load_i18n
from services.weather_service import WeatherService
from core.exceptions import WeatherError, NetworkError
from utils.logger import logger

class WeatherApp(CTk):
    def __init__(self):
        super().__init__()
        
        # FORZAR ICONO EN BARRA DE TAREAS (Windows)
        try:
            myappid = 'WalterTellez.WeatherApp.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass
            
        load_i18n()
        self.settings = SettingsManager()
        
        # Medidas exactas base
        self.base_width = 370
        self.base_height = 630
        
        self.title("Weather Report")
        self.geometry(f"{self.base_width}x{self.base_height}")
        self.config(bg=COLOR_BG)
        self.resizable(False, False)
        
        self.image_manager = ImageManager(self)
        
        # Cargar icono de ventana de forma nativa (iconbitmap es lo mejor para .ico en Windows)
        try:
            icon_path = get_resource_path(IMAGE_LOGO_ICO)
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass

        self.weather_service = WeatherService()
        self.is_fetching = False
        self.search_done = False
        self._retry_handle = None

        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_async_loop, daemon=True).start()

        self._setup_ui()
        self._centrar_ventana()
        
        # Verificación inicial de API_KEY
        from app.config import API_KEY
        if not API_KEY:
            self.after(500, lambda: self._display_message(_("error.api")))

    def _run_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def _setup_ui(self):
        # 1. LOGO
        logo_photo = self.image_manager.load(
            IMAGE_LOGO_PNG, size=(180, 180), add_shadow_effect=True,
            shadow_offset=(2, 2), shadow_color=(0, 0, 0, 80), blur_radius=4, border=6
        )
        self.logo_label = tk.Label(self, image=logo_photo, bg=COLOR_BG, cursor="hand2")
        self.logo_label.image = logo_photo
        self.logo_label.pack(padx=30, pady=20)
        self.logo_label.bind("<Button-1>", lambda e: self._mostrar_informacion())

        # 2. ENTRADA
        self.city_entry = CTkEntry(
            self, font=("Arial", 20, "bold"), justify="center",
            border_color=COLOR_ACCENT, fg_color=COLOR_BG, width=300, height=45
        )
        self.city_entry.pack(padx=30, pady=10)
        
        # Tecla SUPR vinculada a nivel de aplicación para que funcione siempre
        self.bind_all("<Delete>", self._on_delete_key)
        self.city_entry.bind("<Return>", lambda e: self._handle_search())
        self.city_entry.bind("<KeyPress>", self._clear_on_new_search)
        
        self.after(100, lambda: self.city_entry.focus_set())
        
        # 3. BOTÓN BÚSQUEDA
        btn_holder = tk.Frame(self, bg=COLOR_BG, width=220, height=60)
        btn_holder.pack_propagate(False)
        btn_holder.pack(pady=15)

        self.search_button = create_image_button(
            btn_holder, _("ui.search"), self._handle_search, self.image_manager, 
            IMAGE_BOTON, image_size=(200, 48)
        )
        self.search_button.config(font=("Arial", 16, "bold"))
        self.search_button.place(relx=0.5, rely=0.5, anchor="center")

        # 4. RESULTADOS PRINCIPALES
        self.lbl_city = tk.Label(self, bg=COLOR_BG, fg=COLOR_TEXT, font=("Arial", 20, "bold"), wraplength=320)
        self.lbl_city.pack(padx=20, pady=(5, 5))

        self.lbl_temp = tk.Label(self, bg=COLOR_BG, fg=COLOR_TEXT, font=FONT_TEMP)
        self.lbl_temp.pack(padx=10, pady=0)

        self.lbl_desc = tk.Label(self, bg=COLOR_BG, fg=COLOR_TEXT, font=("Arial", 18, "bold"), wraplength=320)
        self.lbl_desc.pack(padx=10, pady=(0, 15))

        # 5. PANEL DE DETALLES (Optimizado para no cortarse)
        self.details_frame = tk.Frame(self, bg=COLOR_BG)
        self.details_frame.pack(fill="x", padx=25, pady=(0, 15))
        
        self.lbl_humidity = tk.Label(
            self.details_frame, text="", bg=COLOR_BG, fg=COLOR_ACCENT, 
            font=("Arial", 11, "bold"), justify="left"
        )
        self.lbl_humidity.pack(side="left", padx=(10, 0))
        
        self.lbl_wind = tk.Label(
            self.details_frame, text="", bg=COLOR_BG, fg=COLOR_ACCENT, 
            font=("Arial", 11, "bold"), justify="right"
        )
        self.lbl_wind.pack(side="right", padx=(0, 10))

    def _ajustar_altura_dinamica(self):
        """Ajusta la altura basándose en el contenido real."""
        self.update_idletasks()
        altura_requerida = self.winfo_reqheight()
        nuevo_alto = max(self.base_height, altura_requerida + 15)
        self.geometry(f"{self.base_width}x{nuevo_alto}")

    def _on_delete_key(self, event):
        """Limpia la entrada y resetea toda la interfaz al estado inicial."""
        self.city_entry.delete(0, 'end')
        self._reset_interface_to_default()
        return "break"

    def _clear_on_new_search(self, event):
        """Al empezar a escribir una nueva ciudad, limpia los resultados anteriores inmediatamente."""
        if event.keysym in ("Return", "Delete", "BackSpace", "Tab", "Shift_L", "Shift_R", "Alt_L", "Control_L"):
            return
            
        if self.search_done:
            self.city_entry.delete(0, 'end')
            self._reset_interface_to_default()

    def _reset_interface_to_default(self):
        """Devuelve la GUI a su estado inicial: logo base, sin textos y altura 630px."""
        self.search_done = False
        
        # 1. Limpiar etiquetas
        self.lbl_city.config(text="")
        self.lbl_temp.config(text="")
        self.lbl_desc.config(text="")
        self.lbl_humidity.config(text="")
        self.lbl_wind.config(text="")
        
        # 2. Restaurar Logo Predeterminado
        default_photo = self.image_manager.load(
            IMAGE_LOGO_PNG, size=(180, 180), add_shadow_effect=True,
            shadow_offset=(2, 2), shadow_color=(0, 0, 0, 80), blur_radius=4, border=6
        )
        if default_photo:
            self.logo_label.config(image=default_photo)
            self.logo_label.image = default_photo
            
        # 3. Restaurar Altura Base
        self._ajustar_altura_dinamica()

    def _handle_search(self, auto_retry=False):
        if not auto_retry and self._retry_handle:
            self.after_cancel(self._retry_handle)
            self._retry_handle = None

        if self.is_fetching: return
        
        city_name = self.city_entry.get().strip()
        if not city_name:
            if not auto_retry: self._display_message(_("ui.enter_city"))
            return
        if not validate_city_name(city_name):
            self._display_message(_("ui.invalid_name"))
            return

        self.is_fetching = True
        asyncio.run_coroutine_threadsafe(self._perform_search(city_name, auto_retry), self.loop)

    async def _perform_search(self, city_name, auto_retry):
        try:
            weather = await self.weather_service.get_weather(city_name)
            self.after(0, self._update_ui_success, weather)
            # Ya no guardamos en settings para el arranque, pero mantenemos settings para otros usos futuros.
        except NetworkError:
            if auto_retry:
                self.after(0, self._display_message, _("ui.connecting"))
                self._retry_handle = self.after(5000, lambda: self._handle_search(auto_retry=True))
            else:
                self.after(0, self._display_message, _("error.network"))
        except WeatherError as e:
            err_msg = str(e)
            if "not found" in err_msg.lower(): err_msg = _("error.city_not_found")
            elif "api" in err_msg.lower(): err_msg = _("error.api")
            self.after(0, self._display_message, err_msg)
        except Exception:
            self.after(0, self._display_message, "Error")
        finally:
            self.after(0, self._reset_ui_state)

    def _update_ui_success(self, weather):
        self.lbl_city.config(text=f"{weather.city}, {weather.country}")
        self.lbl_temp.config(text=f"{int(weather.temperature)}°C")
        self.lbl_desc.config(text=weather.description)
        self.lbl_humidity.config(text=f"💧 {_('ui.humidity')}: {weather.humidity}%")
        self.lbl_wind.config(text=f"💨 {_('ui.wind')}: {weather.wind_speed} km/h")
        self._update_weather_icon(weather.weather_id, weather.icon_code, weather.temperature)
        self.search_done = True
        self.after(10, self._ajustar_altura_dinamica)

    def _update_weather_icon(self, weather_id, icon_code, temp):
        file_name = "logo"
        if 200 <= weather_id <= 232: file_name = "electricalstorm"
        elif weather_id == 500 or weather_id == 501 or 300 <= weather_id <= 321: file_name = "lightrain"
        elif 502 <= weather_id <= 531: file_name = "heavyrain"
        elif 600 <= weather_id <= 622: file_name = "snow"
        elif 701 <= weather_id <= 781: file_name = "mist"
        elif weather_id == 800:
            file_name = "veryhot" if temp >= 30 else "clear"
        elif weather_id == 801: file_name = "fewclouds"
        elif weather_id == 802: file_name = "scatteredclouds"
        elif weather_id == 803 or weather_id == 804: file_name = "verycloudy"

        new_photo = self.image_manager.load(
            f"{file_name}.png", size=(180, 180), add_shadow_effect=True,
            shadow_color=(0, 0, 0, 80), blur_radius=4, border=6
        )
        if new_photo is None:
            new_photo = self.image_manager.load(
                IMAGE_LOGO_PNG, size=(180, 180), add_shadow_effect=True,
                shadow_offset=(2, 2), shadow_color=(0, 0, 0, 80), blur_radius=4, border=6
            )
        if new_photo:
            self.logo_label.config(image=new_photo)
            self.logo_label.image = new_photo

    def _display_message(self, msg):
        self.lbl_city.config(text=msg)
        self.lbl_temp.config(text="")
        self.lbl_desc.config(text="")
        self.lbl_humidity.config(text="")
        self.lbl_wind.config(text="")
        self.search_done = True
        self.after(10, self._ajustar_altura_dinamica)

    def _reset_ui_state(self):
        self.is_fetching = False

    def _mostrar_informacion(self):
        InfoWindow(self, self.image_manager)

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (185)
        y = (self.winfo_screenheight() // 2) - (315)
        self.geometry(f"+{x}+{y}")

    def destroy(self):
        """Cierre controlado de recursos y hilos."""
        try:
            if self.loop.is_running():
                asyncio.run_coroutine_threadsafe(self.weather_service.close(), self.loop)
                self.loop.call_soon_threadsafe(self.loop.stop)
        except Exception as e:
            logger.error(f"Error al cerrar la aplicación: {e}")
        finally:
            super().destroy()
