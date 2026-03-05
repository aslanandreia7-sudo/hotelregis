# hotel/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Contacto, Estadistica, ImagenHero,
    Habitacion, ImagenHabitacion, AmenidadHabitacion,
    ImagenRestaurante,
    CategoriaGaleria, ImagenGaleria,
    Amenidad, Testimonio,
)


# ─────────────────────────────────────────────────────────────
#  HELPER: preview de imagen en admin
# ─────────────────────────────────────────────────────────────
def imagen_preview(obj, campo='imagen', alto=80):
    img = getattr(obj, campo, None)
    if img:
        return format_html('<img src="{}" style="height:{}px;border-radius:4px;">', img.url, alto)
    return "—"


# ─────────────────────────────────────────────────────────────
#  CONTACTO  (solo 1 objeto — se bloquea add/delete)
# ─────────────────────────────────────────────────────────────
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    fieldsets = (
        ("📍 Dirección y Teléfono", {
            "fields": ("direccion", "telefono", "email")
        }),
        ("📱 Redes y WhatsApp", {
            "fields": ("whatsapp_number", "facebook_url")
        }),
    )

    def has_add_permission(self, request):
        return not Contacto.objects.exists()   # Solo permite crear si no existe ninguno

    def has_delete_permission(self, request, obj=None):
        return False


# ─────────────────────────────────────────────────────────────
#  ESTADÍSTICAS
# ─────────────────────────────────────────────────────────────
@admin.register(Estadistica)
class EstadisticaAdmin(admin.ModelAdmin):
    list_display  = ('valor', 'etiqueta', 'orden')
    list_editable = ('etiqueta', 'orden')
    ordering      = ('orden',)


# ─────────────────────────────────────────────────────────────
#  IMÁGENES HERO
# ─────────────────────────────────────────────────────────────
@admin.register(ImagenHero)
class ImagenHeroAdmin(admin.ModelAdmin):
    list_display  = ('preview', 'alt', 'orden', 'activo')
    list_editable = ('alt', 'orden', 'activo')
    ordering      = ('orden',)

    def preview(self, obj):
        return imagen_preview(obj)
    preview.short_description = "Vista Previa"


# ─────────────────────────────────────────────────────────────
#  HABITACIONES  (con inlines de fotos y amenidades)
# ─────────────────────────────────────────────────────────────
class ImagenHabitacionInline(admin.TabularInline):
    model      = ImagenHabitacion
    extra      = 1
    fields     = ('imagen', 'orden', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        return imagen_preview(obj)
    preview.short_description = "Vista"


class AmenidadHabitacionInline(admin.TabularInline):
    model = AmenidadHabitacion
    extra = 3
    fields = ('nombre',)


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display  = ('miniatura_preview', 'tipo', 'precio', 'orden', 'activo')
    list_editable = ('precio', 'orden', 'activo')
    ordering      = ('orden',)
    inlines       = [ImagenHabitacionInline, AmenidadHabitacionInline]

    fieldsets = (
        ("🛏 Información General", {
            "fields": ("tipo", "descripcion", "precio", "orden", "activo")
        }),
        ("🖼 Foto Principal", {
            "fields": ("miniatura", "miniatura_preview")
        }),
    )
    readonly_fields = ('miniatura_preview',)

    def miniatura_preview(self, obj):
        return imagen_preview(obj, 'miniatura', 60)
    miniatura_preview.short_description = "Vista"


# ─────────────────────────────────────────────────────────────
#  RESTAURANTE  —  Galería
# ─────────────────────────────────────────────────────────────
@admin.register(ImagenRestaurante)
class ImagenRestauranteAdmin(admin.ModelAdmin):
    list_display  = ('preview', 'alt', 'orden')
    list_editable = ('alt', 'orden')
    ordering      = ('orden',)

    def preview(self, obj):
        return imagen_preview(obj)
    preview.short_description = "Vista Previa"


# ─────────────────────────────────────────────────────────────
#  GALERÍA GENERAL
# ─────────────────────────────────────────────────────────────
@admin.register(CategoriaGaleria)
class CategoriaGaleriaAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'slug', 'orden')
    list_editable = ('orden',)
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(ImagenGaleria)
class ImagenGaleriaAdmin(admin.ModelAdmin):
    list_display   = ('preview', 'categoria', 'alt', 'orden', 'activo')
    list_editable  = ('categoria', 'alt', 'orden', 'activo')
    list_filter    = ('categoria', 'activo')
    ordering       = ('orden',)

    def preview(self, obj):
        return imagen_preview(obj)
    preview.short_description = "Vista Previa"


# ─────────────────────────────────────────────────────────────
#  AMENIDADES DEL HOTEL
# ─────────────────────────────────────────────────────────────
@admin.register(Amenidad)
class AmenidadAdmin(admin.ModelAdmin):
    list_display  = ('icono', 'nombre', 'descripcion', 'orden')
    list_editable = ('nombre', 'descripcion', 'orden')
    ordering      = ('orden',)


# ─────────────────────────────────────────────────────────────
#  TESTIMONIOS
# ─────────────────────────────────────────────────────────────
@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'ciudad', 'estrellas', 'orden', 'activo')
    list_editable = ('estrellas', 'orden', 'activo')
    ordering      = ('orden',)