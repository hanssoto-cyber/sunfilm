from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(
        max_length=50, default='bi-window',
        help_text='Clase de Bootstrap Icons. Ej: bi-car-front-fill'
    )
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='servicios'
    )
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    descripcion_corta = models.CharField(
        max_length=200, help_text='Se muestra en la tarjeta del listado.'
    )
    descripcion = models.TextField(help_text='Texto completo de la página de detalle.')
    beneficios = models.TextField(
        blank=True, help_text='Un beneficio por línea.'
    )
    imagen = models.ImageField(upload_to='servicios/', blank=True)
    destacado = models.BooleanField(
        default=False, help_text='Aparece en la portada.'
    )
    activo = models.BooleanField(default=True)
    orden = models.PositiveSmallIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['categoria__orden', 'orden', 'nombre']

    def __str__(self):
        return f'{self.nombre} ({self.categoria.nombre})'

    def get_absolute_url(self):
        return reverse('servicios:detalle', kwargs={'slug': self.slug})

    @property
    def lista_beneficios(self):
        return [b.strip() for b in self.beneficios.splitlines() if b.strip()]