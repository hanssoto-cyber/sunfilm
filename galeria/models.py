from django.db import models


class Trabajo(models.Model):
    titulo = models.CharField('Título', max_length=140)
    servicio = models.ForeignKey(
        'servicios.Servicio', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='trabajos',
        verbose_name='Servicio aplicado'
    )
    descripcion = models.TextField(
        'Descripción', blank=True,
        help_text='Opcional. Ej: "Oficina en Providencia, 40 m² de control solar."'
    )
    imagen = models.ImageField('Foto', upload_to='galeria/%Y/%m/')
    alt = models.CharField(
        'Texto alternativo', max_length=160, blank=True,
        help_text='Describe la foto para buscadores y lectores de pantalla. '
                  'Si lo dejas vacío se usa el título.'
    )
    ubicacion = models.CharField('Comuna / Lugar', max_length=100, blank=True)
    fecha_trabajo = models.DateField('Fecha del trabajo', null=True, blank=True)
    destacado = models.BooleanField(
        default=False, help_text='Aparece en la portada.'
    )
    activo = models.BooleanField(default=True)
    orden = models.PositiveSmallIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Trabajo'
        verbose_name_plural = 'Galería de trabajos'
        ordering = ['orden', '-fecha_trabajo', '-creado']

    def __str__(self):
        return self.titulo

    @property
    def texto_alt(self):
        return self.alt or self.titulo