from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


def optimizar_imagen(imagen, max_ancho=1600, calidad=82):
    """
    Redimensiona y comprime una imagen antes de guardarla.
    - Reduce el ancho a max_ancho si es mayor (mantiene proporción).
    - Convierte a RGB y comprime como JPEG optimizado.
    Devuelve un ContentFile listo para asignar al ImageField.
    """
    img = Image.open(imagen)

    # Convertir a RGB (evita errores con PNG/transparencias al guardar como JPEG)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Redimensionar solo si es más ancha que el máximo
    if img.width > max_ancho:
        proporcion = max_ancho / img.width
        nuevo_alto = int(img.height * proporcion)
        img = img.resize((max_ancho, nuevo_alto), Image.LANCZOS)

    # Guardar comprimida en memoria
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=calidad, optimize=True)
    buffer.seek(0)

    return ContentFile(buffer.read())