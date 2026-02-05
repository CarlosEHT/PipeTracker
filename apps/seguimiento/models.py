import os
from uuid import uuid4
from io import BytesIO

from django.db import models
from django.core.files.base import ContentFile
from PIL import Image

from apps.entregas import models as entregas_models
from apps.usuarios import models as usuarios_models

class ImagenBase(models.Model):
    imagen = models.ImageField(
        upload_to='tmp/',
        verbose_name='imagen'
    )

    class Meta:
        abstract = True

    def _procesar_imagen(self, final_dir):
        """
        Procesa la imagen:
        - Redimensiona
        - Convierte a WEBP
        - Ajusta peso <= 1MB
        - Guarda en carpeta final
        """

        img = Image.open(self.imagen.path)

        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        img.thumbnail((1280, 1280))

        buffer = BytesIO()
        quality = 80
        img.save(buffer, format='WEBP', quality=quality)

        while buffer.tell() > 1 * 1024 * 1024 and quality > 30:
            buffer = BytesIO()
            quality -= 10
            img.save(buffer, format='WEBP', quality=quality)

        final_name = f"{uuid4().hex}.webp"
        final_path = os.path.join(final_dir, final_name)

        # Eliminar temporal
        if os.path.exists(self.imagen.path):
            os.remove(self.imagen.path)

        self.imagen.save(
            final_path,
            ContentFile(buffer.getvalue()),
            save=False
        )


class Evidencia(models.Model):
    entrega_diaria = models.ForeignKey(
        entregas_models.EntregaDiaria,
        on_delete=models.CASCADE,
        verbose_name='entrega diaria relacionada'
    )
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha y hora de la evidencia'
    )

    class Meta:
        db_table = 'evidencia'
        verbose_name = 'Evidencia'
        verbose_name_plural = 'Evidencias'

    def __str__(self):
        return f'Evidencia de {self.entrega_diaria} tomada el {self.fecha_hora}'

class ImagenEvidencia(ImagenBase):
    evidencia = models.ForeignKey(
        Evidencia,
        on_delete=models.CASCADE,
        verbose_name='evidencia',
        related_name='imagenes'
    )

    class Meta:
        db_table = 'imagen_evidencia'
        verbose_name = 'Imagen de Evidencia'
        verbose_name_plural = 'Imágenes de Evidencias'

    def __str__(self):
        return f'Imagen para {self.evidencia}'

    def save(self, *args, **kwargs):
        if not self.pk and self.imagen:
            # Guardar primero para que exista el archivo físico
            super().save(*args, **kwargs)

            try:
                servicio_id = self.evidencia.entrega_diaria.entrega.id
                final_dir = f"servicios/servicio_{servicio_id}"
                self._procesar_imagen(final_dir)
            except Exception:
                pass

        super().save(*args, **kwargs)

class Reporte(models.Model):
    entrega_diaria = models.ForeignKey(
        entregas_models.EntregaDiaria,
        on_delete=models.CASCADE,
        verbose_name='entrega diaria relacionada'
    )
    contenido = models.TextField(
        verbose_name='contenido del reporte'
    )
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha y hora del reporte'
    )

    class Meta:
        db_table = 'reporte'
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

    def __str__(self):
        return f'Reporte de {self.entrega_diaria} el {self.fecha_hora}'

class ImagenReporte(ImagenBase):
    reporte = models.ForeignKey(
        Reporte,
        on_delete=models.CASCADE,
        verbose_name='reporte',
        related_name='imagenes'
    )

    class Meta:
        db_table = 'imagen_reporte'
        verbose_name = 'Imagen de Reporte'
        verbose_name_plural = 'Imágenes de Reportes'

    def __str__(self):
        return f'Imagen para {self.reporte}'

    def save(self, *args, **kwargs):
        if not self.pk and self.imagen:
            super().save(*args, **kwargs)

            try:
                reporte_id = self.reporte.entrega_diaria.entrega.id
                final_dir = f"reportes/reporte_{reporte_id}"
                self._procesar_imagen(final_dir)
            except Exception:
                pass

        super().save(*args, **kwargs)

class RespuestaReporte(models.Model):
    reporte = models.ForeignKey(
        Reporte,
        on_delete=models.CASCADE,
        verbose_name='reporte'
    )
    usuario = models.ForeignKey(
        usuarios_models.CustomUser,
        on_delete=models.PROTECT,
        verbose_name='usuario que responde'
    )
    respuesta = models.TextField(
        verbose_name='respuesta al reporte'
    )
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='fecha y hora de la respuesta'
    )

    class Meta:
        db_table = 'respuesta_reporte'
        verbose_name = 'Respuesta de Reporte'
        verbose_name_plural = 'Respuestas de Reportes'

    def __str__(self):
        return (
            f'Respuesta para el reporte {self.reporte} '
            f'por {self.usuario.get_full_name()} '
            f'el {self.fecha_hora}'
        )
