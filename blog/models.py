from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class CategoriaPost(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Categoría del blog'
        verbose_name_plural = 'Categorías del blog'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class PostPublicadoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            estado=Post.PUBLICADO, publicado__lte=timezone.now()
        )


class Post(models.Model):
    BORRADOR = 'borrador'
    PUBLICADO = 'publicado'
    ESTADOS = [
        (BORRADOR, 'Borrador'),
        (PUBLICADO, 'Publicado'),
    ]

    titulo = models.CharField('Título', max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    categoria = models.ForeignKey(
        CategoriaPost, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='posts'
    )
    autor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='posts'
    )
    extracto = models.CharField(
        'Extracto', max_length=220,
        help_text='Resumen breve. Se muestra en el listado y en Google.'
    )
    contenido = models.TextField('Contenido')
    imagen = models.ImageField('Imagen destacada', upload_to='blog/%Y/%m/', blank=True)
    alt = models.CharField(
        'Texto alternativo', max_length=160, blank=True,
        help_text='Si lo dejas vacío se usa el título.'
    )
    servicio_relacionado = models.ForeignKey(
        'servicios.Servicio', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='posts',
        help_text='El artículo cierra ofreciendo este servicio.'
    )

    estado = models.CharField(max_length=20, choices=ESTADOS, default=BORRADOR)
    publicado = models.DateTimeField('Fecha de publicación', default=timezone.now)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    publicados = PostPublicadoManager()

    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos (Tips)'
        ordering = ['-publicado']
        indexes = [models.Index(fields=['-publicado'])]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('blog:detalle', kwargs={'slug': self.slug})

    @property
    def texto_alt(self):
        return self.alt or self.titulo