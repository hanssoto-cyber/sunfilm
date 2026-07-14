from django.contrib import admin
from .models import Categoria, Servicio


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden', 'total_servicios')
    list_editable = ('orden',)
    prepopulated_fields = {'slug': ('nombre',)}

    @admin.display(description='N° de servicios')
    def total_servicios(self, obj):
        return obj.servicios.count()


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'destacado', 'activo', 'orden')
    list_editable = ('destacado', 'activo', 'orden')
    list_filter = ('categoria', 'destacado', 'activo')
    search_fields = ('nombre', 'descripcion_corta', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    fieldsets = (
        ('Información principal', {
            'fields': ('categoria', 'nombre', 'slug', 'descripcion_corta')
        }),
        ('Contenido', {
            'fields': ('descripcion', 'beneficios', 'imagen')
        }),
        ('Publicación', {
            'fields': ('destacado', 'activo', 'orden')
        }),
    )