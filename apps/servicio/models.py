from django.db import models
from apps.core import models as core_models
from apps.usuarios import models as usuarios_models

# Create your models here.
class TipoServicio(models.Model):
    nombre = models.CharField(
        max_length=60,
        unique=True,
        verbose_name='nombre del tipo de servicio'
    )
    
    class Meta:
        db_table = 'tipo_servicio'
        verbose_name = 'Tipo de Servicio'
        verbose_name_plural = 'Tipos de Servicio'
        
    def __str__(self):
        return self.nombre
    

class Servicio(models.Model):
    representante = models.ForeignKey(
        usuarios_models.CustomUser,
        on_delete=models.PROTECT,
        verbose_name='representante'
    )
    municipio = models.ForeignKey(
        core_models.Municipio,
        on_delete=models.CASCADE,
        verbose_name='municipio'
    )
    tipo_servicio = models.ForeignKey(
        TipoServicio,
        on_delete=models.CASCADE,
        verbose_name='tipo de servicio'
    )
    estatus = models.BooleanField(
        default=True,
        verbose_name='estatus del servicio'
    )
    
    class Meta:
        db_table = 'servicio'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        constraints = [
            models.UniqueConstraint(
                fields=['representante', 'municipio', 'tipo_servicio'],
                name='unique_servicio_por_representante'
            )
        ]

    def __str__(self):
        return f"Servicio {self.tipo_servicio} de {self.municipio}"