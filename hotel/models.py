# hotel/models.py

from django.db import models


# ─────────────────────────────────────────────
#  CONTACTO DEL HOTEL (singleton: solo 1 fila)
# ─────────────────────────────────────────────
class Contacto(models.Model):
    direccion        = models.CharField(max_length=255, default="Av. Reforma 123, Mexicali, BC")
    telefono         = models.CharField(max_length=30,  default="+52 686 000 0000")
    email            = models.EmailField(default="info@hotelregis.mx")
    whatsapp_number  = models.CharField(max_length=20,  default="526860000000",
                                        help_text="Solo números, ej: 526861234567")
    facebook_url     = models.URLField(blank=True, default="https://facebook.com/hotelregismexicali")

    class Meta:
        verbose_name        = "Información de Contacto"
        verbose_name_plural = "Información de Contacto"

    def __str__(self):
        return "Contacto Hotel Regis"


# ─────────────────────────────────────────────
#  ESTADÍSTICAS (barra de números del hero)
# ─────────────────────────────────────────────
class Estadistica(models.Model):
    valor   = models.CharField(max_length=20, help_text="Ej: 50+, 30, ★4.8, 24/7")
    etiqueta = models.CharField(max_length=50, help_text="Ej: Habitaciones, Años de Historia")
    orden   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Estadística"
        verbose_name_plural = "Estadísticas"

    def __str__(self):
        return f"{self.valor} — {self.etiqueta}"


# ─────────────────────────────────────────────
#  IMÁGENES DEL HERO CAROUSEL
# ─────────────────────────────────────────────
class ImagenHero(models.Model):
    imagen  = models.ImageField(upload_to='hero/', help_text="Recomendado: 1920×1080px")
    alt     = models.CharField(max_length=100, blank=True, default="Hotel Regis Mexicali")
    orden   = models.PositiveSmallIntegerField(default=0)
    activo  = models.BooleanField(default=True)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Imagen Hero"
        verbose_name_plural = "Imágenes Hero (Carrusel Principal)"

    def __str__(self):
        return f"Hero #{self.orden} — {self.alt}"


# ─────────────────────────────────────────────
#  HABITACIONES
# ─────────────────────────────────────────────
class Habitacion(models.Model):
    tipo        = models.CharField(max_length=100, help_text="Ej: Suite Ejecutiva, Doble Estándar")
    descripcion = models.TextField(help_text="Descripción breve de la habitación")
    precio      = models.DecimalField(max_digits=8, decimal_places=2, help_text="Precio por noche en MXN")
    miniatura   = models.ImageField(upload_to='habitaciones/', help_text="Foto principal (600×400px)")
    orden       = models.PositiveSmallIntegerField(default=0)
    activo      = models.BooleanField(default=True)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Habitación"
        verbose_name_plural = "Habitaciones"

    def __str__(self):
        return self.tipo


class ImagenHabitacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, related_name='imagenes',
                                   on_delete=models.CASCADE)
    imagen     = models.ImageField(upload_to='habitaciones/galeria/',
                                   help_text="Fotos adicionales del cuarto")
    orden      = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Foto de Habitación"
        verbose_name_plural = "Fotos de Habitación"

    def __str__(self):
        return f"Foto de {self.habitacion.tipo} #{self.orden}"


class AmenidadHabitacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, related_name='amenidades',
                                   on_delete=models.CASCADE)
    nombre     = models.CharField(max_length=60, help_text="Ej: WiFi, A/C, TV, Desayuno")

    class Meta:
        verbose_name        = "Amenidad de Habitación"
        verbose_name_plural = "Amenidades de Habitación"

    def __str__(self):
        return f"{self.nombre} — {self.habitacion.tipo}"


# ─────────────────────────────────────────────
#  RESTAURANTE  —  Galería de fotos
# ─────────────────────────────────────────────
class ImagenRestaurante(models.Model):
    imagen = models.ImageField(upload_to='restaurante/',
                               help_text="Foto del restaurante (800×600px)")
    alt    = models.CharField(max_length=100, blank=True, default="Restaurante Villa Don Nacho")
    orden  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Foto Restaurante"
        verbose_name_plural = "Fotos Restaurante (Galería)"

    def __str__(self):
        return f"Restaurante #{self.orden}"


# ─────────────────────────────────────────────
#  GALERÍA GENERAL  (con categorías y filtros)
# ─────────────────────────────────────────────
class CategoriaGaleria(models.Model):
    nombre = models.CharField(max_length=60, help_text="Ej: Hotel, Habitaciones, Restaurante")
    slug   = models.SlugField(unique=True,   help_text="Ej: hotel, habitaciones, restaurante")
    orden  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Categoría de Galería"
        verbose_name_plural = "Categorías de Galería"

    def __str__(self):
        return self.nombre


class ImagenGaleria(models.Model):
    imagen    = models.ImageField(upload_to='galeria/',
                                  help_text="Foto para la galería general")
    categoria = models.ForeignKey(CategoriaGaleria, on_delete=models.SET_NULL,
                                  null=True, related_name='imagenes')
    alt       = models.CharField(max_length=100, blank=True)
    orden     = models.PositiveSmallIntegerField(default=0)
    activo    = models.BooleanField(default=True)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Imagen Galería"
        verbose_name_plural = "Imágenes Galería General"

    def __str__(self):
        return f"Galería — {self.categoria} #{self.orden}"


# ─────────────────────────────────────────────
#  AMENIDADES DEL HOTEL (sección de íconos)
# ─────────────────────────────────────────────
class Amenidad(models.Model):
    icono       = models.CharField(max_length=10, default="✓",
                                   help_text="Emoji o carácter. Ej: 🌐 ❄ 🅿 🍳")
    nombre      = models.CharField(max_length=80, help_text="Ej: WiFi Gratis, Alberca")
    descripcion = models.CharField(max_length=160, blank=True,
                                   default="Disponible para todos los huéspedes")
    orden       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Amenidad"
        verbose_name_plural = "Amenidades del Hotel"

    def __str__(self):
        return self.nombre


# ─────────────────────────────────────────────
#  TESTIMONIOS
# ─────────────────────────────────────────────
class Testimonio(models.Model):
    nombre   = models.CharField(max_length=80)
    ciudad   = models.CharField(max_length=80, blank=True, default="México")
    texto    = models.TextField(help_text="Comentario del huésped")
    estrellas = models.PositiveSmallIntegerField(default=5,
                                                  help_text="Del 1 al 5")
    activo   = models.BooleanField(default=True)
    orden    = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering            = ['orden']
        verbose_name        = "Testimonio"
        verbose_name_plural = "Testimonios"

    def __str__(self):
        return f"{self.nombre} — {self.estrellas}★"