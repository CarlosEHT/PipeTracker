from django.db import models
from apps.core import models as core_models
from apps.servicio import models as servicio_models
from apps.transportes import models as trasportes_models
from apps.usuarios import models as usuarios_models
from datetime import date

# Create your models here.
class Prioridad(models.Model):
    nombre = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='nombre de la prioridad'
    )
    
    class Meta:
        db_table = 'prioridad'
        verbose_name = 'Prioridad'
        verbose_name_plural = 'Prioridades'
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre
    
    
class TipoEntrega(models.Model):
    nombre = models.CharField(
        max_length=60,
        unique=True,
        verbose_name='tipo de entrega'
    )
    
    class Meta:
        db_table = 'tipo_entrega'
        verbose_name = 'Tipo de Entrega'
        verbose_name_plural = 'Tipos de Entrega'
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre
    
class Entrega(models.Model):
    folio_entrega = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='folio de entrega'
    )
    direccion = models.CharField(
        max_length=250,
        verbose_name="dirección de entrega"
    )
    latitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="latitud"
    )
    longitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="longitud"
    )
    fecha_entrega = models.DateField(
        default=date.today,
        verbose_name="fecha de entrega"
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="teléfono de contacto"
    )
    tipo_entrega = models.ForeignKey(
        TipoEntrega,
        on_delete=models.CASCADE,
        verbose_name="tipo de entrega"
    )
    prioridad = models.ForeignKey(
        Prioridad,
        on_delete=models.CASCADE,
        verbose_name="prioridad"
    )
    tipo_agua = models.ForeignKey(
        core_models.TipoAgua,
        on_delete=models.CASCADE,
        verbose_name="tipo de agua"
    )
    servicio = models.ForeignKey(
        servicio_models.Servicio,
        on_delete=models.PROTECT,
        verbose_name="servicio asociado"
    )
    cliente = models.ForeignKey(
        usuarios_models.CustomUser,
        on_delete=models.PROTECT,
        verbose_name="cliente"
    )
    pipa = models.ForeignKey(
        trasportes_models.Pipa,
        on_delete=models.PROTECT,
        verbose_name="pipa asignada"
    )
    
    class Meta:
        db_table = 'entrega'
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'

    def __str__(self):
        return f"{self.folio_entrega} - Cliente: {self.cliente.get_full_name()}"


class EntregaDiaria(models.Model):
    entrega = models.ForeignKey(
        Entrega,
        on_delete=models.CASCADE,
        verbose_name="entrega"
    )
    fecha = models.DateField(
        default=date.today,
        verbose_name="fecha del dia de entrega"
    )
    repartidor = models.ForeignKey(
        usuarios_models.CustomUser,
        on_delete=models.PROTECT,
        verbose_name="repartidor"
    )
    estatus = models.BooleanField(
        default=False,
        verbose_name="estatus de la entrega"
    )
    comentarios = models.TextField(
        blank=True,
        verbose_name="comentarios adicionales"
    )
    
    class Meta:
        db_table = 'entrega_diaria'
        verbose_name = 'Entrega Diaria'
        verbose_name_plural = 'Entregas Diarias'
        constraints = [
            models.UniqueConstraint(
                fields=['entrega'],
                name='unique_entrega_en_entrega_diaria'
            )
        ]

    def __str__(self):
        return f"Repartidor: {self.repartidor.get_full_name()} - Fecha: {self.fecha} - Estatus: {'Entregado' if self.estatus else 'Pendiente'}"