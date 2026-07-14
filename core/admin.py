from django.contrib import admin
from django.utils.html import format_html
from .models import Cotizacion


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono_link', 'servicio', 'comuna', 'estado', 'creado')
    list_filter = ('estado', 'servicio__categoria', 'creado')
    search_fields = ('nombre', 'telefono', 'email', 'mensaje', 'comuna')
    list_editable = ('estado',)
    readonly_fields = ('nombre', 'telefono', 'email', 'comuna', 'servicio',
                       'mensaje', 'creado', 'actualizado')
    date_hierarchy = 'creado'
    fieldsets = (
        ('Datos del cliente', {
            'fields': ('nombre', 'telefono', 'email', 'comuna')
        }),
        ('Solicitud', {
            'fields': ('servicio', 'mensaje', 'creado')
        }),
        ('Gestión interna', {
            'fields': ('estado', 'notas_internas', 'actualizado')
        }),
    )

    @admin.display(description='Teléfono')
    def telefono_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">{} 💬</a>',
            obj.whatsapp_url, obj.telefono
        )

    def has_add_permission(self, request):
        return False