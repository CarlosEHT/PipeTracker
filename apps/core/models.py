from django.db import models

# Create your models here.
class TipoAgua(models.Model):
    nombre = models.CharField(
        max_length=60,
        unique=True,
        verbose_name='nombre del tipo de agua'
    )
    
    class Meta:
        db_table = 'tipo_agua'
        verbose_name = 'Tipo de Agua'
        verbose_name_plural = 'Tipos de Agua'
        
    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(
        max_length=60,
        unique=True,
        verbose_name='nombre del estado'
    )
    
    class Meta:
        db_table = 'estado'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre
    
        
class Municipio(models.Model):
    nombre = models.CharField(
        max_length=60,
        verbose_name='municipio'
    )
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE,
        verbose_name='estado'
    )
    
    class Meta:
        db_table = 'municipio'
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        ordering = ['nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'estado'],
                name='unique_municipio_por_estado'
            )
        ]
        
    def __str__(self):
        return f"{self.nombre}, {self.estado}"
