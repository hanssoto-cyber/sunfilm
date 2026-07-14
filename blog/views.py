from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, CategoriaPost


def lista(request):
    posts = Post.publicados.select_related('categoria', 'autor')
    categorias = CategoriaPost.objects.all()
    categoria_activa = None
    busqueda = request.GET.get('q', '').strip()

    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        categoria_activa = get_object_or_404(CategoriaPost, slug=categoria_slug)
        posts = posts.filter(categoria=categoria_activa)

    if busqueda:
        posts = posts.filter(
            Q(titulo__icontains=busqueda) |
            Q(extracto__icontains=busqueda) |
            Q(contenido__icontains=busqueda)
        )

    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'blog/lista.html', {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'categorias': categorias,
        'categoria_activa': categoria_activa,
        'busqueda': busqueda,
    })


def detalle(request, slug):
    post = get_object_or_404(
        Post.publicados.select_related('categoria', 'autor', 'servicio_relacionado'),
        slug=slug
    )
    relacionados = Post.publicados.filter(
        categoria=post.categoria
    ).exclude(pk=post.pk).select_related('categoria')[:3]

    return render(request, 'blog/detalle.html', {
        'post': post,
        'relacionados': relacionados,
    })