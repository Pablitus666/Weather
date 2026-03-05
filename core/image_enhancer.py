from PIL import Image, ImageFilter

def add_shadow(image: Image.Image, offset=(2, 2), shadow_color=(0, 0, 0, 128), blur_radius=3, border=5):
    """
    Adds a drop shadow to a transparent PIL Image on a symmetric canvas.
    This ensures the button's center is the canvas's center.
    REPLICA EXACTA STEGANO.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Para centrado perfecto, usamos un margen simétrico basado en el máximo desplazamiento
    pad = max(abs(offset[0]), abs(offset[1])) + border

    total_width = image.width + 2 * pad
    total_height = image.height + 2 * pad

    # Create a transparent background
    shadow_image = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))

    # Capa de sombra
    shadow_layer = Image.new('RGBA', image.size, shadow_color)

    # Pegamos la sombra con el desplazamiento
    shadow_image.paste(shadow_layer, (pad + offset[0], pad + offset[1]), image.getchannel('A'))

    # Blur
    if blur_radius > 0:
        shadow_image = shadow_image.filter(ImageFilter.GaussianBlur(blur_radius))

    # Pegamos la imagen original en el centro exacto
    shadow_image.paste(image, (pad, pad), image)

    return shadow_image
