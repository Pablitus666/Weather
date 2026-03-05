from PIL import Image, ImageTk, ImageEnhance
import os
from typing import Optional, Tuple
from collections import OrderedDict
from . import resources
from .image_enhancer import add_shadow
from utils.logger import logger

def _create_disabled_pil_image(pil_image: Image.Image) -> Image.Image:
    """Crea una versión semitransparente de una imagen."""
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    alpha = pil_image.getchannel('A')
    alpha = ImageEnhance.Brightness(alpha).enhance(0.4)
    disabled_img = pil_image.copy()
    disabled_img.putalpha(alpha)
    return disabled_img

class ImageManager:
    """
    REPLICA EXACTA STEGANO: Gestión LRU y DPI.
    Optimizado para detectar recursos faltantes.
    """
    def __init__(self, root, max_cache_size: int = 16):
        self.root = root
        self._photo_cache = OrderedDict()
        self._pil_cache = OrderedDict()
        self.max_cache_size = max_cache_size
        try:
            self.scale = root.winfo_fpixels('1i') / 96.0
        except Exception:
            self.scale = 1.0

    def load(
        self,
        filename: str,
        size: Optional[Tuple[int, int]] = None,
        add_shadow_effect: bool = False,
        shadow_offset: Tuple[int, int] = (2, 2),
        shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 128),
        blur_radius: int = 3,
        border: int = 5,
        return_disabled: bool = False
    ) -> ImageTk.PhotoImage | Tuple[ImageTk.PhotoImage, ImageTk.PhotoImage]:

        cache_key = (filename, size, add_shadow_effect, shadow_offset, shadow_color, blur_radius, border, self.scale)

        if not return_disabled and cache_key in self._photo_cache:
            self._photo_cache.move_to_end(cache_key)
            return self._photo_cache[cache_key]

        try:
            pil_image = self._get_base_pil(filename)
            
            # Si no se pudo obtener la imagen base, abortamos la carga
            if pil_image is None:
                return (None, None) if return_disabled else None

            if size:
                physical_size = (int(size[0] * self.scale), int(size[1] * self.scale))
                pil_image = pil_image.resize(physical_size, Image.LANCZOS)

            # Efecto de viveza sutil
            pil_image = ImageEnhance.Color(pil_image).enhance(1.05)

            if add_shadow_effect:
                pil_image = add_shadow(
                    pil_image,
                    offset=shadow_offset,
                    shadow_color=shadow_color,
                    blur_radius=blur_radius,
                    border=border
                )

            tk_img_normal = ImageTk.PhotoImage(pil_image)

            if return_disabled:
                disabled_pil = _create_disabled_pil_image(pil_image)
                tk_img_disabled = ImageTk.PhotoImage(disabled_pil)
                return (tk_img_normal, tk_img_disabled)

            self._store_in_cache(cache_key, tk_img_normal)
            return tk_img_normal

        except Exception as e:
            logger.error(f"Error en ImageManager.load para {filename}: {e}")
            return (None, None) if return_disabled else None

    def _store_in_cache(self, key, value):
        self._photo_cache[key] = value
        self._photo_cache.move_to_end(key)
        if len(self._photo_cache) > self.max_cache_size:
            self._photo_cache.popitem(last=False)

    def _get_base_pil(self, filename: str) -> Image.Image:
        if filename in self._pil_cache:
            self._pil_cache.move_to_end(filename)
            return self._pil_cache[filename]

        base_name = os.path.splitext(os.path.basename(filename))[0]
        paths_to_try = [
            os.path.join(resources.get_base_path(), "assets", "images", "png_master", f"{base_name}.png"),
            resources.image_path(filename),
            os.path.join(resources.get_base_path(), filename) if not os.path.isabs(filename) else filename
        ]

        for path in paths_to_try:
            if os.path.exists(path):
                try:
                    with Image.open(path) as img:
                        pil_img = img.convert("RGBA")
                        self._pil_cache[filename] = pil_img
                        self._pil_cache.move_to_end(filename)
                        if len(self._pil_cache) > self.max_cache_size:
                            self._pil_cache.popitem(last=False)
                        return pil_img
                except Exception:
                    continue

        return None # Importante: Devolver None si no existe
