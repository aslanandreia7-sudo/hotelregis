# hotel/views.py

from django.shortcuts import render
from .models import (
    Contacto, Estadistica, ImagenHero,
    Habitacion, ImagenRestaurante,
    CategoriaGaleria, ImagenGaleria,
    Amenidad, Testimonio,
)


def index(request):
    # ── Contacto (singleton, crea uno vacío si no existe) ──
    contacto, _ = Contacto.objects.get_or_create(pk=1)

    context = {
        "contacto":            contacto,
        "estadisticas":        Estadistica.objects.all(),
        "imagenes_hero":       ImagenHero.objects.filter(activo=True),
        "habitaciones":        Habitacion.objects.filter(activo=True).prefetch_related(
                                   'imagenes', 'amenidades'
                               ),
        "galeria_restaurante": ImagenRestaurante.objects.all(),
        "categorias_galeria":  CategoriaGaleria.objects.all(),
        "galeria_general":     ImagenGaleria.objects.filter(activo=True).select_related('categoria'),
        "amenidades":          Amenidad.objects.all(),
        "testimonios":         Testimonio.objects.filter(activo=True),
    }
    return render(request, "hotel/index.html", context)