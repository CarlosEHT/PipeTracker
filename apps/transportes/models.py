from django.db import models
from apps.servicio import models as servicio_models

# Create your models here.
class TipoPipa(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='tipo de pipa'
    )
    
    class Meta:
        db_table = 'tipo_pipa'
        verbose_name = 'Tipo de Pipa'
        verbose_name_plural = 'Tipos de Pipa'
        
    def __str__(self):
        return self.nombre


class Pipa(models.Model):
    no_pipa = models.CharField(
        max_length=20,
        blank=True,
        db_column='no_pipa',
        verbose_name='número de pipa'
    )
    placa = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='placa de la pipa'
    )
    capacidad = models.PositiveIntegerField(
        verbose_name='capacidad de la pipa (en litros)'
    )
    tipo_pipa = models.ForeignKey(
        TipoPipa,
        on_delete=models.CASCADE,
        verbose_name='tipo de pipa'
    )
    servicio = models.ForeignKey(
        servicio_models.Servicio,
        on_delete=models.PROTECT,
        verbose_name='servicio al que pertenece la pipa'
    )
    
    class Meta:
        db_table = 'pipa'
        verbose_name = 'Pipa'
        verbose_name_plural = 'Pipas'
        
    def __str__(self):
        return self.placa
