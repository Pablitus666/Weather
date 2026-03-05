from PIL import Image, ImageFilter, ImageChops

def apply_effects(image: Image.Image, shadow_offset=(3, 3), shadow_blur=5, shadow_opacity=40) -> Image.Image:
    """
    Aplica efectos de sombra proyectada con opacidad controlada.
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Crear el lienzo con padding para la sombra
    padding = shadow_blur * 2
    canvas_size = (image.width + padding, image.height + padding)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

    # Extraer la máscara alfa para la sombra con opacidad reducida (shadow_opacity)
    alpha = image.getchannel("A")
    shadow = Image.new("RGBA", image.size, (0, 0, 0, shadow_opacity)) 
    shadow.putalpha(alpha)
    
    # Aplicar desenfoque a la sombra
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    
    # Pegar la sombra
    canvas.paste(shadow, (padding // 2 + shadow_offset[0], padding // 2 + shadow_offset[1]), shadow)

    # Pegar la imagen original
    canvas.paste(image, (padding // 2, padding // 2), image)
    
    return canvas
