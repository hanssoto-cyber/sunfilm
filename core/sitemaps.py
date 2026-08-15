from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from servicios.models import Servicio
from blog.models import Post


class EstaticoSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'core:home',
            'core:nosotros',
            'core:cotizar',
            'servicios:lista',
            'galeria:lista',
            'blog:lista',
        ]

    def location(self, item):
        return reverse(item)


class ServicioSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Servicio.objects.filter(activo=True)

    def location(self, obj):
        return obj.get_absolute_url()


class PostSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Post.publicados.all()

    def lastmod(self, obj):
        return obj.actualizado

    def location(self, obj):
        return obj.get_absolute_url()