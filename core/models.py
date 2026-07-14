from django.db import models


class Cotizacion(models.Model):
    ESTADO_NUEVO = 'nuevo'
    ESTADO_CONTACTADO = 'contactado'
    ESTADO_COTIZADO = 'cotizado'
    ESTADO_CERRADO = 'cerrado'
    ESTADO_DESCARTADO = 'descartado'

    ESTADOS = [
        (ESTADO_NUEVO, 'Nuevo'),
        (ESTADO_CONTACTADO, 'Contactado'),
        (ESTADO_COTIZADO, 'Cotización enviada'),
        (ESTADO_CERRADO, 'Cerrado / Vendido'),
        (ESTADO_DESCARTADO, 'Descartado'),
    ]

    nombre = models.CharField('Nombre', max_length=120)
    telefono = models.CharField('Teléfono', max_length=20)
    email = models.EmailField('Correo', blank=True)
    comuna = models.CharField('Comuna', max_length=80, blank=True)
    servicio = models.ForeignKey(
        'servicios.Servicio', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='cotizaciones',
        verbose_name='Servicio de interés'
    )
    mensaje = models.TextField('Mensaje', blank=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_NUEVO)
    notas_internas = models.TextField(
        blank=True, help_text='Uso interno. No lo ve el cliente.'
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-creado']

    def __str__(self):
        return f'{self.nombre} - {self.get_estado_display()} ({self.creado:%d/%m/%Y})'

    @property
    def whatsapp_url(self):
        numero = self.telefono.replace(' ', '').replace('+', '').lstrip('0')
        if not numero.startswith('56'):
            numero = '56' + numero
        return f'https://wa.me/{numero}'