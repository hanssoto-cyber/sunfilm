from django.shortcuts import render, redirect
from django.contrib import messages
from servicios.models import Servicio, Categoria
from galeria.models import Trabajo
from .forms import CotizacionForm
from django.http import HttpResponse

def home(request):
    destacados = Servicio.objects.filter(
        activo=True, destacado=True
    ).select_related('categoria')[:6]
    categorias = Categoria.objects.all()
    trabajos = Trabajo.objects.filter(
        activo=True, destacado=True
    ).select_related('servicio')[:8]

    return render(request, 'core/home.html', {
        'destacados': destacados,
        'categorias': categorias,
        'trabajos': trabajos,
    })


def nosotros(request):
    return render(request, 'core/nosotros.html')


def cotizar(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                '¡Gracias! Recibimos tu solicitud. Te contactamos a la brevedad.'
            )
            return redirect('core:cotizar')
        messages.error(request, 'Revisá los datos marcados en rojo.')
    else:
        servicio_id = request.GET.get('servicio')
        form = CotizacionForm(initial={'servicio': servicio_id} if servicio_id else None)

    return render(request, 'core/cotizar.html', {'form': form})

def robots_txt(request):
    lineas = [
        "User-agent: *",
        "Allow: /",
        "",
        "Sitemap: https://sunfilm.cl/sitemap.xml",
    ]
    return HttpResponse("\n".join(lineas), content_type="text/plain")