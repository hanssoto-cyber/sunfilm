from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from servicios.models import Categoria
from .models import Trabajo


def lista(request):
    categoria_slug = request.GET.get('categoria')
    trabajos = Trabajo.objects.filter(activo=True).select_related(
        'servicio', 'servicio__categoria'
    )
    categorias = Categoria.objects.all()
    categoria_activa = None

    if categoria_slug:
        categoria_activa = get_object_or_404(Categoria, slug=categoria_slug)
        trabajos = trabajos.filter(servicio__categoria=categoria_activa)

    paginator = Paginator(trabajos, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'galeria/lista.html', {
        'page_obj': page_obj,
        'trabajos': page_obj.object_list,
        'categorias': categorias,
        'categoria_activa': categoria_activa,
    })