from django.shortcuts import render, get_object_or_404
from .models import Categoria, Servicio


def lista(request):
    categoria_slug = request.GET.get('categoria')
    servicios = Servicio.objects.filter(activo=True).select_related('categoria')
    categorias = Categoria.objects.all()
    categoria_activa = None

    if categoria_slug:
        categoria_activa = get_object_or_404(Categoria, slug=categoria_slug)
        servicios = servicios.filter(categoria=categoria_activa)

    return render(request, 'servicios/lista.html', {
        'servicios': servicios,
        'categorias': categorias,
        'categoria_activa': categoria_activa,
    })


def detalle(request, slug):
    servicio = get_object_or_404(
        Servicio.objects.select_related('categoria'), slug=slug, activo=True
    )
    relacionados = Servicio.objects.filter(
        categoria=servicio.categoria, activo=True
    ).exclude(pk=servicio.pk)[:3]

    return render(request, 'servicios/detalle.html', {
        'servicio': servicio,
        'relacionados': relacionados,
    })