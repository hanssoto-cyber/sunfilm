from django.contrib import admin
from django.utils.html import format_html
from .models import Trabajo


@admin.register(Trabajo)
class TrabajoAdmin(admin.ModelAdmin):
    list_display = ('miniatura', 'titulo', 'servicio', 'ubicacion',
                    'fecha_trabajo', 'destacado', 'activo', 'orden')
    list_display_links = ('miniatura', 'titulo')
    list_editable = ('destacado', 'activo', 'orden')
    list_filter = ('servicio__categoria', 'servicio', 'destacado', 'activo')
    search_fields = ('titulo', 'descripcion', 'ubicacion')
    date_hierarchy = 'fecha_trabajo'
    readonly_fields = ('vista_previa', 'creado')
    fieldsets = (
        ('Foto', {
            'fields': ('imagen', 'vista_previa', 'alt')
        }),
        ('Información', {
            'fields': ('titulo', 'servicio', 'descripcion', 'ubicacion', 'fecha_trabajo')
        }),
        ('Publicación', {
            'fields': ('destacado', 'activo', 'orden', 'creado')
        }),
    )

    @admin.display(description='Foto')
    def miniatura(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="height:50px;width:70px;object-fit:cover;border-radius:4px;">',
                obj.imagen.url
            )
        return '—'

    @admin.display(description='Vista previa')
    def vista_previa(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height:280px;border-radius:8px;">',
                obj.imagen.url
            )
        return 'Subí una foto y guardá para verla acá.'