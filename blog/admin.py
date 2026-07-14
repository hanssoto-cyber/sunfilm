from django.contrib import admin
from django.utils.html import format_html
from .models import Post, CategoriaPost


@admin.register(CategoriaPost)
class CategoriaPostAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_posts')
    prepopulated_fields = {'slug': ('nombre',)}

    @admin.display(description='N° de artículos')
    def total_posts(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('miniatura', 'titulo', 'categoria', 'estado', 'publicado', 'autor')
    list_display_links = ('miniatura', 'titulo')
    list_editable = ('estado',)
    list_filter = ('estado', 'categoria', 'publicado')
    search_fields = ('titulo', 'extracto', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'publicado'
    readonly_fields = ('vista_previa', 'creado', 'actualizado')
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'slug', 'categoria', 'extracto', 'contenido')
        }),
        ('Imagen destacada', {
            'fields': ('imagen', 'vista_previa', 'alt')
        }),
        ('Conversión', {
            'fields': ('servicio_relacionado',),
            'description': 'El artículo cierra invitando a cotizar este servicio.'
        }),
        ('Publicación', {
            'fields': ('estado', 'publicado', 'autor', 'creado', 'actualizado')
        }),
    )

    @admin.display(description='Foto')
    def miniatura(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="height:45px;width:65px;object-fit:cover;border-radius:4px;">',
                obj.imagen.url
            )
        return '—'

    @admin.display(description='Vista previa')
    def vista_previa(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height:250px;border-radius:8px;">', obj.imagen.url)
        return 'Subí una imagen y guardá para verla acá.'

    def save_model(self, request, obj, form, change):
        if not obj.autor:
            obj.autor = request.user
        super().save_model(request, obj, form, change)